# Booster pack opening

A 3D Pokémon TCG booster pack you can tip, rip open and swipe through, with holofoil card effects.
Built with [three.js](https://threejs.org) and [GSAP](https://gsap.com). Runs entirely in the browser.

## Credits

- **Holofoil effects** are ported to WebGL shaders from Simon Goellner's
  [pokemon-cards-css](https://github.com/simeydotme/pokemon-cards-css) and
  [pokemon-cards-151](https://github.com/simeydotme/pokemon-cards-151), including their foil textures.
  Those projects are licensed under GPL-3.0, so this project is too.
- **Card data and images** come from the free [TCGdex](https://tcgdex.dev) API.
- **Pull rates** default to TCGplayer's published Paldean Fates figures.
- Pokémon and all related names and artwork are © The Pokémon Company, Nintendo, Creatures and GAME FREAK.
  This is an unofficial fan project, not affiliated with or endorsed by them.

## Folder layout

```
index.html              the whole app (pack model, shaders and textures are embedded)
cards/sets.json                     list of card set folders shown in the dropdown
cards/{set_name}/manifest.json      card list with rarities (made by the script)
cards/{set_name}/*.jpg              card images (made by the script)
get_paldean_fates.py                downloads the cards from TCGdex into cards/paldean_fates/
```

## Getting the cards

Run `python3 get_paldean_fates.py` (Mac/Linux) or `py get_paldean_fates.py` (Windows) in this folder.
It saves every Paldean Fates card and a `manifest.json` into `cards/paldean_fates/` and registers the set in `cards/sets.json`.

## Card sets

Each folder in `cards/` is one set, named like `paldean_fates` (lowercase words joined by underscores).
The dropdown in the top bar lists them with underscores turned into spaces and each word capitalized,
so `paldean_fates` shows as "Paldean Fates". To add a set, put its folder (with a `manifest.json`) in `cards/`
and add the folder name to `cards/sets.json`. If `sets.json` is missing, the page falls back to the
server's directory listing of `cards/`, which works with `python3 -m http.server`.

## Running it locally

Browsers block pages opened straight from a file from reading the card manifests, so serve the folder:

```
python3 -m http.server 8000
```

then open http://localhost:8000.

## License

GPL-3.0, following the projects the holofoil effects are ported from.
