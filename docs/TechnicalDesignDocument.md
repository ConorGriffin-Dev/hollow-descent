The Hollow Descent — Technical Design Document

Architecture Overview

The game is separated into distinct layers. Each layer has one
responsibility and communicates only through GameState.

```
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
```

Core principle: GameState is the single source of truth. Every system
reads from and writes to GameState only. The Renderer reads GameState and
draws. It never modifies anything.

---

Technology Stack

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Renderer | Pygame 2.x |
| Tile Size | 32×32 pixels |
| Asset Format | PNG spritesheets |
| Testing | pytest |
| Version Control | Git + GitHub |
| Save Format | JSON |

---

Folder Structure

```
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
│   │   ├── __init__.py
│   │   ├── game_loop.py
│   │   ├── game_state.py
│   │   ├── input_handler.py
│   │   ├── action_resolver.py
│   │   └── renderer.py
│   │
│   ├── world/
│   │   ├── __init__.py
│   │   ├── floor.py
│   │   ├── room.py
│   │   ├── tile.py
│   │   ├── dungeon_gen.py
│   │   ├── exit_discovery.py
│   │   └── gate_system.py
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── behaviors.py
│   │   └── npc.py
│   │
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── combat.py
│   │   ├── pathfinding.py
│   │   ├── inventory.py
│   │   ├── loot.py
│   │   ├── magic.py
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
```

---

Data Structures

 Tile
```python
@dataclass
class Tile:
    type: str           # "wall" "floor" "door" "exit" "staircase"
    sprite_key: str     # key into sprite atlas
    walkable: bool
    blocks_sight: bool
```

 Exit
```python
@dataclass
class Exit:
    direction: str      # "north" "south" "east" "west"
    leads_to: str       # room_id of destination
    discovered: bool = False
```

 Room
```python
@dataclass
class Room:
    id: str
    name: str
    description: str
    room_type: str      # "standard" "corridor" "chamber" etc
    width: int
    height: int
    tiles: List[List[Tile]]
    exits: List[Exit]
    enemies: List[Enemy]
    items: List[Item]
    story_item: Optional[StoryItem]
    visited: bool = False
    first_visit: bool = True
    enemies_cleared: bool = False
    special_state: Dict = field(default_factory=dict)
```

 Floor
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

 GateRequirement
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

 Player
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
    xp_to_next: int = 100
    gold: int = 0
    position: Tuple[int, int] = (0, 0)
    current_room_id: str = ""
    current_floor: int = 1
    inventory: List[Item] = field(default_factory=list)
    inventory_cap: int = 12
    equipped: Dict[str, Optional[Item]] = field(default_factory=dict)
    story_items: List[StoryItem] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    oaths_sworn: List[str] = field(default_factory=list)
    playstyle_counters: Dict[str, int] = field(default_factory=dict)
    status_effects: List[StatusEffect] = field(default_factory=list)
```

 Enemy
```python
@dataclass
class Enemy:
    id: str
    name: str
    sprite_key: str
    hp: int
    max_hp: int
    atk: int
    def_: int
    spd: int
    xp_reward: int
    drop_table: List[DropEntry]
    behavior: str       # "aggressive" "ranged" "patrol" etc
    position: Tuple[int, int] = (0, 0)
    alive: bool = True
    special_ability: Optional[str] = None
    ability_cooldown: int = 0
    behavior_state: Dict = field(default_factory=dict)
```

 Item
```python
@dataclass
class Item:
    id: str
    true_name: str
    mystery_name: str
    category: str       # "weapon" "armor" "consumable" "material"
    identified: bool = False
    rarity: str = "common"
    stats: Dict = field(default_factory=dict)
    effect: Optional[str] = None
    cursed: bool = False
    lore: str = ""
    quantity: int = 1
```

 StoryItem
```python
@dataclass
class StoryItem:
    id: str
    name: str
    description: str
    floor_found: int
    lore: str
    gameplay_effect: str
    collected: bool = False
    counts_toward_cap: bool = True
    # counts_toward_cap becomes False after second oath
```

 GameState
```python
@dataclass
class GameState:
    player: Player
    current_floor: Floor
    floor_cache: Dict[int, Floor]   # floor_number → Floor
    run_seed: int
    turn_count: int = 0
    game_phase: str = "exploring"
    # "exploring" "combat" "merchant" "gate" "transition" "game_over"
    message_log: List[str] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    # flags tracks story state across the entire run
    # e.g. flags["journal_found"] = True
    #      flags["voryn_spoke"] = True
    #      flags["veil_weakened"] = False
```

---

Key Algorithms

 BSP Room Graph Generation
```
1. Decide room count for this floor number
2. Generate guaranteed path from START to STAIRCASE
3. Branch off main path — dead ends, loops, optional wings
4. Assign room types to all rooms
5. Place gate requirement item/trigger in a reachable room
6. Validate — every room reachable, gate item placeable
7. If validation fails, regenerate with incremented seed
```

 A* Pathfinding
Contained entirely within one room's tile grid. Enemies never cross
room boundaries. Runs per enemy per turn. Room size cap of roughly
40×20 tiles means near-instant computation even with many enemies.

```
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
```

Heuristic: Chebyshev distance (accounts for diagonal movement on grid).

 Exit Discovery
Runs every player move. Checks distance from player to each
undiscovered exit tile in the current room.

```python
DISCOVERY_RADIUS = 2        # standard
READER_RADIUS    = 5        # with Perception ability active

