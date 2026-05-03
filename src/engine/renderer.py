import pygame
from engine.constants import TILE_SIZE

# Colours per tile type (temporary — replaced by sprites later)
TILE_COLOURS = {
    "wall":           (40,  40,  40),
    "floor":          (80,  70,  60),
    "door":           (100, 70,  40),
    "staircase_down": (80,  50, 100),
    "staircase_up":   (80,  50, 100),
}

def draw_room(screen, room):
    """
    Draws the full tile grid of a Room object.
    Iterates every tile, looks up its colour, draws a rectangle.
    """
    for row_index, row in enumerate(room.tiles):
        for col_index, tile in enumerate(row):
            colour = TILE_COLOURS.get(tile.type, (0, 0, 0))
            pixel_x = col_index * TILE_SIZE
            pixel_y = row_index * TILE_SIZE
            rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, (20, 20, 20), rect, 1)

def draw_sidebar(screen, window_width, room_width, sidebar_width, window_height):
    """
    Draws the sidebar panel on the right side of the window.
    Placeholder — stats, minimap, inventory added later.
    """
    sidebar_rect = pygame.Rect(room_width, 0, sidebar_width, window_height)
    pygame.draw.rect(screen, (15, 15, 15), sidebar_rect)
    pygame.draw.line(screen, (40, 40, 40), (room_width, 0), (room_width, window_height), 1)