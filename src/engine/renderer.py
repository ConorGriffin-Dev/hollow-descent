import pygame
from world.tile import Tile

# Tile size in pixels
TILE_SIZE = 32

# Colours per tile type (temporary — replaced by sprites later)
TILE_COLOURS = {
    "wall":          (40,  40,  40),   # dark grey
    "floor":         (80,  70,  60),   # warm dark brown
    "door":          (100, 70,  40),   # slightly lighter brown
    "staircase_down":(80,  50, 100),   # muted purple
    "staircase_up":  (80,  50, 100),   # muted purple
}

def draw_room(screen, room):
    """
    Draws the full tile grid of a Room object.
    Iterates every tile, looks up its colour, draws a rectangle.
    Draws a subtle grid line over each tile for readability.
    """
    for row_index, row in enumerate(room.tiles):
        for col_index, tile in enumerate(row):

            # Get colour for this tile type
            colour = TILE_COLOURS.get(tile.type, (0, 0, 0))

            # Calculate pixel position from grid position
            pixel_x = col_index * TILE_SIZE
            pixel_y = row_index * TILE_SIZE

            rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)

            # Draw filled tile
            pygame.draw.rect(screen, colour, rect)

            # Draw grid line (1px border, slightly darker)
            pygame.draw.rect(screen, (20, 20, 20), rect, 1)