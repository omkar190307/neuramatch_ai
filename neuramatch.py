"""
NeuraMatch - AI Recommendation Engine (Terminal Version)
DecodeLabs | AI Project 3

HOW TO RUN IN VS CODE:
  1. Open terminal  (Ctrl + `)
  2. Run:  python neuramatch.py
"""

import os, sys, math, time
sys.stdout.reconfigure(encoding='utf-8')

from colorama import init, Fore, Style
init(autoreset=True)

# ─── COLOR HELPERS ────────────────────────────────────────

def clr(text, color):  return color + str(text) + Style.RESET_ALL
def bold(text):        return Style.BRIGHT + str(text) + Style.RESET_ALL
def dim(text):         return Style.DIM + str(text) + Style.RESET_ALL

P  = Fore.MAGENTA   # purple
C  = Fore.CYAN      # cyan
G  = Fore.GREEN     # green
Y  = Fore.YELLOW    # yellow
W  = Fore.WHITE     # white
GR = Fore.WHITE + Style.DIM  # grey

# ─── DATASET ──────────────────────────────────────────────

CATALOG = {
    "1": {
        "name": "Movies", "icon": "[Movie]",
        "tags": ["Action","Comedy","Drama","Sci-Fi","Horror","Romance","Thriller","Animation","Mystery","Fantasy"],
        "items": [
            {"title":"Inception",                        "meta":"2010 | Christopher Nolan",    "tags":["Sci-Fi","Thriller","Mystery","Drama"]},
            {"title":"The Dark Knight",                  "meta":"2008 | Christopher Nolan",    "tags":["Action","Drama","Thriller","Mystery"]},
            {"title":"Interstellar",                     "meta":"2014 | Christopher Nolan",    "tags":["Sci-Fi","Drama","Fantasy","Mystery"]},
            {"title":"Parasite",                         "meta":"2019 | Bong Joon-ho",         "tags":["Drama","Thriller","Mystery","Comedy"]},
            {"title":"Get Out",                          "meta":"2017 | Jordan Peele",         "tags":["Horror","Thriller","Mystery","Drama"]},
            {"title":"La La Land",                       "meta":"2016 | Damien Chazelle",      "tags":["Romance","Drama","Comedy","Fantasy"]},
            {"title":"Avengers: Endgame",                "meta":"2019 | Russo Brothers",       "tags":["Action","Sci-Fi","Fantasy","Drama"]},
            {"title":"Spider-Man: Into the Spider-Verse","meta":"2018 | Animation",            "tags":["Animation","Action","Sci-Fi","Fantasy"]},
            {"title":"Everything Everywhere All at Once","meta":"2022 | EEAAO",               "tags":["Sci-Fi","Comedy","Action","Fantasy","Drama"]},
            {"title":"Arrival",                          "meta":"2016 | Denis Villeneuve",     "tags":["Sci-Fi","Drama","Mystery","Thriller"]},
            {"title":"Knives Out",                       "meta":"2019 | Rian Johnson",         "tags":["Mystery","Comedy","Thriller","Drama"]},
            {"title":"Spirited Away",                    "meta":"2001 | Hayao Miyazaki",       "tags":["Animation","Fantasy","Drama","Romance"]},
        ]
    },
    "2": {
        "name": "Music", "icon": "[Music]",
        "tags": ["Pop","Hip-Hop","Rock","Electronic","Jazz","Classical","R&B","Indie","Metal","Lo-Fi"],
        "items": [
            {"title":"Random Access Memories",   "meta":"Daft Punk | 2013",      "tags":["Electronic","Pop","Indie","Jazz"]},
            {"title":"To Pimp a Butterfly",      "meta":"Kendrick Lamar | 2015", "tags":["Hip-Hop","R&B","Jazz","Indie"]},
            {"title":"The Dark Side of the Moon","meta":"Pink Floyd | 1973",      "tags":["Rock","Classical","Electronic","Indie"]},
            {"title":"Blonde",                   "meta":"Frank Ocean | 2016",    "tags":["R&B","Indie","Pop","Electronic"]},
            {"title":"Midnights",                "meta":"Taylor Swift | 2022",   "tags":["Pop","Indie","Electronic","R&B"]},
            {"title":"Demon Days",               "meta":"Gorillaz | 2005",       "tags":["Electronic","Hip-Hop","Rock","Indie"]},
            {"title":"Discovery",                "meta":"Daft Punk | 2001",      "tags":["Electronic","Pop","R&B","Indie"]},
            {"title":"Kind of Blue",             "meta":"Miles Davis | 1959",    "tags":["Jazz","Classical","Indie"]},
            {"title":"Nevermind",                "meta":"Nirvana | 1991",        "tags":["Rock","Metal","Indie"]},
            {"title":"Currents",                 "meta":"Tame Impala | 2015",    "tags":["Indie","Electronic","Pop","Rock"]},
            {"title":"Ctrl",                     "meta":"SZA | 2017",            "tags":["R&B","Pop","Hip-Hop","Indie"]},
            {"title":"Lofi Hip Hop Essentials",  "meta":"Various Artists",       "tags":["Lo-Fi","Hip-Hop","Jazz","Indie"]},
        ]
    },
    "3": {
        "name": "Books", "icon": "[Book]",
        "tags": ["Fiction","Sci-Fi","Mystery","Fantasy","Non-Fiction","Romance","Thriller","Horror","Biography","Philosophy"],
        "items": [
            {"title":"Dune",                     "meta":"Frank Herbert | 1965",        "tags":["Sci-Fi","Fiction","Fantasy","Philosophy"]},
            {"title":"The Name of the Wind",     "meta":"Patrick Rothfuss | 2007",     "tags":["Fantasy","Fiction","Romance","Mystery"]},
            {"title":"Project Hail Mary",        "meta":"Andy Weir | 2021",            "tags":["Sci-Fi","Fiction","Mystery","Non-Fiction"]},
            {"title":"Gone Girl",                "meta":"Gillian Flynn | 2012",        "tags":["Thriller","Mystery","Fiction","Horror"]},
            {"title":"Sapiens",                  "meta":"Yuval Harari | 2011",         "tags":["Non-Fiction","Biography","Philosophy","Sci-Fi"]},
            {"title":"The Hitchhiker's Guide",   "meta":"Douglas Adams | 1979",        "tags":["Sci-Fi","Fiction","Fantasy","Philosophy"]},
            {"title":"Normal People",            "meta":"Sally Rooney | 2018",         "tags":["Romance","Fiction","Philosophy"]},
            {"title":"The Shining",             "meta":"Stephen King | 1977",         "tags":["Horror","Thriller","Mystery","Fiction"]},
            {"title":"Thinking, Fast and Slow",  "meta":"Daniel Kahneman | 2011",     "tags":["Non-Fiction","Philosophy","Biography"]},
            {"title":"Mistborn",                 "meta":"Brandon Sanderson | 2006",    "tags":["Fantasy","Fiction","Mystery","Thriller"]},
            {"title":"The Midnight Library",     "meta":"Matt Haig | 2020",            "tags":["Fiction","Fantasy","Philosophy","Romance"]},
            {"title":"Atomic Habits",            "meta":"James Clear | 2018",          "tags":["Non-Fiction","Philosophy","Biography"]},
        ]
    },
    "4": {
        "name": "Games", "icon": "[Game]",
        "tags": ["RPG","Action","Strategy","Horror","Puzzle","Open World","Shooter","Indie","Adventure","Simulation"],
        "items": [
            {"title":"The Witcher 3",        "meta":"CD Projekt Red | 2015",    "tags":["RPG","Open World","Action","Adventure"]},
            {"title":"Elden Ring",           "meta":"FromSoftware | 2022",      "tags":["RPG","Action","Open World","Horror"]},
            {"title":"Hollow Knight",        "meta":"Team Cherry | 2017",       "tags":["Indie","Action","Adventure","Puzzle"]},
            {"title":"Portal 2",            "meta":"Valve | 2011",             "tags":["Puzzle","Indie","Adventure"]},
            {"title":"Civilization VI",      "meta":"2K Games | 2016",          "tags":["Strategy","Simulation","Open World"]},
            {"title":"Resident Evil 4",      "meta":"Capcom | 2023",            "tags":["Horror","Action","Shooter","Adventure"]},
            {"title":"Stardew Valley",       "meta":"ConcernedApe | 2016",      "tags":["Simulation","Indie","RPG","Open World"]},
            {"title":"Hades",                "meta":"Supergiant Games | 2020",  "tags":["Action","RPG","Indie","Adventure"]},
            {"title":"Outer Wilds",          "meta":"Mobius Digital | 2019",    "tags":["Adventure","Puzzle","Open World","Indie"]},
            {"title":"DOOM Eternal",         "meta":"id Software | 2020",       "tags":["Shooter","Action","Horror"]},
            {"title":"Disco Elysium",        "meta":"ZA/UM | 2019",             "tags":["RPG","Adventure","Puzzle","Indie"]},
            {"title":"Total War: Shogun 2",  "meta":"Creative Assembly | 2011", "tags":["Strategy","Simulation","Action"]},
        ]
    }
}

