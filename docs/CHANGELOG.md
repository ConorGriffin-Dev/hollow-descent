# Changelog

All notable changes to The Hollow Descent will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed — Cyberpunk Reskin
- Full genre pivot from dark fantasy to cyberpunk. Emotional spine,
  relationships, faction structure, and ending architecture unchanged —
  only setting and flavour.
- The Underspire renamed to **The Gyrus Tunnel**.
- Overworld → **Reality**; Underworld → **Cyberspace**.
- Reader ability **removed** — Vincent is special because he shares
  Francis's neural signature.
- Magic system replaced by the **Neural Enhancement** system.
- Godqueen → **Aruki**; the Cleric → **Megath**.
- Factions replaced with **The Bound**, **The Eternal Court**, and
  **The Guild**. The Veilborn removed entirely.
- Enemies reframed — rats/goblins → **bugs/glitches**, plus faction-based
  enemy tiers (The Flickering, The Hollow Guard, The Fractured, The Crowned Few).
- GDD and TDD rewritten for the cyberpunk setting.

### Planned
- Apply cyberpunk renames across the codebase.
- Implement enemy type system reflecting the Enemy Bible tiers.
- Add named NPCs (Luma, Megath) and multi-floor bosses.
- Build the neural enhancement system replacing magic.
- Integrate floor-by-floor story beats and dialogue.

---

## Version History

## [0.2.0] — Phase 2: Items, Inventory, Save, Merchant

### Added
- Item data structure supporting weapons, armor, consumables,
  materials, and story items with an identification system.
- Loot drops from enemies — gold and items, scaled by floor depth.
- Items rendered on the floor; pickup with G.
- 12-slot inventory with a full overlay screen (navigate, use, equip, drop).
- Consumable stacking up to 5 per slot.
- Equipment system — weapons change damage dice, armor changes DEF;
  equipped items shown in sidebar and tagged in inventory.
- Save and load system using JSON; auto-save on floor descent, manual
  save with F5, auto-load on launch.
- Start screen with New Game and Continue options.
- Random seed per run for unique procedural floors.
- Chest system — chests placed in rooms, opened with F, drop gold and items.
- Partial enemy respawn (60%) in cleared rooms on backtracking.
- Merchant rooms — merchant NPC, shop screen, buy system.
- Enemy stat scaling by floor depth.
- Rooms-discovered counter in sidebar.

### Fixed
- Room types correctly assigned before enemy spawning.
- staircase_id defined before use in floor generation.
- Game over correctly halts input and enemy turns.
- Staircase ascent/descent variable scoping crash.
- Save/load tile deserialization (removed invalid sprite_key argument).
- Consumable stack cap enforced on pickup at 5.
- Chest loot placed on walkable tiles so it can be retrieved.
- Input ordering so non-movement keys (G, F, H, F5, I) fire correctly.

## [0.1.0] — Phase 1: Core Engine

### Added
- Project structure, GDD, TDD, README, CHANGELOG, .gitignore, LICENSE.
- Environment setup — Python 3.13, Pygame, pytest, virtual environment.
- constants.py as the single source of truth for config and colours.
- Tile, Room, Exit, and Floor data structures.
- Player entity with stats, movement, and sidebar rendering.
- GameState as the single source of truth.
- Procedural floor generation — room graph with a main path and branches,
  room types, scaling room counts per floor.
- Room-by-room rendering (no camera/viewport).
- WASD/arrow key movement with wall and enemy collision.
- Minimap that builds from exploration — blank until walked, exits only
  shown once discovered.
- Combat system — turn-based, dice-based damage, crits, XP, level ups.
- Enemy entities with floor-based factory functions.
- Enemy AI — A* pathfinding, aggressive and coward behaviors, enemy turns.
- Floor transitions — descending and ascending staircases, floor cache.
- Game over screen on death.

---