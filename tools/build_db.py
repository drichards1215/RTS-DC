"""Build the expanded DC statue database from the Wikipedia list.
Usage: python -I build_db.py <page.wiki> <existing artworks.json> <out.csv> <out.json> <cache dir>
"""
import csv, json, re, sys, time, urllib.parse, urllib.request, os, hashlib

def hash(s):  # stable across runs (built-in hash() is randomized)
    return int(hashlib.md5(s.encode()).hexdigest()[:12], 16)

wiki_path, existing_path, out_csv, out_json, cache_dir = sys.argv[1:6]
UA = {"User-Agent": "RTS-site-builder/1.0 (static site data build)"}
os.makedirs(cache_dir, exist_ok=True)

def get_json(url):
    key = os.path.join(cache_dir, str(abs(hash(url))) + ".json")
    if os.path.exists(key):
        return json.load(open(key, encoding="utf-8"))
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(6):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=30))
            break
        except urllib.error.HTTPError as err:
            if err.code != 429 or attempt == 5:
                raise
            wait = int(err.headers.get("Retry-After") or 0) or 5 * (attempt + 1)
            time.sleep(min(wait, 60))
    json.dump(data, open(key, "w", encoding="utf-8"))
    time.sleep(1.0)
    return data

def strip_markup(s):
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{.*?\}\}", "", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip(" ,.;")

# ---------- 1. Parse the list ----------
text = open(wiki_path, encoding="utf-8").read()
sections = re.split(r"(?m)^==([^=].*?)==\s*$", text)
entries = []
for i in range(1, len(sections), 2):
    name, body = sections[i].strip(), sections[i + 1]
    if name.startswith("Statues of historical"):
        kind = "Statue"
    elif name.startswith("Other outdoor"):
        kind = "Sculpture"
    else:
        continue
    for line in body.splitlines():
        if not line.startswith("*"):
            continue
        line = line.lstrip("* ").strip()
        m = re.search(r"\[\[([^|\]]+)(?:\|([^\]]+))?\]\]", line)
        if not m:
            continue
        article = m.group(1).strip()
        display = strip_markup(m.group(2) or m.group(1))
        rest = strip_markup(line[m.end():])
        rest = re.sub(r"^(at|in|on|near|outside|inside|,)\s+", "", rest, flags=re.I)
        entries.append({"article": article, "display": display, "location": rest, "kind": kind})

# ---------- 2. Wikipedia: coords, wikidata id, intro ----------
def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

titles = sorted({e["article"] for e in entries})
info, redirect = {}, {}
for batch in chunks(titles, 20):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "redirects": 1, "titles": "|".join(batch),
        "prop": "coordinates|pageprops|extracts|info", "inprop": "url",
        "exintro": 1, "explaintext": 1, "exsentences": 2, "exlimit": 20, "ppprop": "wikibase_item",
    })
    d = get_json("https://en.wikipedia.org/w/api.php?" + q)["query"]
    for r in d.get("normalized", []) + d.get("redirects", []):
        redirect[r["from"]] = r["to"]
    for p in d["pages"].values():
        info[p.get("title")] = {
            "coords": (p["coordinates"][0]["lat"], p["coordinates"][0]["lon"]) if p.get("coordinates") else None,
            "qid": p.get("pageprops", {}).get("wikibase_item"),
            "extract": p.get("extract", ""),
            "url": p.get("fullurl", ""),
        }

def resolve(t):
    seen = 0
    while t in redirect and seen < 5:
        t, seen = redirect[t], seen + 1
    return info.get(t, {})

# ---------- 3. Wikidata: artist, year, material, height, type ----------
qids = sorted({resolve(e["article"]).get("qid") for e in entries} - {None})
claims = {}
for batch in chunks(qids, 50):
    q = urllib.parse.urlencode({"action": "wbgetentities", "format": "json", "ids": "|".join(batch), "props": "claims"})
    claims.update(get_json("https://www.wikidata.org/w/api.php?" + q)["entities"])

def vals(qid, prop):
    out = []
    for c in claims.get(qid, {}).get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
        if v is not None:
            out.append(v)
    return out

