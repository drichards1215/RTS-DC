"""Build one "full story & badge" page per statue.

    python tools/build_statue_pages.py

Reads:
  artworks.json                   - facts, map pins, and the order statues appear in the Quest
  tools/statue_template.html      - the page layout (copied from the original Roosevelt page)
  tools/statue_content/*.py       - the story, badge and quiz for each statue
Writes:
  statues/<slug>.html             - one page per catalog statue that has content
  artworks.json                   - adds a "page" link to each entry (used by Catalog and Quest)

To change the wording on a page, edit its entry in tools/statue_content/ and run this again.
To change the layout of every page, edit tools/statue_template.html and run this again.
"""
import html, importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def roman(n):
    out = ""
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out += s
            n -= v
    return out


def load_content():
    content = {}
    for path in sorted((TOOLS / "statue_content").glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for title, entry in mod.STATUES.items():
            assert title not in content, f"{title} is defined twice"
            content[title] = entry
    return content


def paragraphs(paras):
    # Story text is written as HTML (it may contain <em>); the first paragraph gets the drop cap.
    dropcap = ' class="dropcap"'
    return "\n".join(
        f'      <p{dropcap if i == 0 else ""}>{p}</p>' for i, p in enumerate(paras))


def main():
    art_path = ROOT / "artworks.json"
    items = json.loads(art_path.read_text(encoding="utf-8"))
    content = load_content()
    template = (TOOLS / "statue_template.html").read_text(encoding="utf-8")

    # Only catalog entries that have written content get a page. Content for statues
    # no longer in the catalog is kept (parked) but not built.
    with_pages = [i for i in items if i["title"] in content]
    without = [i["title"] for i in items if i["title"] not in content]
    parked = [t for t in content if t not in {i["title"] for i in items}]

    for item in items:
        if item["title"] not in content:
            item.pop("page", None)

    for n, item in enumerate(with_pages):
        c = content[item["title"]]
        nxt = with_pages[(n + 1) % len(with_pages)]
        title = item["title"]

        qs = c["questions"]
        assert len(qs) == 5, f"{title}: needs 5 questions"
        for q, opts, ans in qs:
            assert 0 <= ans < len(opts), f"{title}: bad answer index in {q!r}"

        facts = c.get("facts") or [
            ("Sculptor", item["artist"]),
            ("Dedicated", item["year"]),
            ("Height", f'{item["height_ft"]:g} ft' if item["height_ft"] else ""),
            ("Material", item["material"]),
            ("Setting", c["setting"]),
        ]
        facts_html = "\n".join(
            f'      <div class="fact"><dt>{html.escape(k)}</dt><dd>{html.escape(str(v))}</dd></div>'
            for k, v in facts if v)

        radius = c.get("radius") or (250 if item["pin_accuracy"] == "exact" else 350)
        visit_note = c.get("visit_note") or (
            f"Location check-in works within about {round(radius * 1.0936, -1):g} yards of the statue. "
            "Your location is checked on your device and never sent anywhere.")
        more_label, more_url = c.get("more") or ("Read more on Wikipedia", item["source_url"])

        ring = c["ring"].upper()
        ring_size, ring_spacing = (13, 3) if len(ring) <= 18 else (11, 2) if len(ring) <= 22 else (9.5, 1.5)
        mono = c["mono"]
        mono_size = {1: 40, 2: 36, 3: 30}.get(len(mono), 24)
        sub = c.get("sub") or roman(int(item["year"]))
        sub_spacing = 2 if len(sub) <= 7 else 1

        badge = {
            "id": c["slug"],
            "name": title,
            "lat": item["lat"],
            "lng": item["lng"],
            "radiusMeters": radius,
            "passScore": 4,
            "questions": [{"q": q, "options": o, "answer": a} for q, o, a in qs],
        }
        badge_json = json.dumps(badge, ensure_ascii=False, indent=2).replace("</", "<\\/")
        badge_json = badge_json.replace("\n", "\n    ")

        out = template
        for key, val in {
            "TITLE": html.escape(title),
            "WHERE": html.escape(c["where"]),
            "FACTS": facts_html,
            "STATUE": paragraphs(c["statue"]),
            "QUOTE": c["quote"],
            "LIFE_TITLE": html.escape(c.get("life_title", "The Life")),
            "LIFE": paragraphs(c["life"]),
            "VISIT": c["visit"],
            "LAT": str(item["lat"]),
            "LNG": str(item["lng"]),
            "MORE_URL": html.escape(more_url),
            "MORE_LABEL": html.escape(more_label),
            "BADGE_TITLE": html.escape(c["badge_title"]),
            "RING": html.escape(ring),
            "RING_SIZE": f"{ring_size:g}",
            "RING_SPACING": f"{ring_spacing:g}",
            "MONO": html.escape(mono),
            "MONO_SIZE": str(mono_size),
            "SUB": html.escape(sub),
            "SUB_SPACING": str(sub_spacing),
            "VISIT_PROMPT": html.escape(c.get("visit_prompt", "Standing in front of it? Log your visit.")),
            "VISIT_NOTE_JSON": json.dumps(visit_note, ensure_ascii=False),
            "VISIT_NOTE": html.escape(visit_note),
            "NEXT_SLUG": content[nxt["title"]]["slug"],
            "NEXT_TITLE": html.escape(nxt["title"]),
            "BADGE_JSON": badge_json,
            "TOTAL": str(len(items)),
        }.items():
            out = out.replace(f"%%{key}%%", val)
        assert "%%" not in out, f"{title}: unfilled token"

        (ROOT / "statues" / f'{c["slug"]}.html').write_text(out, encoding="utf-8", newline="\n")
        item["page"] = f'statues/{c["slug"]}.html'

    with open(art_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Built {len(with_pages)} statue pages.")
    if without:
        print(f"No story yet ({len(without)}): " + ", ".join(without))
    if parked:
        print(f"Parked, not in catalog ({len(parked)}): " + ", ".join(parked))


if __name__ == "__main__":
    main()