# ─── UTILS ────────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Press Enter to continue..."):
    input(clr(f"\n  {msg}", GR))

def divider(w=56):
    print(clr("-" * w, P + Style.DIM))

def section(title):
    print()
    divider()
    print(clr(f"  {title}", C + Style.BRIGHT))
    divider()

def bar(ratio, width=28):
    filled = round(ratio * width)
    return clr("#" * filled, G) + clr("." * (width - filled), GR)

def cosine(user_vec, item_vec, tags):
    dot = mag_u = mag_i = 0.0
    for t in tags:
        u = user_vec.get(t, 0)
        i = item_vec.get(t, 0)
        dot   += u * i
        mag_u += u * u
        mag_i += i * i
    if mag_u == 0 or mag_i == 0:
        return 0.0
    return dot / (math.sqrt(mag_u) * math.sqrt(mag_i))

def loading():
    frames = [
        "[                            ]",
        "[###                         ]",
        "[######                      ]",
        "[#########                   ]",
        "[############                ]",
        "[###############             ]",
        "[##################          ]",
        "[#####################       ]",
        "[########################    ]",
        "[############################]",
    ]
    for f in frames:
        sys.stdout.write(f"\r  {clr('Computing similarity...', C)}  {clr(f, G)}")
        sys.stdout.flush()
        time.sleep(0.07)
    print()

