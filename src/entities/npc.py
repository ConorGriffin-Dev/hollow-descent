import pygame
from dataclasses import dataclass, field
from typing import List
from engine.constants import TILE_SIZE

# Merchant colour — distinct blue so player recognises them
MERCHANT_COLOUR = (70, 100, 160)

@dataclass
class Merchant:
    """
    A merchant NPC that sells items to Vincent.
    Placed in merchant rooms during floor generation.
    Stock is generated once and persists until purchased.
    """
    col: int
    row: int
    stock: List = field(default_factory=list)

    def draw(self, screen):
        """Draws merchant as a blue rectangle."""
        pixel_x = self.col * TILE_SIZE
        pixel_y = self.row * TILE_SIZE
        rect    = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, MERCHANT_COLOUR, rect)

def generate_merchant_stock(floor_number):
    """
    Generates a merchant's stock appropriate to the floor depth.
    Returns a list of (item, price) tuples.
    Deeper floors have better items at higher prices.
    """
    import copy
    from systems.inventory import (
        HEALTH_POTION, STRONG_POTION, IRON_DAGGER,
        IRON_SWORD, BONE_STAFF, LEATHER_CHEST,
        IRON_HELMET, SCROLL_OF_LIGHT
    )

    # Base stock always available
    base_stock = [
        (copy.deepcopy(HEALTH_POTION), 20),
        (copy.deepcopy(HEALTH_POTION), 20),
    ]

    # Floor scaled stock
    if floor_number <= 3:
        extra = [
            (copy.deepcopy(IRON_DAGGER),    30),
            (copy.deepcopy(LEATHER_CHEST),  40),
            (copy.deepcopy(SCROLL_OF_LIGHT),35),
        ]
    elif floor_number <= 6:
        extra = [
            (copy.deepcopy(IRON_SWORD),     60),
            (copy.deepcopy(STRONG_POTION),  45),
            (copy.deepcopy(IRON_HELMET),    50),
            (copy.deepcopy(SCROLL_OF_LIGHT),35),
        ]
    else:
        extra = [
            (copy.deepcopy(BONE_STAFF),     90),
            (copy.deepcopy(STRONG_POTION),  45),
            (copy.deepcopy(STRONG_POTION),  45),
            (copy.deepcopy(IRON_SWORD),     60),
        ]

    # Identify all merchant stock — you can see what you're buying
    stock = base_stock + extra
    for item, price in stock:
        item.identified = True

    return stock