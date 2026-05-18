import pygame
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from engine.constants import TILE_SIZE, COL_PLAYER

@dataclass
class Player:
    """
    Represents Vincent — the player character.
    All stats, inventory, and progression live here.
    This is the single source of truth for player data.
    """
    name: str = "Vincent"

    # Core stats
    level: int   = 1
    hp: int      = 100
    max_hp: int  = 100
    atk: int     = 5
    def_: int    = 2
    spd: int     = 10
    lck: int     = 5

    # Progression
    xp: int      = 0
    xp_next: int = 100
    gold: int    = 0

    # Position in the current room (tile coordinates)
    col: int     = 1
    row: int     = 1

    # Floor tracking
    current_floor: int = 1

    # Inventory (to be expanded in Phase 2)
    inventory: List     = field(default_factory=list)
    inventory_cap: int  = 12
    # Inventory (to be expanded in Phase 2)
    inventory: List     = field(default_factory=list)
    inventory_cap: int  = 12
    equipped: Dict      = field(default_factory=lambda: {
        "weapon": None,
        "helmet": None,
        "chest":  None,
        "gloves": None,
        "boots":  None,
    })
    story_items: List   = field(default_factory=list)
    story_items: List   = field(default_factory=list)

    # Abilities and progression tracking
    abilities: List          = field(default_factory=list)
    oaths_sworn: List        = field(default_factory=list)
    playstyle_counters: Dict = field(default_factory=lambda: {
        "blade_actions":  0,
        "reader_actions": 0,
        "shadow_actions": 0,
    })

    # Status effects (to be expanded in Phase 2)
    status_effects: List = field(default_factory=list)

    def move(self, d_col, d_row, room):
        """
        Attempts to move Vincent by (d_col, d_row) tiles.
        Uses Room.is_walkable() to validate the target tile.
        """
        target_col = self.col + d_col
        target_row = self.row + d_row
        if room.is_walkable(target_col, target_row):
            self.col = target_col
            self.row = target_row

    def draw(self, screen):
        """
        Draws Vincent as a coloured rectangle.
        Converts tile position to pixel position for Pygame.
        """
        pixel_x = self.col * TILE_SIZE
        pixel_y = self.row * TILE_SIZE
        rect    = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COL_PLAYER, rect)

    def to_sidebar_dict(self, floor=None):
        """
        Returns a dict of display values for the sidebar renderer.
        Includes player object reference for inventory rendering.
        """
        rooms_visited = 0
        rooms_total   = 0

        if floor:
            rooms_total   = len(floor.rooms)
            rooms_visited = sum(
                1 for room in floor.rooms.values()
                if room.visited
            )

        return {
            "floor":         self.current_floor,
            "hp":            self.hp,
            "max_hp":        self.max_hp,
            "xp":            self.xp,
            "xp_next":       self.xp_next,
            "level":         self.level,
            "atk":           self.atk,
            "def_":          self.def_,
            "spd":           self.spd,
            "lck":           self.lck,
            "gold":          self.gold,
            "rooms_visited": rooms_visited,
            "rooms_total":   rooms_total,
            "player_obj":    self,    # ← full player object for inventory
        }