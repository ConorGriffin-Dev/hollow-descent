# The Hollow Descent — Technical Design Document

## Architecture Overview

The game is separated into distinct layers. Each layer has one
responsibility and communicates only through GameState.

main.py
│
├── GameLoop
│      ├── InputHandler        reads keypress, returns Action
│      ├── ActionResolver      takes Action, updates GameState
│      └── Renderer            reads GameState, draws via Pygame
│
├── GameState                  single source of truth
│      ├── Player
│      ├── CurrentFloor
│      └── FloorCache
│
└── Systems
├── DungeonGenerator
├── CombatSystem
├── PathfindingSystem
├── LootSystem
├── GateSystem
├── AnimationSystem
└── SaveSystem

Core principle: GameState is the single source of truth. Every system
reads from and writes to GameState only. The Renderer reads GameState and
draws. It never modifies anything.

---

## Technology Stack

| Property | Value |
|----------|-------|
| Language | Python 3.13 |
| Renderer | Pygame 2.x |
| Tile Size | 32×32 pixels |
| Asset Format | PNG spritesheets |
| Testing | pytest |
| Version Control | Git + GitHub |
| Save Format | JSON |
| Distribution | PyInstaller |

---

## Folder Structure
hollow-descent/
│
├── docs/
│   ├── GDD.md
│   ├── TDD.md
│   └── CHANGELOG.md
│
├── src/
│   ├── main.py
│   │
│   ├── engine/
│   │   ├── init.py
│   │   ├── game_loop.py
│   │   ├── game_state.py
│   │   ├── input_handler.py
│   │   ├── action_resolver.py
│   │   ├── renderer.py
│   │   └── constants.py
│   │
│   ├── world/
│   │   ├── init.py
│   │   ├── floor.py
│   │   ├── room.py
│   │   ├── tile.py
│   │   ├── dungeon_gen.py
│   │   ├── exit_discovery.py
│   │   └── gate_system.py
│   │
│   ├── entities/
│   │   ├── init.py
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── behaviors.py
│   │   └── npc.py
│   │
│   ├── systems/
│   │   ├── init.py
│   │   ├── combat.py
│   │   ├── pathfinding.py
│   │   ├── inventory.py
│   │   ├── loot.py
│   │   ├── enhancements.py
│   │   ├── animation.py
│   │   └── save_system.py
│   │
│   └── data/
│       (files added as needed)
│
├── assets/
│   ├── tilesets/
│   ├── sprites/
│   └── fonts/
│
├── tests/
│   ├── test_combat.py
│   ├── test_dungeon_gen.py
│   ├── test_pathfinding.py
│   ├── test_inventory.py
│   └── test_gate_system.py
│
├── saves/
│   └── .gitkeep
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

---

## Data Structures

### Tile
```python
@dataclass
class Tile:
    type: str           # "wall" "floor" "door" "staircase_down"
                        # "staircase_up" "chest_closed" "chest_open"
    walkable: bool
    blocks_sight: bool
```

### Exit
```python
@dataclass
class Exit:
    direction: str      # "north" "south" "east" "west"
    leads_to: str       # room_id of destination
    discovered: bool = False
```

### Room
```python
@dataclass
class Room:
    id: str
    name: str
    description: str
    room_type: str      # "standard" "chamber" "merchant" "secret"
                        # "trap" "sanctuary" "boss_arena"
    width: int
    height: int
    tiles: List[List[Tile]]
    exits: List[Exit]
    enemies: List[Enemy]
    items: List[Item]
    visited: bool = False
    first_visit: bool = True
    enemies_cleared: bool = False
    special_state: Dict = field(default_factory=dict)
```

### Floor
```python
@dataclass
class Floor:
    number: int
    rooms: Dict[str, Room]
    start_room_id: str
    staircase_room_id: str
    gate_requirement: GateRequirement
    seed: int
    player_current_room: str
```

### GateRequirement
```python
@dataclass
class GateRequirement:
    floor_number: int
    type: str           # "carry" "speak" "defeat" "solve"
                        # "knowledge" "sacrifice" "sequence"
    description: str
    inscription: str
    condition: Dict
    satisfied: bool = False
```

### Player
```python
@dataclass
class Player:
    name: str = "Vincent"
    level: int = 1
    hp: int = 100
    max_hp: int = 100
    atk: int = 5
    def_: int = 2
    spd: int = 10
    lck: int = 5
    xp: int = 0
    xp_next: int = 100
    gold: int = 0
    col: int = 1
    row: int = 1
    current_floor: int = 1
    inventory: List[Item] = field(default_factory=list)
    inventory_cap: int = 12
    equipped: Dict[str, Optional[Item]] = field(default_factory=dict)
    story_items: List[Item] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    enhancements: List[str] = field(default_factory=list)
    playstyle_counters: Dict[str, int] = field(default_factory=dict)
    status_effects: List = field(default_factory=list)
```

