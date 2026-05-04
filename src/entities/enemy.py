import pygame
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from engine.constants import TILE_SIZE

# Enemy colours (temporary — replaced by sprites later)
ENEMY_COLOURS = {
    "goblin":       (80,  120, 60),    # muted green
    "rat":          (100, 90,  70),    # dirty brown
    "skeleton":     (180, 170, 150),   # pale bone
    "ashen_knight": (120, 100, 70),    # rusty orange
    "dark_mage":    (120, 80,  160),   # purple
    "default":      (160, 60,  60),    # fallback red
}

@dataclass
class Enemy:
    """
    Represents a single enemy in the dungeon.
    Stats, position, behaviour and state all live here.
    """
    id: str
    name: str
    enemy_type: str             # used to look up colour and sprite later
    hp: int
    max_hp: int
    atk: int
    def_: int
    spd: int
    xp_reward: int
    col: int = 0                # tile position
    row: int = 0
    alive: bool = True
    behavior: str = "aggressive"
    # "aggressive" "ranged" "patrol" "coward" "coordinator" "adapter"
    behavior_state: Dict = field(default_factory=dict)
    special_ability: Optional[str] = None
    ability_cooldown: int = 0
    drop_table: List = field(default_factory=list)

    def draw(self, screen):
        """
        Draws the enemy as a coloured rectangle.
        Only draws if alive.
        """
        if not self.alive:
            return

        colour  = ENEMY_COLOURS.get(self.enemy_type, ENEMY_COLOURS["default"])
        pixel_x = self.col * TILE_SIZE
        pixel_y = self.row * TILE_SIZE
        rect    = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, colour, rect)

        # Draw a small HP bar above the enemy
        draw_enemy_hp_bar(screen, pixel_x, pixel_y, self.hp, self.max_hp)

def draw_enemy_hp_bar(screen, pixel_x, pixel_y, hp, max_hp):
    """
    Draws a small HP bar directly above an enemy tile.
    Red fill scaled to current HP percentage.
    """
    bar_width  = TILE_SIZE
    bar_height = 3
    fill       = int(bar_width * (hp / max_hp))
    bar_y      = pixel_y - bar_height - 1

    # Background
    pygame.draw.rect(screen, (40, 10, 10),
                     pygame.Rect(pixel_x, bar_y, bar_width, bar_height))
    # Fill
    pygame.draw.rect(screen, (180, 40, 40),
                     pygame.Rect(pixel_x, bar_y, fill, bar_height))


def make_goblin(col, row):
    """
    Factory function — creates a standard goblin enemy.
    Factory functions keep enemy creation clean and consistent.
    """
    return Enemy(
        id           = f"goblin_{col}_{row}",
        name         = "Goblin",
        enemy_type   = "goblin",
        hp           = 15,
        max_hp       = 15,
        atk          = 4,
        def_         = 1,
        spd          = 8,
        xp_reward    = 20,
        col          = col,
        row          = row,
        behavior     = "aggressive",
    )

def make_rat(col, row):
    """Factory function — creates a rat enemy."""
    return Enemy(
        id           = f"rat_{col}_{row}",
        name         = "Rat",
        enemy_type   = "rat",
        hp           = 8,
        max_hp       = 8,
        atk          = 2,
        def_         = 0,
        spd          = 12,
        xp_reward    = 10,
        col          = col,
        row          = row,
        behavior     = "aggressive",
    )