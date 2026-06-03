import random
import copy
from systems.inventory import (
    Item, ITEM_POOL,
    HEALTH_POTION, IRON_DAGGER, IRON_SWORD
)

# Gold drop ranges per floor
GOLD_RANGES = {
    1:  (3,  10),
    2:  (5,  15),
    3:  (8,  20),
    4:  (10, 25),
    5:  (15, 35),
    6:  (20, 45),
    7:  (25, 55),
    8:  (30, 65),
    9:  (35, 80),
    10: (40, 100),
}

# Drop chance per enemy type
DROP_CHANCES = {
    "rat":          {"gold": 0.4, "item": 0.05},
    "goblin":       {"gold": 0.6, "item": 0.15},
    "skeleton":     {"gold": 0.3, "item": 0.20},
    "ashen_knight": {"gold": 0.7, "item": 0.35},
    "dark_mage":    {"gold": 0.5, "item": 0.40},
    "default":      {"gold": 0.5, "item": 0.10},
}

def roll_loot(enemy, floor_number):
    """
    Determines what an enemy drops on death.
    Returns a tuple of (gold_amount, item_or_None).
    Uses enemy type and floor number to scale drops.
    """
    chances = DROP_CHANCES.get(enemy.enemy_type, DROP_CHANCES["default"])
    gold    = 0
    item    = None

    # Roll for gold drop
    if random.random() < chances["gold"]:
        min_gold, max_gold = GOLD_RANGES.get(floor_number, (3, 10))
        gold = random.randint(min_gold, max_gold)

    # Roll for item drop
    if random.random() < chances["item"]:
        item = generate_drop(floor_number)

    return gold, item

def generate_drop(floor_number):
    """
    Generates a random item drop appropriate for the floor depth.
    Deep floors have higher chance of uncommon and rare items.
    Returns a copy of an item template — never the template itself.
    """
    # Rarity weights shift as floors increase
    if floor_number <= 3:
        weights = {"common": 0.80, "uncommon": 0.18, "rare": 0.02}
    elif floor_number <= 6:
        weights = {"common": 0.65, "uncommon": 0.28, "rare": 0.07}
    else:
        weights = {"common": 0.45, "uncommon": 0.38, "rare": 0.17}

    rarity = random.choices(
        list(weights.keys()),
        weights=list(weights.values())
    )[0]

    # Pick item category
    category = random.choice(["weapon", "armor", "consumable"])

    # Select from appropriate pool
    pool_key = f"{rarity}_{category}s"
    pool     = ITEM_POOL.get(pool_key)

    if not pool:
        # Fallback to common consumable if pool empty
        pool = [HEALTH_POTION]

    # Return a deep copy so each drop is independent
    return copy.deepcopy(random.choice(pool))

def place_floor_loot(room, floor_number, rng):
    """
    Places loot items directly on the floor of a room.
    Used for chests and pre-placed loot in special rooms.
    Returns a list of (col, row, item) tuples.
    """
    loot   = []
    count  = rng.randint(0, 2)

    walkable = [
        (col, row)
        for row in range(1, room.height - 1)
        for col in range(1, room.width  - 1)
        if room.tiles[row][col].walkable
    ]

    rng.shuffle(walkable)

    for i in range(min(count, len(walkable))):
        col, row = walkable[i]
        item     = generate_drop(floor_number)
        loot.append((col, row, item))

    return loot