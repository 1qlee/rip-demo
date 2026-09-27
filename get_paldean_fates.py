# Downloads every Paldean Fates card image + rarity from the free tcgdex API
# into a folder the booster prototype can load.
#
# Run it on your own computer (needs Python 3, nothing else):
#   Mac:      open Terminal, cd to this file's folder, run   python3 get_paldean_fates.py
#   Windows:  open Command Prompt, cd to this file's folder, run   py get_paldean_fates.py
#
# It creates a folder "paldean_fates_cards" with the card images and a manifest.json.
# Then open the prototype, click "Load cards" and choose that folder.

import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

SET_ID = "sv04.5"
API = "https://api.tcgdex.net/v2/en"
OUT = "cards"
HEADERS = {"User-Agent": "booster-prototype/1.0 (personal project)"}


def get(url, binary=False, tries=3):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:
            if attempt == tries - 1:
                print(f"  failed: {url} ({e})")
                return None
            time.sleep(1.5 * (attempt + 1))


def fetch_card(brief):
    card = get(f"{API}/cards/{brief['id']}")
    if not card:
        return None
    image = card.get("image") or brief.get("image")
    if not image:
        print(f"  no image for {brief['id']} {brief.get('name')}")
        return None
    filename = f"{card['id']}.jpg"
    path = os.path.join(OUT, filename)
    if not os.path.exists(path):
        img = get(f"{image}/high.jpg", binary=True)
        if not img:
            return None
        with open(path, "wb") as f:
            f.write(img)
    return {
        "id": card["id"],
        "name": card.get("name"),
        "number": card.get("localId"),
        "rarity": card.get("rarity"),
        "category": card.get("category"),
        "stage": card.get("stage"),
        "file": filename,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Fetching set list...")
    s = get(f"{API}/sets/{SET_ID}")
    if not s:
        sys.exit("Couldn't reach the tcgdex API. Check your internet connection and try again.")
    briefs = s.get("cards", [])
    print(f"{len(briefs)} cards in {s.get('name')}. Downloading (this takes a minute or two)...")
    cards, done = [], 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(fetch_card, briefs):
            done += 1
            if result:
                cards.append(result)
            if done % 20 == 0 or done == len(briefs):
                print(f"  {done}/{len(briefs)}")
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"set": s.get("name"), "cards": cards}, f, indent=1, ensure_ascii=False)
    rarities = {}
    for c in cards:
        rarities[c["rarity"]] = rarities.get(c["rarity"], 0) + 1
    print(f"\nDone: {len(cards)} cards saved to '{OUT}'.")
    for r, n in sorted(rarities.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {r}")


if __name__ == "__main__":
    main()
