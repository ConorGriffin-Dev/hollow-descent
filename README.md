# The Hollow Descent

> A cyberpunk roguelike dungeon crawler.
> Descend ten floors. Prove your worthiness.
> Find your father.

---

## What Is This

The Hollow Descent is a Pygame-based roguelike dungeon crawler built in Python.
You play as Vincent, a sixteen-year-old who opens a program through his neural
link and is locked inside the Gyrus Tunnel — a ten-floor proving ground between
reality and Cyberspace — searching for a father who vanished into the network
eleven years ago. Each floor is a network of self-contained rooms explored one
at a time. Every floor is sealed until you find and satisfy its unique
requirement, forcing genuine exploration before descent. Combat is turn-based,
death is permanent, and every run is procedurally generated.

---

## Status

> In active development. Core engine and systems complete; story content in progress.

Playable: procedural floors, turn-based combat, enemy AI, inventory,
equipment, loot, chests, merchants, save/load, and floor transitions
are all implemented.

---

## Installation

Requires Python 3.13

```bash
git clone https://github.com/YoungGriff11/hollow-descent
cd hollow-descent
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
python src/main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| WASD / Arrow keys | Move |
| G | Pick up item |
| F | Open chest |
| M | Trade with merchant |
| I | Open / close inventory |
| Arrow keys (in inventory) | Navigate items |
| U | Use selected item |
| E | Equip selected item |
| D | Drop selected item |
| F5 | Save game |
| ESC | Close menu / quit on game over |

---

## Roadmap

- [x] Phase 1 — Core engine, room rendering, movement, combat
- [x] Phase 2 — Floor persistence, backtracking, inventory, save/load, merchants
- [ ] Phase 3 — Story, factions, characters, neural enhancements, bosses, endings
- [ ] Phase 4 — Sprites, animation, audio, polish, release

---

## Built With

Python 3.13 · Pygame 2.6 · pytest · PyInstaller

---

## License

MIT License — see LICENSE for details.