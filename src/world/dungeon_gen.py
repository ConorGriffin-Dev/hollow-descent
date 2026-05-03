import random
from world.tile import WALL, FLOOR, STAIRCASE_DOWN, STAIRCASE_UP
from world.room import Room, Exit
from world.floor import Floor, GateRequirement

# Room size bounds in tiles
ROOM_MIN_W = 8
ROOM_MAX_W = 20
ROOM_MIN_H = 6
ROOM_MAX_H = 14

# Corridor dimensions
CORRIDOR_W = 3   # width of connecting corridors

def generate_floor(floor_number, seed):
    """
    Generates a complete Floor object for the given floor number.
    Uses the seed for reproducibility — same seed = same floor.
    Each floor is a graph of connected Room objects.
    """
    rng        = random.Random(seed + floor_number)
    room_count = get_room_count(floor_number, rng)
    rooms      = {}

    # ── Step 1: Build main path with varied directions ────────────
    # The main path walks in random directions instead of always south.
    # This creates organic L, Z, and winding shapes.
    main_path_length = max(4, room_count // 2)
    main_path_ids    = []

    # Start room
    first_id = f"room_{len(rooms):03d}"
    rooms[first_id] = build_room(first_id, floor_number, rng)
    main_path_ids.append(first_id)

    for i in range(main_path_length - 1):
        parent   = rooms[main_path_ids[-1]]
        available = get_available_directions(parent)

        if not available:
            break

        # Bias toward continuing in the same direction as last step
        # but allow turns — creates more natural winding paths
        if len(main_path_ids) > 1 and rng.random() < 0.6:
            last_exit = main_path_ids[-1]
            last_room = rooms[main_path_ids[-2]]
            last_dir  = next(
                (e.direction for e in last_room.exits
                 if e.leads_to == last_exit),
                None
            )
            if last_dir and last_dir in available:
                direction = last_dir
            else:
                direction = rng.choice(available)
        else:
            direction = rng.choice(available)

        room_id          = f"room_{len(rooms):03d}"
        rooms[room_id]   = build_room(room_id, floor_number, rng)
        main_path_ids.append(room_id)
        connect_rooms(rooms[main_path_ids[-2]], rooms[room_id], direction)

    # ── Step 2: Branch off the main path ─────────────────────────
    remaining = room_count - len(main_path_ids)

    for _ in range(remaining):
        # Pick a random room from all existing rooms to branch from
        # not just the main path — creates denser graphs
        parent_id = rng.choice(list(rooms.keys()))
        parent    = rooms[parent_id]
        available = get_available_directions(parent)

        if not available:
            continue

        direction      = rng.choice(available)
        room_id        = f"room_{len(rooms):03d}"
        rooms[room_id] = build_room(room_id, floor_number, rng)
        connect_rooms(parent, rooms[room_id], direction)

    # ── Step 3: Assign room types ─────────────────────────────────
    assign_room_types(rooms, main_path_ids, rng)

    # ── Step 4: Place staircases ──────────────────────────────────
    start_id     = main_path_ids[0]
    staircase_id = main_path_ids[-1]

    place_staircase(rooms[start_id],     "staircase_up")
    place_staircase(rooms[staircase_id], "staircase_down")

    # ── Step 5: Build placeholder gate requirement ────────────────
    gate = GateRequirement(
        floor_number = floor_number,
        type         = "carry",
        description  = "The way down is sealed.",
        inscription  = "Prove your worth.",
        condition    = {},
        satisfied    = True
    )

    return Floor(
        number               = floor_number,
        rooms                = rooms,
        start_room_id        = start_id,
        staircase_room_id    = staircase_id,
        gate_requirement     = gate,
        seed                 = seed,
        player_current_room  = start_id,
    )

def get_room_count(floor_number, rng):
    """
    Returns the number of rooms for this floor.
    Higher floors have more rooms — scale from GDD.
    """
    counts = {
        1:  rng.randint(8,  10),
        2:  rng.randint(10, 12),
        3:  rng.randint(12, 14),
        4:  rng.randint(14, 16),
        5:  rng.randint(16, 18),
        6:  rng.randint(18, 20),
        7:  rng.randint(20, 23),
        8:  rng.randint(23, 26),
        9:  rng.randint(26, 29),
        10: rng.randint(30, 35),
    }
    return counts.get(floor_number, rng.randint(8, 10))

def build_room(room_id, floor_number, rng):
    """
    Builds a single Room with a random size and filled tile grid.
    All tiles start as floor — walls are placed on the border.
    """
    width  = rng.randint(ROOM_MIN_W, ROOM_MAX_W)
    height = rng.randint(ROOM_MIN_H, ROOM_MAX_H)

    # Build tile grid — walls on border, floor inside
    tiles = []
    for row in range(height):
        tile_row = []
        for col in range(width):
            if row == 0 or row == height - 1:
                tile_row.append(WALL)
            elif col == 0 or col == width - 1:
                tile_row.append(WALL)
            else:
                tile_row.append(FLOOR)
        tiles.append(tile_row)

    return Room(
        id          = room_id,
        name        = generate_room_name(floor_number, rng),
        description = "",
        room_type   = "standard",
        width       = width,
        height      = height,
        tiles       = tiles,
        exits       = [],
        visited     = False,
        first_visit = True,
    )

def connect_rooms(room_a, room_b, direction):
    """
    Creates exits between two rooms in the given direction.
    Adds exit to room_a pointing to room_b and vice versa.
    Direction is from room_a's perspective.
    """
    opposite = {
        "north": "south",
        "south": "north",
        "east":  "west",
        "west":  "east",
    }

    room_a.exits.append(Exit(
        direction  = direction,
        leads_to   = room_b.id,
        discovered = False
    ))

    room_b.exits.append(Exit(
        direction  = opposite[direction],
        leads_to   = room_a.id,
        discovered = False
    ))

def get_available_directions(room):
    """
    Returns directions that don't already have an exit.
    Prevents duplicate exits in the same direction.
    """
    used = {exit.direction for exit in room.exits}
    all_directions = {"north", "south", "east", "west"}
    return list(all_directions - used)

def assign_room_types(rooms, main_path_ids, rng):
    """
    Assigns room types based on position in the floor graph.
    Main path rooms are standard or chamber.
    Branch rooms can be secret, trap, sanctuary, or standard.
    One merchant room placed off the main path if enough rooms exist.
    """
    main_path_set = set(main_path_ids)
    merchant_placed = False

    for room_id, room in rooms.items():
        if room_id == main_path_ids[0]:
            room.room_type = "standard"   # start room always standard
            continue
        if room_id == main_path_ids[-1]:
            room.room_type = "standard"   # staircase room always standard
            continue

        if room_id in main_path_set:
            # Main path rooms — occasionally a chamber
            room.room_type = rng.choice(["standard", "standard", "chamber"])
        else:
            # Branch rooms — more variety
            if not merchant_placed and rng.random() < 0.25:
                room.room_type  = "merchant"
                merchant_placed = True
            else:
                room.room_type = rng.choice([
                    "standard", "standard",
                    "secret", "trap", "sanctuary"
                ])

def place_staircase(room, staircase_type):
    """
    Places a staircase tile in the centre of the given room.
    staircase_type is "staircase_up" or "staircase_down".
    """
    centre_col = room.width  // 2
    centre_row = room.height // 2

    if staircase_type == "staircase_down":
        room.tiles[centre_row][centre_col] = STAIRCASE_DOWN
    else:
        room.tiles[centre_row][centre_col] = STAIRCASE_UP

def generate_room_name(floor_number, rng):
    """
    Picks a random atmospheric room name appropriate
    to the floor depth. Deeper floors get darker names.
    Full name lists added in Phase 3 with story content.
    """
    early_names = [
        "The Entry Hollow",
        "The Dusty Passage",
        "The Broken Hall",
        "The Forgotten Chamber",
        "The Stone Corridor",
        "The Collapsed Gallery",
        "The Dim Antechamber",
        "The Crumbling Vault",
    ]

    deep_names = [
        "The Ashen Gallery",
        "The Veil Chamber",
        "The Sunken Hall",
        "The Hollow Throne",
        "The Shattered Keep",
        "The Dark Vestibule",
        "The Bone Repository",
        "The Drowned Passage",
        "The Pale Corridor",
        "The Final Approach",
    ]

    names = deep_names if floor_number >= 5 else early_names
    return rng.choice(names)