### Enemy
```python
@dataclass
class Enemy:
    id: str
    name: str
    enemy_type: str     # see Enemy Type System below
    hp: int
    max_hp: int
    atk: int
    def_: int
    spd: int
    xp_reward: int
    col: int = 0
    row: int = 0
    alive: bool = True
    behavior: str       # "aggressive" "ranged" "patrol" etc
    behavior_state: Dict = field(default_factory=dict)
    special_ability: Optional[str] = None
    ability_cooldown: int = 0
    drop_table: List = field(default_factory=list)
```

### Boss (extends Enemy)
```python
@dataclass
class Boss(Enemy):
    phase: int = 1
    phase_thresholds: List[int] = field(default_factory=list)
    # HP values at which the boss changes phase, e.g. [200, 100]

    def update_phase(self):
        """Returns True if a phase threshold was crossed this hit."""
        for i, threshold in enumerate(self.phase_thresholds):
            if self.hp <= threshold and self.phase <= i + 1:
                self.phase = i + 2
                return True
        return False
```

### Item
```python
@dataclass
class Item:
    id: str
    true_name: str
    mystery_name: str
    category: str       # "weapon" "armor" "consumable"
                        # "material" "story"
    identified: bool = False
    rarity: str = "common"
    quantity: int = 1
    cursed: bool = False
    lore: str = ""
    damage_dice: str = ""
    atk_bonus: int = 0
    def_bonus: int = 0
    slot: str = ""
    effect: str = ""
    effect_value: int = 0
    is_story_item: bool = False
    floor_col: int = 0
    floor_row: int = 0
```

### GameState
```python
@dataclass
class GameState:
    player: Player
    current_floor: Floor
    floor_cache: Dict[int, Floor]   # floor_number → Floor
    run_seed: int = 0
    turn_count: int = 0
    game_phase: str = "exploring"
    # "exploring" "combat" "merchant" "gate" "transition"
    # "story" "game_over"
    messages: List[str] = field(default_factory=list)
    story_message: Optional[str] = None
    flags: Dict[str, bool] = field(default_factory=dict)
    # flags tracks story state across the entire run
    # e.g. flags["hologram_found"] = True
    #      flags["megath_met"] = True
    #      flags["francis_freed"] = False
    inventory_open: bool = False
    inventory_selected: int = 0
    merchant_open: bool = False
    merchant_selected: int = 0
```

---

## Enemy Type System

Enemies are categorised into tiers that map to floor depth. The
`enemy_type` field on each Enemy keys into colour, stats, and behaviour.

| Tier | Enemy Types | Floors |
|------|-------------|--------|
| Tier 1 | Bugs & Glitches — feral, mindless corrupted code, starting fodder | 1–2 |
| Tier 2 | The Flickering (hostile, Aruki-controlled) & low-level Fractured | 3–5 |
| Tier 3 | The Hollow Guard & named Fractured warriors | 6–8 |
| Tier 4 | All enemy types converge | 9–10 |

Faction origins of enemy types:
- **Bugs / Glitches** — corrupted code, no faction, baseline fodder.
- **The Flickering** — Eternal Court; ensnared, mostly hostile.
- **The Hollow Guard** — Eternal Court; pure AI muscle, attack on sight.
- **The Fractured** — The Bound; shattered minds, hostile by instinct, named ones carry backstory.
- **The Crowned Few** — Eternal Court; boss-tier elite.

### Boss Roster (multi-floor, draft)

| Floor | Boss | Notes |
|-------|------|-------|
| 2 | The Swarmcluster | Fused mass of bugs/glitches. Teaches boss mechanics. |
| 3 | The First Fractured | First named Fractured. Tragic intro. |
| 4 | Warden of the Flickering | Corrupted Flickering, dark mirror of Luma. |
| 5 | The Hollowed General | First Hollow Guard commander. |
| 6 | The Choir of the Fractured | Several named Fractured fought together. |
| 7 | The Gatekeeper | Massive Hollow Guard construct. |
| 8 | First Crowned Few | Defeat triggers Aruki's direct manifestation. |
| 9 | The Crowned Few who took Francis | The father beat. |
| 10 | Aruki's Avatar / guardian | Final barrier. Full Aruki reserved for sequel. |

