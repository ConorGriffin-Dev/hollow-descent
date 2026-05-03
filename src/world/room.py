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
    id: str
    name: str
    description: str
    room_type: str
    width: int
    height: int
    tiles: List[List[Tile]]
    exits: List[Exit] = field(default_factory=list)
    visited: bool = False
    first_visit: bool = True
    enemies_cleared: bool = False
    special_state: Dict = field(default_factory=dict)

    def get_tile(self, col, row):
        """Returns the Tile at grid position (col, row)."""
        return self.tiles[row][col]

    def get_exit_position(self, direction):
        """
        Returns (col, row) of the exit tile for a given direction.
        Exits are centred on their respective walls.
        """
        centre_col = self.width  // 2
        centre_row = self.height // 2

        positions = {
            "north": (centre_col, 0),
            "south": (centre_col, self.height - 1),
            "east":  (self.width - 1, centre_row),
            "west":  (0, centre_row),
        }
        return positions[direction]

    def is_walkable(self, col, row):
        """
        Returns True if the tile at (col, row) can be walked on.
        Exit positions are always walkable even if the tile is a wall.
        """
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False

        # Exit tiles are always walkable — triggers room transition
        for exit in self.exits:
            exit_col, exit_row = self.get_exit_position(exit.direction)
            if col == exit_col and row == exit_row:
                return True

        return self.tiles[row][col].walkable