label_ids = set()
for q in qids:
    for p in ("P170", "P186", "P31"):
        label_ids.update(v["id"] for v in vals(q, p) if isinstance(v, dict) and "id" in v)
labels = {}
for batch in chunks(sorted(label_ids), 50):
    q = urllib.parse.urlencode({"action": "wbgetentities", "format": "json", "ids": "|".join(batch), "props": "labels", "languages": "en"})
    for k, v in get_json("https://www.wikidata.org/w/api.php?" + q)["entities"].items():
        labels[k] = v.get("labels", {}).get("en", {}).get("value", "")

def lab(qid, prop):
    return [labels.get(v["id"], "") for v in vals(qid, prop) if isinstance(v, dict) and "id" in v]

def year(qid):
    for p in ("P571", "P1619", "P580"):
        for v in vals(qid, p):
            m = re.match(r"[+-](\d{4})", v.get("time", ""))
            if m:
                return int(m.group(1))
    return ""

def height_ft(qid):
    for v in vals(qid, "P2048"):
        amt, unit = float(v["amount"]), v.get("unit", "")
        if unit.endswith("Q11573"):
            return round(amt * 3.28084, 1)
        if unit.endswith("Q3710"):
            return round(amt, 1)
        if unit.endswith("Q174728"):
            return round(amt / 30.48, 1)
    return ""

# ---------- 4. Neighborhood guess from the location text ----------
AREAS = [
    ("Lincoln Park", "Lincoln Park / Capitol Hill"), ("Capitol", "Capitol Hill"), ("Union Station", "Capitol Hill"),
    ("Judiciary Square", "Judiciary Square"), ("Lafayette", "Lafayette Square"), ("White House", "Lafayette Square"),
    ("Meridian Hill", "Meridian Hill Park"), ("Dupont", "Dupont Circle"), ("Logan Circle", "Logan Circle"),
    ("Thomas Circle", "Thomas Circle"), ("Scott Circle", "Scott Circle"), ("Farragut", "Farragut Square"),
    ("McPherson", "McPherson Square"), ("Franklin Square", "Franklin Square"), ("Mount Vernon Square", "Mount Vernon Square"),
    ("Massachusetts Avenue", "Embassy Row"), ("Embassy", "Embassy Row"), ("Sheridan Circle", "Embassy Row"),
    ("Tidal Basin", "Tidal Basin"), ("West Potomac", "West Potomac Park"), ("East Potomac", "East Potomac Park"),
    ("Hains Point", "East Potomac Park"), ("Constitution Avenue", "National Mall"), ("National Mall", "National Mall"),
    ("Smithsonian", "National Mall"), ("Hirshhorn", "National Mall"), ("National Gallery", "National Mall"),
    ("Independence Avenue", "National Mall"), ("Pennsylvania Avenue", "Penn Quarter"), ("Navy Memorial", "Penn Quarter"),
    ("Foggy Bottom", "Foggy Bottom"), ("Kennedy Center", "Foggy Bottom"), ("Washington Circle", "Foggy Bottom"),
    ("George Washington University", "Foggy Bottom"), ("Cathedral", "Cathedral Heights"), ("Georgetown", "Georgetown"),
    ("Franciscan Monastery", "Brookland"), ("Catholic University", "Brookland"), ("Basilica", "Brookland"),
    ("Rock Creek", "Rock Creek Park"), ("Zoo", "Woodley Park"), ("Mount Pleasant", "Mount Pleasant / Columbia Heights"),
    ("16th Street", "16th Street NW"), ("Southwest", "Southwest Waterfront"), ("Wharf", "Southwest Waterfront"),
    ("Anacostia", "Anacostia"), ("Navy Yard", "Navy Yard"), ("Stanton Park", "Capitol Hill"),
    ("Marion Park", "Capitol Hill"), ("Gallaudet", "Northeast"), ("Columbia Heights", "Mount Pleasant / Columbia Heights"),
]

def area(loc, article):
    hay = f"{loc} {article}"
    for key, name in AREAS:
        if key.lower() in hay.lower():
            return name
    return "Other / Citywide"