Boss assignment is data-driven via a `BOSS_FLOORS` set in the dungeon
generator. Boss rooms replace the staircase room with a sealed arena.
Final per-floor boss selection is locked during narrative integration.

---

## Key Algorithms

### Room Graph Generation
Decide room count for this floor number
Generate guaranteed path from START to STAIRCASE
Branch off main path — dead ends, loops, optional wings
Assign room types to all rooms
Spawn enemies and place chests/merchants per room
Place gate requirement item/trigger in a reachable room
Place staircases

### A* Pathfinding
Contained entirely within one room's tile grid. Enemies never cross
room boundaries. Runs per enemy per turn. Room size cap means
near-instant computation even with many enemies.
open_set    = {start}
came_from   = {}
g_score     = {start: 0}
f_score     = {start: heuristic(start, goal)}
while open_set is not empty:
current = node in open_set with lowest f_score
if current == goal: return reconstruct_path()
for each walkable neighbour:
tentative_g = g_score[current] + 1
if tentative_g < g_score[neighbour]:
came_from[neighbour] = current
g_score[neighbour] = tentative_g
f_score[neighbour] = tentative_g + heuristic(neighbour, goal)

Heuristic: Chebyshev distance (accounts for diagonal movement on grid).

### Exit Discovery
Runs every player move. Checks distance from player to each
undiscovered exit tile in the current room.

```python
DISCOVERY_RADIUS = 2

def check_exit_discovery(player, room):
    for exit in room.exits:
        if exit.discovered:
            continue
        exit_pos = get_exit_position(room, exit.direction)
        distance = chebyshev_distance(player_pos, exit_pos)
        if distance <= DISCOVERY_RADIUS:
            exit.discovered = True
```

### Enemy Stat Scaling
Enemy base stats are multiplied by a per-floor factor so encounters
grow tougher with depth.

```python
FLOOR_SCALING = {
    1: 1.0,  2: 1.1,  3: 1.25, 4: 1.4,  5: 1.6,
    6: 1.8,  7: 2.0,  8: 2.3,  9: 2.6, 10: 3.0,
}

def scale_stat(base, floor_number):
    return max(1, int(base * FLOOR_SCALING.get(floor_number, 1.0)))
```

### Combat Resolution
```python
def resolve_attack(attacker, defender):
    base   = roll_dice(attacker.weapon.damage_dice)
    total  = base + attacker.atk
    damage = max(1, total - defender.def_)
    if random.random() < attacker.lck * 0.01:
        damage *= 2
    defender.hp -= damage
    return defender.hp <= 0
```

### Gate Validation
Runs when Vincent interacts with a sealed staircase.
Checks condition dict against current GameState.

```python
def check_gate(player, floor):
    req = floor.gate_requirement
    if req.type == "carry":
        req.satisfied = any(
            item.id == req.condition["item_id"]
            for item in player.story_items + player.inventory
        )
    elif req.type == "defeat":
        req.satisfied = floor.special_state.get(
            f"{req.condition['enemy_id']}_defeated", False
        )
    elif req.type == "speak":
        req.satisfied = handle_spoken_gate(player, req)
    elif req.type == "sacrifice":
        req.satisfied = handle_sacrifice(player, req)
    elif req.type == "knowledge":
        req.satisfied = handle_knowledge_gate(player, req)
    elif req.type == "sequence":
        req.satisfied = check_sequence(player, floor, req)
    return req.satisfied
```

### Floor Persistence
```python
def leave_floor(game_state, direction):
    floor = game_state.current_floor
    game_state.floor_cache[floor.number] = floor

    next_number = floor.number + (1 if direction == "down" else -1)

    if next_number in game_state.floor_cache:
        next_floor = game_state.floor_cache[next_number]
    else:
        next_floor = generate_floor(next_number, game_state.run_seed)

    game_state.current_floor = next_floor
```

On load from save, cleared rooms respawn 60% of their original enemy
count; survivors are untouched.

### Procedural Item Generation
```python
def generate_drop(floor_number):
    rarity   = roll_rarity(floor_number)   # weights shift with depth
    category = random.choice(["weapon", "armor", "consumable"])
    template = pick_from_pool(rarity, category)
    return copy.deepcopy(template)
```