# ─── SCREENS ──────────────────────────────────────────────

def banner():
    clear()
    print()
    print(clr("  +------------------------------------------------------+", P))
    print(clr("  |", P) + clr("        NeuraMatch  -  AI Recommendation Engine        ", C + Style.BRIGHT) + clr("|", P))
    print(clr("  |", P) + clr("              DecodeLabs  |  AI Project 3              ", Y)                + clr("|", P))
    print(clr("  |", P) + clr("    Cosine Similarity  |  Pattern Matching  |  AI      ", GR)              + clr("|", P))
    print(clr("  +------------------------------------------------------+", P))
    print()

def how_it_works():
    section("HOW THE AI WORKS  |  Algorithm")
    print()
    rows = [
        ("1", "User Vector",      "Your tags + weights  =>  U = [w1, w2, ..., wn]"),
        ("2", "Item Vectors",     "Each item encodes     =>  I = [0 or 1, ...]"),
        ("3", "Cosine Similarity","sim(U,I) = (U . I) / (|U| x |I|)"),
        ("4", "Ranked Output",    "Sort items by score, show top matches"),
    ]
    for num, name, desc in rows:
        print(f"   {clr(num, Y + Style.BRIGHT)}.  {clr(name.ljust(20), C + Style.BRIGHT)}  {clr(desc, W)}")
    print()
    pause("Press Enter to start...")

def pick_category():
    section("STEP 1  |  Choose a Category")
    print()
    for k, cat in CATALOG.items():
        print(f"   {clr(k, Y + Style.BRIGHT)}.  {clr(cat['icon'], C)}  {bold(cat['name'])}")
    print()
    while True:
        ch = input(clr("  Enter 1 / 2 / 3 / 4 : ", W)).strip()
        if ch in CATALOG:
            return ch
        print(clr("  [!] Enter 1, 2, 3, or 4", Fore.RED))