# ---------- 5. Merge with the existing hand-made entries ----------
existing = json.load(open(existing_path, encoding="utf-8"))
rows, seen = [], set()
for e in existing:
    row = {k: e.get(k, "") for k in ("title", "artist", "year", "type", "material", "height_ft", "neighborhood", "location", "lat", "lng", "description")}
    row["source_url"] = e.get("source_url", "")
    row["pin_accuracy"] = "exact"
    rows.append(row)
    seen.add(e["title"].lower())

# Lines where the sculpture's name continues after the link
TITLE_FIX = {
    "Civil War": ("Nuns of the Battlefield (Civil War Nurses)", "M Street and Rhode Island Avenue NW", ""),
    "Red Cross": ("Red Cross Men and Women Killed in Service Memorial", "Red Cross National Headquarters garden, 1730 E Street NW", ""),
    "She Who Must Be Obeyed": ("She Who Must Be Obeyed", "Frances Perkins Building, 200 Constitution Avenue NW", "Tony Smith"),
}
# Hand-placed pins for places the geocoder can't find (approximate)
MANUAL = {
    "Albert Gallatin": (38.8988, -77.0340, "Lafayette Square"),
    "Alexander Hamilton": (38.8975, -77.0342, "Lafayette Square"),
    "Chuck Brown": (38.9255, -76.9748, "Northeast"),
    "Nuns of the Battlefield (Civil War Nurses)": (38.9058, -77.0383, "Dupont Circle"),
    "Eleanor Roosevelt": (38.8835, -77.0444, "West Potomac Park"),
    "Franklin D. Roosevelt": (38.8838, -77.0450, "West Potomac Park"),
    "Pope John Paul II": (38.9378, -77.0007, "Brookland"),
    "Red Cross Men and Women Killed in Service Memorial": (38.8955, -77.0399, "Foggy Bottom"),
    "She Who Must Be Obeyed": (38.8932, -77.0137, "Judiciary Square"),
    "Joseph Henry": (38.8889, -77.0260, "National Mall"),
    "(Here I Stand) In the Spirit of Paul Robeson": (38.9418, -77.0255, "Petworth"),
    "Albert Einstein": (38.8924, -77.0479, "Foggy Bottom"),
    "Albert Pike": (38.8945, -77.0157, "Judiciary Square"),
    "Alexander Pushkin": (38.8990, -77.0490, "Foggy Bottom"),
    "Alexander Robey Shepherd": (38.8950, -77.0313, "Penn Quarter"),
    "Archer Alexander": (38.8897, -76.9900, "Lincoln Park / Capitol Hill"),
    "Benito Juárez": (38.8976, -77.0545, "Foggy Bottom"),
    "Benjamin Franklin": (38.8938, -77.0275, "Penn Quarter"),
    "Bernardo de Gálvez": (38.8950, -77.0485, "Foggy Bottom"),
    "Boy Scout Memorial": (38.8937, -77.0365, "The Ellipse"),
    "Carter G. Woodson": (38.9104, -77.0240, "Shaw"),
    "Christopher Columbus": (38.8978, -77.0152, "Judiciary Square"),
    "Columbus Statue": (38.8962, -77.0071, "Capitol Hill"),
    "Comte Jean de Rochambeau": (38.8991, -77.0380, "Lafayette Square"),
    "Cordell Hull": (38.8929, -77.0398, "Organization of American States"),
    "Count Casimir Pulaski": (38.8960, -77.0297, "Penn Quarter"),
    "Crouching Woman": (38.8885, -77.0225, "National Mall"),
    "Crown Princess Märtha": (38.9240, -77.0670, "Embassy Row"),
    "Dante Alighieri": (38.9210, -77.0357, "Meridian Hill Park"),
    "Duke Ellington": (38.9155, -77.0220, "Shaw"),
    "Edmund Burke": (38.9013, -77.0270, "Mount Vernon Square"),
    "Edward Miner Gallaudet": (38.9075, -76.9930, "Northeast"),
    "Father Godfrey Schilling": (38.9370, -76.9853, "Brookland"),
    "Francis Scott Key": (38.9050, -77.0680, "Georgetown"),
    "Frank Howard": (38.8730, -77.0074, "Navy Yard"),
    "Josh Gibson": (38.8731, -77.0076, "Navy Yard"),
    "Walter Johnson": (38.8729, -77.0072, "Navy Yard"),
    "George Mason": (38.8795, -77.0390, "East Potomac Park"),
    "James A. Garfield": (38.8880, -77.0130, "Capitol Hill"),
    "James Buchanan": (38.9205, -77.0360, "Meridian Hill Park"),
    "James Earle Fraser": (38.8925, -77.0230, "National Mall"),
    "James Gibbons": (38.9310, -77.0365, "Mount Pleasant / Columbia Heights"),
    "Jane Delano": (38.8950, -77.0410, "Foggy Bottom"),
    "John A. Rawlins": (38.8955, -77.0425, "Foggy Bottom"),
    "John Marshall": (38.8925, -77.0155, "Judiciary Square"),
    "John Paul Jones": (38.8870, -77.0393, "National Mall"),
    "John Wesley": (38.9395, -77.0905, "Spring Valley"),
    "John Witherspoon": (38.9074, -77.0410, "Dupont Circle"),
    "José Cecilio del Valle": (38.8930, -77.0397, "Organization of American States"),
    "Pablo Neruda": (38.8928, -77.0399, "Organization of American States"),
    "Queen Isabella of Spain": (38.8931, -77.0399, "Organization of American States"),
    "Simon Bolivar, Libertador": (38.8927, -77.0397, "Organization of American States"),
    "Sor Juana Inés de la Cruz": (38.8930, -77.0400, "Organization of American States"),
    "Teresa de la Parra": (38.8928, -77.0396, "Organization of American States"),
    "Marion Barry": (38.8951, -77.0311, "Penn Quarter"),
    "Marquis Gilbert de Lafayette": (38.8991, -77.0354, "Lafayette Square"),
    "Martin Luther": (38.9058, -77.0322, "Thomas Circle"),
    "Martin Luther King Jr": (38.8862, -77.0442, "Tidal Basin / West Potomac Park"),
    "Mary McLeod Bethune Memorial": (38.8897, -76.9880, "Lincoln Park / Capitol Hill"),
    "Mary, Protector of Faith": (38.9333, -76.9970, "Brookland"),
    "Théodore Guérin": (38.9335, -76.9972, "Brookland"),
    "Michael Kováts de Fabricy": (38.9395, -77.0700, "Forest Hills"),
    "Mustafa Kemal Atatürk": (38.9137, -77.0545, "Embassy Row"),
    "Nathan Hale": (38.8925, -77.0240, "Penn Quarter"),
    "Nathanael Greene": (38.8946, -76.9988, "Capitol Hill"),
    "Nelson Mandela": (38.9188, -77.0612, "Embassy Row"),
    "Olive Risley Seward": (38.8857, -76.9975, "Capitol Hill"),
    "Robert A. Taft": (38.8930, -77.0110, "Capitol Hill"),
    "Robert Emmet": (38.9115, -77.0505, "Embassy Row"),
    "Saint Bernadette": (38.9372, -76.9851, "Brookland"),
    "Saint Christopher": (38.9369, -76.9855, "Brookland"),
    "Saint Francis of Assisi": (38.9370, -76.9853, "Brookland"),
    "Saint Michael": (38.9371, -76.9856, "Brookland"),
    "Samuel Gompers": (38.9010, -77.0258, "Mount Vernon Square"),
    "Samuel Hahnemann": (38.9070, -77.0365, "Scott Circle"),
    "Sir William Blackstone": (38.8924, -77.0160, "Judiciary Square"),
    "Spirit of Haida Gwaii": (38.8930, -77.0170, "Penn Quarter"),
    "Theodore Roosevelt": (38.8965, -77.0645, "Theodore Roosevelt Island"),
    "Thomas Hopkins Gallaudet": (38.9077, -76.9928, "Northeast"),
    "William O. Douglas": (38.9040, -77.0590, "Georgetown"),
    "Winfield Scott Hancock": (38.8937, -77.0220, "Penn Quarter"),
    "Winston Churchill": (38.9195, -77.0630, "Embassy Row"),
    "Boy Scout": (38.8937, -77.0365, "The Ellipse"),
    "The Burghers of Calais": (38.8886, -77.0228, "National Mall"),
}
skipped = []
missing_coords = []
for e in entries:
    if e["display"] in TITLE_FIX:
        t, loc, art = TITLE_FIX[e["display"]]
        e = dict(e, display=t, location=loc, artist_fix=art)
    meta = resolve(e["article"])
    qid = meta.get("qid")
    p31 = set(v["id"] for v in vals(qid, "P31") if isinstance(v, dict)) if qid else set()
    about_artwork = qid and "Q5" not in p31   # link goes to the artwork, not to the person
    title = e["display"]
    if title.lower() in seen:
        skipped.append(f"{title} @ {e['location']}")
        continue
    seen.add(title.lower())
    coords = meta.get("coords") if about_artwork else None
    if about_artwork:
        desc = meta.get("extract", "").strip()
        types = [t for t in lab(qid, "P31") if t]
        kind = types[0].capitalize() if types else e["kind"]
        artist = ", ".join(x for x in lab(qid, "P170") if x)
        mat = ", ".join(x for x in lab(qid, "P186") if x)
        yr, ht = year(qid), height_ft(qid)
    else:
        desc = f"{e['kind']} of {title}" + (f", located at {e['location']}." if e["location"] else ".")
        kind, artist, mat, yr, ht = e["kind"], e.get("artist_fix", ""), "", "", ""
    row = {
        "title": title, "artist": artist, "year": yr, "type": kind, "material": mat, "height_ft": ht,
        "neighborhood": area(e["location"], e["article"]), "location": e["location"],
        "lat": round(coords[0], 5) if coords else "", "lng": round(coords[1], 5) if coords else "",
        "description": desc, "source_url": meta.get("url", ""),
        "pin_accuracy": "exact" if coords else "approximate",
    }
    if title in MANUAL:
        lat, lng, hood = MANUAL[title]
        row.update(lat=lat, lng=lng, neighborhood=hood, pin_accuracy="approximate")
        rows.append(row)
        continue
    if not coords:
        missing_coords.append(row)
    rows.append(row)

