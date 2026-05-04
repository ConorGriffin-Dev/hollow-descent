from dataclasses import dataclass, field
from typing import List, Optional, Dict
from world.tile import Tile

@dataclass
class Exit:
    direction: str
    leads_to: str
    discovered: bool = False

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
    enemies: List = field(default_factory=list)   # Enemy objects in this room
    items: List   = field(default_factory=list)   # Item objects in this room
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
        Exit positions are always walkable.
        Tiles occupied by living enemies are not walkable.
        """
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False

        # Exit tiles are always walkable
        for exit in self.exits:
            exit_col, exit_row = self.get_exit_position(exit.direction)
            if col == exit_col and row == exit_row:
                return True

        # Tiles with living enemies block movement
        for enemy in self.enemies:
            if enemy.alive and enemy.col == col and enemy.row == row:
                return False

        return self.tiles[row][col].walkable

    def get_enemy_at(self, col, row):
        """
        Returns the living enemy at (col, row) or None.
        Used by combat system to detect attack targets.
        """
        for enemy in self.enemies:
            if enemy.alive and enemy.col == col and enemy.row == row:
                return enemy
        return None

    def all_enemies_dead(self):
        """Returns True if all enemies in the room are dead."""
        return all(not e.alive for e in self.enemies)