def pick_tags(cat):
    section("STEP 2  |  Select Your Interests")
    tags = cat["tags"]
    print(clr("  Type tag numbers separated by commas  e.g.  1,3,5", GR))
    print(clr("  Or type 'all' to select everything\n", GR))
    for i, t in enumerate(tags, 1):
        print(f"   {clr(str(i).rjust(2), Y)}.  {t}")
    print()
    while True:
        raw = input(clr("  Your choices: ", W)).strip()
        if not raw:
            print(clr("  [!] Select at least one.", Fore.RED)); continue
        if raw.lower() == "all":
            return set(tags)
        parts = [p.strip() for p in raw.split(",")]
        chosen, ok = set(), True
        for p in parts:
            if p.isdigit() and 1 <= int(p) <= len(tags):
                chosen.add(tags[int(p)-1])
            else:
                print(clr(f"  [!] '{p}' is not valid. Try again.", Fore.RED)); ok = False; break
        if ok and chosen:
            print(f"\n  {clr('Selected:', G + Style.BRIGHT)} {', '.join(sorted(chosen))}")
            return chosen

def set_weights(selected):
    section("STEP 3  |  Rate Preference Strength  (1=low  10=high)")
    print(clr("  Press Enter to use default = 5\n", GR))
    weights = {}
    for tag in sorted(selected):
        while True:
            raw = input(f"   {clr(tag.ljust(18), C)}  weight [1-10]: ").strip()
            if raw == "":
                weights[tag] = 5; break
            if raw.isdigit() and 1 <= int(raw) <= 10:
                weights[tag] = int(raw); break
            print(clr("   [!] Enter 1-10", Fore.RED))
    return weights

def show_results(cat, selected, weights):
    section("COMPUTING  |  Running Cosine Similarity")
    loading()

    all_tags = cat["tags"]
    user_vec = {t: weights.get(t, 0) for t in all_tags}

    scored = []
    for item in cat["items"]:
        iv      = {t: (1 if t in item["tags"] else 0) for t in all_tags}
        score   = cosine(user_vec, iv, all_tags)
        matched = [t for t in item["tags"] if t in selected]
        scored.append({**item, "score": score, "matched": matched})

    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]["score"] if scored[0]["score"] > 0 else 1.0

    # ── Score Chart ──────────────────────────────
    section("SIMILARITY SCORE CHART  |  All Items")
    print()
    for item in scored:
        ratio = item["score"] / best
        pct   = f"{item['score']*100:5.1f}%"
        name  = item["title"][:28].ljust(28)
        print(f"   {clr(name, W)}  {bar(ratio)}  {clr(pct, G + Style.BRIGHT)}")
    print()
    pause()

    # ── Top Results ──────────────────────────────
    clear(); banner()
    section("RESULTS  |  Top 6 Recommendations for You")
    print()

    medals = ["#1 GOLD  ","#2 SILVER","#3 BRONZE","#4      ","#5      ","#6      "]
    mcols  = [Y+Style.BRIGHT, W+Style.BRIGHT, Y+Style.DIM, C, C, P]

    for i, item in enumerate(scored[:6]):
        pct     = f"{item['score']*100:.0f}%"
        ratio   = item["score"] / best

        print(f"  {clr(medals[i], mcols[i])}  {clr(item['title'], W + Style.BRIGHT)}")
        print(f"             {clr(item['meta'], GR)}")

        tag_str = "  ".join(
            clr(f"[{t}]", G + Style.BRIGHT) if t in item["matched"]
            else clr(f"[{t}]", GR)
            for t in item["tags"]
        )
        print(f"             {tag_str}")
        print(f"             Match: {bar(ratio, 22)}  {clr(pct, Y + Style.BRIGHT)}")
        print()

    divider()
    print(clr("  Green tags = matched your interests", G))
    print(clr("  Match % uses cosine similarity formula", GR))
    divider()

# ─── MAIN ─────────────────────────────────────────────────

def main():
    banner()
    how_it_works()

    while True:
        banner()
        cat_key  = pick_category()
        cat_data = CATALOG[cat_key]
        selected = pick_tags(cat_data)
        weights  = set_weights(selected)
        show_results(cat_data, selected, weights)

        print()
        again = input(clr("  Run again? (y / n): ", C)).strip().lower()
        if again != "y":
            print()
            print(clr("  Thank you for using NeuraMatch!", P + Style.BRIGHT))
            print(clr("  DecodeLabs | AI Project 3\n", GR))
            break

if __name__ == "__main__":
    main()
