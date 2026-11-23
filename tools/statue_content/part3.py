# Story, badge and quiz content for each statue page (part 3 of 3).
# Keys must match "title" in artworks.json exactly.

STATUES = {

"John Paul Jones": {
    "slug": "john-paul-jones",
    "where": "West Potomac Park · 17th Street",
    "setting": "Foot of 17th Street, near the Tidal Basin",
    "badge_title": "John Paul Jones",
    "ring": "John Paul Jones", "mono": "JPJ",
    "statue": [
        "Where 17th Street meets Independence Avenue, near the Tidal Basin, a 10-foot bronze John Paul Jones stands in his naval uniform against a tall marble pylon. Water spills from two sculpted dolphins into a pool at his feet.",
        "Sculptor Charles Henry Niehaus made the memorial, which was dedicated in 1912. Walk around to the back of the pylon to find a carved scene of Jones raising the American flag aboard his ship.",
        "Jones himself is buried in Annapolis, Maryland. He died in Paris in 1792 and lay in a forgotten grave there for over a century, until his body was found in 1905 and brought home to a crypt at the U.S. Naval Academy.",
    ],
    "quote": "Losing his ship, he still won the battle.",
    "life_title": "The Man",
    "life": [
        "He was born John Paul in Scotland in 1747 and went to sea at 13. In the Caribbean he killed a mutinous sailor, fled, and added “Jones” to his name.",
        "When the Revolution began he joined the new Continental Navy and raided the coast of Britain itself. In September 1779, commanding the <em>Bonhomme Richard</em>, he fought the British warship <em>Serapis</em> off the English coast. With his ship burning and sinking, he is said to have answered a demand to surrender with: “I have not yet begun to fight!” Hours later the British captain surrendered, and Jones sailed away in the captured <em>Serapis</em>.",
        "After the war he served as an admiral in the Russian navy under Catherine the Great. Today he is often called the “Father of the American Navy.”",
    ],
    "visit": "The memorial is at 17th Street SW and Independence Avenue, just north of the Tidal Basin and a short walk from the Washington Monument. The Smithsonian Metro station is about 15 minutes away on foot.",
    "questions": [
        ("Where was John Paul Jones born?", ["Scotland", "Ireland", "Virginia"], 0),
        ("What was the name of his ship in the famous 1779 battle?", ["Old Ironsides", "Bonhomme Richard", "Hartford"], 1),
        ("What is he said to have shouted when asked to surrender?", ["“Damn the torpedoes!”", "“Don't give up the ship!”", "“I have not yet begun to fight!”"], 2),
        ("Where is he buried today?", ["The U.S. Naval Academy in Annapolis", "Paris", "Arlington National Cemetery"], 0),
        ("What is he often called?", ["The Sea Wolf", "The Father of the American Navy", "Old Salt"], 1),
    ],
},

"David G. Farragut": {
    "slug": "david-g-farragut",
    "where": "Farragut Square",
    "setting": "Center of Farragut Square",
    "badge_title": "Farragut",
    "ring": "David G. Farragut", "mono": "DGF",
    "statue": [
        "In the middle of Farragut Square, surrounded by office workers on their lunch breaks, Admiral David Farragut stands on deck with a telescope in hand, as if scanning the horizon.",
        "The bronze has a remarkable source: it was cast from the propeller of the USS <em>Hartford</em>, Farragut's flagship during the Civil War. The sculptor was Vinnie Ream, who as a teenager had been commissioned by Congress to sculpt Abraham Lincoln, making her the first woman to receive a federal commission for a statue. The Farragut statue was unveiled in 1881.",
        "Farragut is so much a part of the neighborhood that two Metro stations are named after him: Farragut North and Farragut West.",
    ],
    "quote": "An admiral cast from the propeller of his own flagship.",
    "life_title": "The Man",
    "life": [
        "He was born James Glasgow Farragut in Tennessee in 1801. After his mother died, he was taken in by naval officer David Porter, and he later changed his first name to David in Porter's honor. He joined the Navy as a midshipman at just 9, and at 12, during the War of 1812, he was put in charge of a captured ship.",
        "Though a Southerner, Farragut stayed loyal to the Union in the Civil War. In 1862 he captured New Orleans, the Confederacy's largest city. In 1864, leading his fleet into Mobile Bay past underwater mines, then called torpedoes, he is said to have ordered: “Damn the torpedoes! Full speed ahead!”",
        "Farragut became the U.S. Navy's first rear admiral, first vice admiral, and in 1866 its first full admiral. He died in 1870.",
    ],
    "visit": "Farragut Square is on K Street NW between 16th and 17th streets, directly above the Farragut North and Farragut West Metro stations.",
    "questions": [
        ("What was melted down to cast the statue?", ["Cannons from Fort Sumter", "The propeller of his flagship", "Old coins"], 1),
        ("What famous order is Farragut said to have given?", ["“Damn the torpedoes! Full speed ahead!”", "“I have not yet begun to fight!”", "“Fire when ready!”"], 0),
        ("How old was Farragut when he joined the Navy?", ["9", "16", "21"], 0),
        ("Sculptor Vinnie Ream was the first woman to get a federal commission for a statue of whom?", ["George Washington", "Abraham Lincoln", "David Farragut"], 1),
        ("Which city did Farragut capture in 1862?", ["Charleston", "Richmond", "New Orleans"], 2),
    ],
},

"William Tecumseh Sherman": {
    "slug": "william-tecumseh-sherman",
    "where": "President's Park · Sherman Plaza",
    "setting": "Sherman Plaza, beside the Treasury",
    "badge_title": "Sherman",
    "ring": "William T. Sherman", "mono": "WTS",
    "statue": [
        "Just south of the Treasury Building, General William Tecumseh Sherman sits on horseback atop a tall granite pedestal. Below him, soldiers stand guard at the four corners, representing the infantry, artillery, cavalry, and engineers, and bronze reliefs show scenes from his campaigns. The spot is said to be where Sherman stood in May 1865 to review his troops in the Grand Review of the Armies at the end of the Civil War.",
        "The monument had a troubled start. When Danish-born sculptor Carl Rohl-Smith won the commission in 1896, other leading sculptors protested the competition. Rohl-Smith then died in 1900 with the work unfinished, and his widow oversaw other artists to complete it. President Theodore Roosevelt spoke at the dedication in 1903.",
    ],
    "quote": "He made war hard so that it would end sooner, and the country is still arguing about what that cost.",
    "life_title": "The Man",
    "life": [
        "William Tecumseh Sherman was born in Ohio in 1820. His father named him after Tecumseh, the Shawnee leader. After West Point and the Army, he tried banking in San Francisco and ran a military academy in Louisiana before the Civil War began.",
        "He became one of the Union's most important generals, a close partner of Ulysses S. Grant. His capture of Atlanta in September 1864 helped Lincoln win re-election. Then came his March to the Sea: about 60,000 soldiers crossing Georgia to Savannah, destroying railroads, crops, and supplies to break the South's ability to fight. In early 1865 his Special Field Order No. 15 set aside land for freed families, the origin of the phrase “forty acres,” though President Andrew Johnson later reversed it.",
        "After the war Sherman commanded the U.S. Army for nearly 15 years, including during wars against Native nations on the Great Plains. Pressed to run for president, he flatly refused. He died in 1891.",
    ],
    "visit": "Sherman Plaza is on 15th Street NW at Pennsylvania Avenue, just south of the Treasury Building and next to the White House grounds. The McPherson Square and Metro Center stations are each about a 10-minute walk.",
    "questions": [
        ("Where did Sherman's March to the Sea end?", ["Atlanta", "Savannah", "Charleston"], 1),
        ("Sherman was named after whom?", ["A Shawnee leader", "A Roman emperor", "His grandfather"], 0),
        ("Which president spoke at the statue's dedication?", ["Abraham Lincoln", "Ulysses S. Grant", "Theodore Roosevelt"], 2),
        ("What did Special Field Order No. 15 set aside?", ["Land for freed families", "Money for veterans", "A national cemetery"], 0),
        ("What happened to the original sculptor?", ["He quit the project", "He died before finishing it", "He was fired"], 1),
    ],
},

"Philip Sheridan": {
    "slug": "philip-sheridan",
    "where": "Sheridan Circle · Embassy Row",
    "setting": "Sheridan Circle on Embassy Row",
    "badge_title": "Sheridan",
    "ring": "Philip Sheridan", "mono": "PHS",
    "statue": [
        "In the center of Sheridan Circle, surrounded by embassies, General Philip Sheridan reins in his charging horse, rallying his retreating troops. The bronze captures the moment at the Battle of Cedar Creek in October 1864 when Sheridan arrived and turned a defeat into a victory.",
        "The sculptor was Gutzon Borglum, who would later carve Mount Rushmore. The statue was dedicated in 1908.",
    ],
    "quote": "A twenty-mile gallop that turned a rout into a victory, frozen at the moment he arrived.",
    "life_title": "The Man",
    "life": [
        "Philip Sheridan was born in 1831 and grew up in Somerset, Ohio. At West Point he was suspended for a year for fighting with another cadet. He was short, about 5 feet 5 inches, and Lincoln once described him as a “brown, chunky little chap.”",
        "In the Civil War he rose quickly to command the cavalry under Ulysses S. Grant. In October 1864 Confederate forces surprised his army at Cedar Creek, Virginia, while Sheridan was away in Winchester. He galloped some 20 miles back to the battlefield on his horse, Rienzi, rallied his men, and won. The famous “Sheridan's Ride” inspired a popular poem, and Rienzi was renamed Winchester. In April 1865 Sheridan's cavalry helped block Robert E. Lee's escape just before the surrender at Appomattox.",
        "After the war he led campaigns against Native nations on the Great Plains, a harsh chapter of his career. He also pushed to protect Yellowstone, and from 1886 the Army guarded the park from poachers and vandals. He became commanding general of the Army and died in 1888.",
    ],
    "visit": "Sheridan Circle is on Massachusetts Avenue NW at 23rd Street, in the heart of Embassy Row, about a 10-minute walk from the Dupont Circle Metro station.",
    "questions": [
        ("The sculptor later carved which famous monument?", ["Mount Rushmore", "The Lincoln Memorial", "Stone Mountain"], 0),
        ("Which battle does the statue show?", ["Gettysburg", "Cedar Creek", "Bull Run"], 1),
        ("What was the name of Sheridan's horse?", ["Traveller", "Cincinnati", "Rienzi"], 2),
        ("Which national park did Sheridan help protect?", ["Yosemite", "Yellowstone", "Grand Canyon"], 1),
        ("Under which general did Sheridan command the cavalry?", ["Ulysses S. Grant", "George McClellan", "Winfield Scott"], 0),
    ],
},

"Winfield Scott": {
    "slug": "winfield-scott",
    "where": "Scott Circle",
    "setting": "Scott Circle, on 16th Street",
    "badge_title": "Scott",
    "ring": "Winfield Scott", "mono": "WS",
    "statue": [
        "In the middle of Scott Circle, where 16th Street meets Massachusetts and Rhode Island avenues, General Winfield Scott sits upright on a sturdy horse, high above the traffic.",
        "Sculptor Henry Kirke Brown made the statue from bronze cannons captured during the Mexican-American War, the war Scott himself had won. It was dedicated in 1874.",
    ],
    "quote": "He served under fourteen presidents, and the cannons he captured became his statue.",
    "life_title": "The Man",
    "life": [
        "Winfield Scott was born in Virginia in 1786. He became a hero in the War of 1812, where he was badly wounded at the Battle of Lundy's Lane. Tall, proud, and a stickler for proper uniforms and rules, he was nicknamed “Old Fuss and Feathers.”",
        "Scott served as an Army officer for more than 50 years, under 14 presidents, and was the Army's top general from 1841 to 1861. In 1838 he oversaw the forced removal of the Cherokee from their homeland, the Trail of Tears. In the Mexican-American War he landed his army at Veracruz and fought his way inland to capture Mexico City in 1847.",
        "He ran for president as the Whig candidate in 1852 and lost to Franklin Pierce. At the start of the Civil War, too old to take the field, he proposed the Anaconda Plan to blockade and squeeze the Confederacy, which became the backbone of Union strategy. He retired in 1861 and died at West Point in 1866.",
    ],
    "visit": "Scott Circle is on 16th Street NW at Massachusetts Avenue, about a 10-minute walk from either the Dupont Circle or Farragut North Metro station.",
    "questions": [
        ("What was the statue cast from?", ["Captured cannons", "Church bells", "Old coins"], 0),
        ("What was Scott's nickname?", ["“Old Hickory”", "“Old Fuss and Feathers”", "“Little Phil”"], 1),
        ("Which city did Scott capture in 1847?", ["Havana", "New Orleans", "Mexico City"], 2),
        ("What was Scott's plan for the Civil War called?", ["The Anaconda Plan", "The Cobra Plan", "The Eagle Plan"], 0),
        ("Who beat Scott in the 1852 presidential election?", ["Zachary Taylor", "Franklin Pierce", "Abraham Lincoln"], 1),
    ],
},

"Simón Bolívar": {
    "slug": "simon-bolivar",
    "where": "Foggy Bottom · Virginia Avenue",
    "setting": "Plaza near the Organization of American States",
    "badge_title": "Bolívar",
    "ring": "Simón Bolívar", "mono": "SB",
    "statue": [
        "On a small plaza along Virginia Avenue, near the headquarters of the Organization of American States, Simón Bolívar rides a horse at full stride, one arm raised, high on a stone base.",
        "The statue was a gift from the people of Venezuela, Bolívar's homeland, and was dedicated in 1959. The sculptor, Felix de Weldon, is best known for the Marine Corps War Memorial in Arlington, the famous scene of Marines raising the flag on Iwo Jima.",
    ],
    "quote": "The liberator of six nations, riding at a gallop a few blocks from the White House.",
    "life_title": "The Man",
    "life": [
        "Simón Bolívar was born in Caracas, Venezuela, in 1783 to a wealthy family and was orphaned as a child. While traveling in Europe as a young man, he stood on Monte Sacro, one of the hills of Rome, in 1805 and swore an oath not to rest until South America was free from Spain.",
        "He kept his word. Over two decades of war he led armies across jungles and over the Andes mountains, winning independence for what are now Venezuela, Colombia, Ecuador, Peru, Bolivia, and Panama. Bolivia is named after him, and across Latin America he is simply <em>El Libertador</em>, the Liberator.",
        "Bolívar dreamed of uniting the freed lands into one great nation, and for a time he led a union called Gran Colombia. But it broke apart amid rivalries. He died of tuberculosis in 1830, at 47.",
    ],
    "visit": "The statue is at 18th Street and C Street at Virginia Avenue NW, near the Organization of American States and the Department of the Interior, about a 10-minute walk from the Farragut West Metro station.",
    "questions": [
        ("Which country is named after Bolívar?", ["Bolivia", "Colombia", "Venezuela"], 0),
        ("On a hill in which city did young Bolívar swear to free South America?", ["Madrid", "Rome", "Paris"], 1),
        ("What is his famous title?", ["El Presidente", "El Conquistador", "El Libertador"], 2),
        ("Which country gave the statue?", ["Venezuela", "Spain", "Peru"], 0),
        ("Which famous memorial did the same sculptor make?", ["The Lincoln Memorial", "The Marine Corps War Memorial (Iwo Jima)", "The Vietnam Veterans Memorial"], 1),
    ],
},

"Christopher Columbus (Columbus Fountain)": {
    "slug": "christopher-columbus",
    "where": "Columbus Circle · Union Station",
    "setting": "Plaza in front of Union Station",
    "badge_title": "Columbus",
    "ring": "Christopher Columbus", "mono": "CC",
    "statue": [
        "Anyone arriving at Union Station by train walks out to find Christopher Columbus waiting. The explorer stands in a long cloak before a tall stone shaft topped by a globe, flanked by figures representing the Old World and the New, all rising above a wide, curving fountain.",
        "The marble memorial is by Chicago sculptor Lorado Taft. Congress paid for it after a campaign by the Knights of Columbus, and it was dedicated in 1912 with a huge parade.",
        "Like many Columbus monuments, it has become a focus of protest and debate over how he treated the Indigenous people of the Caribbean, and some have called for its removal. It still stands.",
    ],
    "quote": "Celebrated for a century, questioned in this one, and still the first statue many visitors to Washington see.",
    "life_title": "The Man",
    "life": [
        "Christopher Columbus was born in Genoa, Italy, around 1451 and became a sailor and navigator. He believed he could reach Asia by sailing west across the Atlantic. After years of rejection, he won the backing of Spain's King Ferdinand and Queen Isabella.",
        "On October 12, 1492, his three ships reached an island in the Bahamas. He went on to make four voyages, reaching Caribbean islands and the coasts of Central and South America, but to his death he insisted he had reached Asia.",
        "As governor of Hispaniola, Columbus enslaved and brutally mistreated the Taíno people, and Spanish rule devastated their population. Complaints about his harsh rule led to his arrest in 1500, and he was sent back to Spain in chains. He died in 1506. Columbus Day became a federal holiday in 1937, and today many places also mark the day as Indigenous Peoples' Day.",
    ],
    "visit": "The fountain is on Columbus Circle, directly in front of Union Station at Massachusetts Avenue NE. The Union Station Metro station is right inside.",
    "questions": [
        ("Which monarchs paid for Columbus's voyage?", ["Ferdinand and Isabella", "Henry VIII and Anne", "Louis XIV and Marie"], 0),
        ("In what year did Columbus first reach the Americas?", ["1066", "1492", "1607"], 1),
        ("Where did Columbus believe he had landed?", ["Africa", "Australia", "Asia"], 2),
        ("Which building does the memorial stand in front of?", ["The U.S. Capitol", "Union Station", "The Library of Congress"], 1),
        ("Which group campaigned for the memorial?", ["The Knights of Columbus", "The Navy League", "The Daughters of the American Revolution"], 0),
    ],
},

"George Mason": {
    "slug": "george-mason",
    "where": "George Mason Memorial · East Potomac Park",
    "setting": "Garden near the Jefferson Memorial",
    "badge_title": "Mason",
    "ring": "George Mason", "mono": "GM",
    "more": ("National Park Service", "https://www.nps.gov/gemm/"),
    "statue": [
        "In a quiet garden just southwest of the Jefferson Memorial, George Mason sits on a stone bench with his legs crossed, a book in hand and more books stacked beside him, his hat and cane set down. He looks like a man taking a break, and there's room on the bench to sit down next to him.",
        "The bronze by sculptor Wendy M. Ross was dedicated in 2002. Mason is one of the least-known founders honored with a memorial in Washington, but his ideas are carved into the stone around him.",
    ],
    "quote": "The founder who refused to sign the Constitution, and got the Bill of Rights because of it.",
    "life_title": "The Man",
    "life": [
        "George Mason was born in Virginia in 1725 and became a wealthy planter at his estate, Gunston Hall, where he enslaved more than 100 people. He was a neighbor and friend of George Washington.",
        "In 1776 he wrote the Virginia Declaration of Rights, which promised freedom of the press, freedom of religion, and trial by jury. Thomas Jefferson drew on its ideas for the Declaration of Independence weeks later.",
        "At the Constitutional Convention in 1787, Mason refused to sign the finished Constitution, partly because it had no bill of rights and partly because it let the slave trade continue for 20 more years. His objections helped push Congress to add the Bill of Rights in 1791, which is why he is often called the “Father of the Bill of Rights.” He died in 1792. George Mason University in Virginia is named for him.",
    ],
    "visit": "The memorial is on Ohio Drive SW in East Potomac Park, a few minutes' walk from the Jefferson Memorial along the Tidal Basin. It's open at all times.",
    "questions": [
        ("Why did Mason refuse to sign the Constitution?", ["It had no bill of rights", "He wanted a king", "He missed the vote"], 0),
        ("Which document did Mason write in 1776?", ["The Articles of Confederation", "The Virginia Declaration of Rights", "The Federalist Papers"], 1),
        ("What is Mason often called?", ["The Father of the Constitution", "The Sage of Monticello", "The Father of the Bill of Rights"], 2),
        ("What was the name of Mason's estate?", ["Gunston Hall", "Mount Vernon", "Monticello"], 0),
        ("How is Mason shown in the statue?", ["On horseback", "Seated on a bench", "Giving a speech"], 1),
    ],
},

}