# ---------- 6. Geocode rows with no coordinates (OpenStreetMap Nominatim, 1 req/sec) ----------
def geocode(q):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "limit": 1, "viewbox": "-77.12,38.995,-76.909,38.79", "bounded": 1})
    key = os.path.join(cache_dir, "geo_" + str(abs(hash(url))) + ".json")
    if os.path.exists(key):
        res = json.load(open(key, encoding="utf-8"))
    else:
        res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
        json.dump(res, open(key, "w", encoding="utf-8"))
        time.sleep(1.1)
    return (float(res[0]["lat"]), float(res[0]["lon"])) if res else None

still_missing = []
for row in missing_coords:
    loc = row["location"]
    tries = [f"{loc}, Washington, DC"] if loc else []
    first_place = re.split(r",| and | at ", loc)[0] if loc else ""
    if first_place and first_place != loc:
        tries.append(f"{first_place}, Washington, DC")
    if row["neighborhood"] != "Other / Citywide":
        tries.append(f"{row['neighborhood'].split(' / ')[0]}, Washington, DC")
    hit = None
    for t in tries:
        hit = geocode(t)
        if hit:
            break
    if hit:
        row["lat"], row["lng"] = round(hit[0], 5), round(hit[1], 5)
    else:
        still_missing.append(row["title"])

rows.sort(key=lambda r: r["title"].lower())
fields = ["title", "artist", "year", "type", "material", "height_ft", "neighborhood", "location", "lat", "lng", "description", "source_url", "pin_accuracy"]
print("skipped as duplicates:", skipped)
print("approximate pins:", sum(1 for r in rows if r["pin_accuracy"] == "approximate"))
with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
json.dump(rows, open(out_json, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

print("total rows:", len(rows))
print("from wikipedia with article coords:", sum(1 for r in rows if r not in missing_coords) - len(existing))
print("geocoded approx:", len(missing_coords) - len(still_missing))
print("no location found:", len(still_missing), still_missing)
print("with artist:", sum(1 for r in rows if r["artist"]), " with year:", sum(1 for r in rows if r["year"]))