def check_exit_discovery(player, room):
    radius = READER_RADIUS if "perception" in player.abilities \
             else DISCOVERY_RADIUS
    for exit in room.exits:
        if exit.discovered:
            continue
        exit_pos = get_exit_tile_position(room, exit.direction)
        distance = chebyshev_distance(player.position, exit_pos)
        if distance <= radius:
            exit.discovered = True
            add_message(f"You notice a passage to the {exit.direction}.")
```

 Combat Resolution
```python
def resolve_attack(attacker, defender):
    base   = roll_dice(attacker.weapon.damage_dice)
    total  = base + attacker.atk
    damage = max(1, total - defender.def_)
    if random.random() < attacker.lck * 0.01:
        damage *= 2
        add_message("Critical hit!")
    defender.hp -= damage
    return defender.hp <= 0  # returns True if defender dies
```

 Gate Validation
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

 Floor Persistence
```python
def leave_floor(game_state, direction):
    floor = game_state.current_floor
    game_state.floor_cache[floor.number] = serialize_floor(floor)

    next_number = floor.number + (1 if direction == "down" else -1)

    if next_number in game_state.floor_cache:
        next_floor = deserialize_floor(game_state.floor_cache[next_number])
        respawn_enemies(next_floor)     # respawn 60% of dead enemies
    else:
        next_floor = generate_floor(next_number, game_state.run_seed)

    game_state.current_floor = next_floor
```

 Procedural Item Generation
```python
def generate_item(floor_number, rarity):
    base      = random.choice(get_items_for_floor(floor_number, rarity))
    quality   = roll_quality(floor_number)
    stats     = roll_stats(base, quality)
    cursed    = random.random() < curse_chance(floor_number)
    mystery   = generate_mystery_name(base.category)
    return Item(
        id           = base.id,
        true_name    = build_true_name(quality, base, stats),
        mystery_name = mystery,
        identified   = False,
        stats        = stats,
        cursed       = cursed,
        lore         = base.lore_template
    )
```

 Dynamic Build Weighting
```python
def get_perk_options(player):
    counters  = player.playstyle_counters
    total     = sum(counters.values()) or 1
    weights   = {k: v / total for k, v in counters.items()}
    options   = [
        pick_perk("blade",  weights.get("blade_actions",  0)),
        pick_perk("reader", weights.get("reader_actions", 0)),
        pick_perk("shadow", weights.get("shadow_actions", 0)),
    ]
    random.shuffle(options)
    return options[:3]
```

---

Pygame Renderer

 Window Layout
```
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
│                                 │  [■]                 │
│                                 │   │                  │
│                                 │  [■]─[▶]             │
│                                 │  ──────────────────  │
│                                 │  INVENTORY  7/12     │
├─────────────────────────────────┴──────────────────────┤
│ > You enter The Ashen Gallery. Portraits line the walls │
│ > A passage opens to the north.                        │
│ > The Ashen Knight turns slowly to face you.           │
└────────────────────────────────────────────────────────┘
```

 Rendering Pipeline (per frame)
```
1. Fill background
2. Draw room tile grid (floor, walls, doors, exits)
3. Draw items on floor
4. Draw enemies with current animation frame
5. Draw Vincent with current animation frame
6. Draw UI panels — sidebar, minimap, inventory, message log
7. pygame.display.flip()
```

 Animation System
Sprite sheets contain multiple frames per state.
Frame selected by: `(pygame.time.get_ticks() // frame_ms) % frame_count`

```
States    idle
          walk_north / walk_south / walk_east / walk_west
          attack
          death
```

---

Game Loop

```python
FPS   = 60
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            action = input_handler.map(event.key)
            if action:
                action_resolver.resolve(action, game_state)

    animation_system.update(game_state)
    renderer.draw(screen, game_state)
    pygame.display.flip()
    clock.tick(FPS)
```

---

Data Flow — Single Player Turn

```
1. InputHandler.map(keypress)
        ↓ returns Action object

2. ActionResolver.resolve(action, game_state)
        ↓ modifies game_state
        ↓ returns list of Events

3. EnemySystem.take_turns(game_state)
        ↓ each living enemy in room acts
        ↓ modifies game_state

4. GateSystem.check(game_state)
        ↓ if Vincent is at staircase, validate gate
        ↓ modifies gate_requirement.satisfied

5. GameState.check_conditions()
        ↓ returns CONTINUE | PLAYER_DEAD | FLOOR_COMPLETE | GAME_WON

6. AnimationSystem.update(game_state)

7. Renderer.draw(screen, game_state)
```

---

Save File Schema

```json
{
  "version": "0.1.0",
  "run_seed": 847291,
  "turn_count": 412,
  "player": {
    "name": "Vincent",
    "level": 4,
    "hp": 67,
    "max_hp": 115,
    "atk": 11,
    "def": 6,
    "spd": 10,
    "lck": 5,
    "xp": 45,
    "xp_to_next": 150,
    "gold": 83,
    "inventory_cap": 12,
    "abilities": ["perception", "resonance"],
    "oaths_sworn": [],
    "playstyle_counters": {
      "blade_actions": 34,
      "reader_actions": 18,
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
  "current_floor_number": 4,
  "game_phase": "exploring",
  "floor_cache": {
    "1": {},
    "2": {},
    "3": {}
  },
  "flags": {
    "journal_found": false,
    "veil_weakened": false
  },
  "message_log": []
}
```

---

Testing Strategy

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

Requirements

```
pygame==2.5.2
pytest==8.0.0
```

`requirements.txt` is the single source of truth for dependencies.
Virtual environment is always activated before development sessions.