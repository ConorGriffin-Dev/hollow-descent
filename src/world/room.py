# Room represents a single self-contained area in the dungeon.
# The player is always inside exactly one room at a time.
# Exits connect rooms to each other — discovered by proximity.

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from world.tile import Tile

@dataclass
class Exit:
    direction: str      # "north" "south" "east" "west"
    leads_to: str       # room_id of the destination room
    discovered: bool = False  # only shown on minimap once discovered

@dataclass
class Room:
    id: str                         # unique identifier e.g. "room_003"
    name: str                       # display name e.g. "The Ashen Gallery"
    description: str                # shown on first visit
    room_type: str                  # "standard" "chamber" "merchant" etc
    width: int                      # room width in tiles
    height: int                     # room height in tiles
    tiles: List[List[Tile]]         # 2D grid of Tile objects [row][col]
    exits: List[Exit] = field(default_factory=list)
    visited: bool = False           # has the player entered this room
    first_visit: bool = True        # triggers description on first entry only
    enemies_cleared: bool = False   # all enemies in room are dead
    special_state: Dict = field(default_factory=dict)  # room-specific flags

    def get_tile(self, col, row):
        """Returns the Tile at grid position (col, row)."""
        return self.tiles[row][col]

    def is_walkable(self, col, row):
        """Returns True if the tile at (col, row) can be walked on."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.tiles[row][col].walkable
        return False