### Dynamic Build Weighting
```python
def get_perk_options(player):
    counters = player.playstyle_counters
    total    = sum(counters.values()) or 1
    weights  = {k: v / total for k, v in counters.items()}
    options  = [
        pick_perk("blade",    weights.get("blade_actions",    0)),
        pick_perk("residual", weights.get("residual_actions", 0)),
        pick_perk("shadow",   weights.get("shadow_actions",   0)),
    ]
    random.shuffle(options)
    return options[:3]
```

---

## Pygame Renderer

### Window Layout
┌─────────────────────────────────┬──────────────────────┐
│                                 │  The Hollow Descent  │
│                                 │  ──────────────────  │
│                                 │  Vincent   Floor 4   │
│         ROOM VIEWPORT           │  HP ███████░░ 67/100 │
│         32×32 tiled sprites     │  XP ████░░░░░ 45/150 │
│                                 │  ──────────────────  │
│                                 │  ATK 11  DEF  6      │
│                                 │  SPD 10  LCK  5      │
│                                 │  Gold    83          │
│                                 │  ──────────────────  │
│                                 │  MINIMAP             │
│                                 │  ──────────────────  │
│                                 │  INVENTORY  7/12     │
├─────────────────────────────────┴──────────────────────┤
│ > You enter The Ashen Gallery.                          │
│ > A passage opens to the north.                         │
└────────────────────────────────────────────────────────┘
### Rendering Pipeline (per frame)
Fill background
Draw room tile grid (floor, walls, doors, exits, chests)
Draw items on floor
Draw merchant if present
Draw enemies with current animation frame
Draw Vincent with current animation frame
Draw UI panels — sidebar, minimap, inventory, message log
Draw overlays — inventory screen, merchant screen, game over
pygame.display.flip()

### Animation System
Sprite sheets contain multiple frames per state.
Frame selected by: `(pygame.time.get_ticks() // frame_ms) % frame_count`

States    idle
walk_north / walk_south / walk_east / walk_west
attack
death

Animation system is deferred until the asset pack is selected.

---

## Game Loop

```python
FPS   = 60
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            handle_input(event, game_state)

    renderer.draw(screen, game_state)
    pygame.display.flip()
    clock.tick(FPS)
```

---

## Data Flow — Single Player Turn
handle_input(keypress, game_state)
↓ movement, combat, or interaction
Player acts — move / attack / use item / interact
↓ modifies game_state
Enemy turns — each living enemy in room acts
↓ A* toward player, attack if adjacent
↓ modifies game_state
Gate / staircase check
↓ validate gate if at staircase
↓ transition floor if descending/ascending
Condition check
↓ CONTINUE | PLAYER_DEAD | FLOOR_COMPLETE | GAME_WON
Renderer.draw(screen, game_state)

---

## Save File Schema

```json
{
  "version": "0.1.0",
  "run_seed": 847291,
  "turn_count": 412,
  "game_phase": "exploring",
  "current_floor_number": 4,
  "player": {
    "name": "Vincent",
    "level": 4,
    "hp": 67,
    "max_hp": 115,
    "atk": 11,
    "def_": 6,
    "spd": 10,
    "lck": 5,
    "xp": 45,
    "xp_next": 150,
    "gold": 83,
    "col": 5,
    "row": 4,
    "current_floor": 4,
    "inventory_cap": 12,
    "abilities": [],
    "enhancements": [],
    "playstyle_counters": {
      "blade_actions": 34,
      "residual_actions": 18,
      "shadow_actions": 7
    },
    "inventory": [],
    "story_items": [],
    "equipped": {
      "weapon": null,
      "helmet": null,
      "chest": null,
      "gloves": null,
      "boots": null
    },
    "status_effects": []
  },
  "floors": {
    "1": {},
    "2": {},
    "3": {},
    "4": {}
  },
  "flags": {
    "hologram_found": false,
    "megath_met": false,
    "francis_freed": false
  },
  "messages": [],
  "story_message": null
}
```

---

## Testing Strategy

| Test File | What It Covers |
|-----------|---------------|
| test_combat.py | Damage formula, crit rolls, death detection, edge cases |
| test_dungeon_gen.py | Floor always completable, room count correct, gate item placeable |
| test_pathfinding.py | A* finds valid path, handles no-path gracefully, walls respected |
| test_inventory.py | Cap enforcement, stacking rules, story item slot rules |
| test_gate_system.py | Each gate type satisfies correctly, staircase locks/unlocks |

Core rule: Every bug found during development gets a regression test
written before the fix. If it broke once it gets a test so it never
breaks again.

---

## Requirements
pygame==2.6.1
pytest==9.0.3
pyinstaller
`requirements.txt` is the single source of truth for dependencies.
Virtual environment is always activated before development sessions.