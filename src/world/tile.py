# Tile is the smallest unit of the dungeon.
# Every room is a 2D grid of Tile objects.

from dataclasses import dataclass

@dataclass
class Tile:
    type: str           # "wall" "floor" "door" "exit" "staircase"
    walkable: bool      # whether the player/enemies can move onto this tile
    blocks_sight: bool  # whether this tile blocks line of sight

# Pre-built tile types — used by the dungeon generator
# instead of creating new Tile objects every time

WALL = Tile(
    type="wall",
    walkable=False,
    blocks_sight=True
)

FLOOR = Tile(
    type="floor",
    walkable=True,
    blocks_sight=False
)

DOOR = Tile(
    type="door",
    walkable=True,
    blocks_sight=True
)

STAIRCASE_DOWN = Tile(
    type="staircase_down",
    walkable=True,
    blocks_sight=False
)

STAIRCASE_UP = Tile(
    type="staircase_up",
    walkable=True,
    blocks_sight=False
)

CHEST_CLOSED = Tile(
    type         = "chest_closed",
    walkable     = False,
    blocks_sight = False
)

CHEST_OPEN = Tile(
    type         = "chest_open",
    walkable     = False,
    blocks_sight = False
)