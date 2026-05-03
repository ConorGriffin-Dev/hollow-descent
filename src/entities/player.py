import pygame
from engine.constants import TILE_SIZE

PLAYER_COLOUR = (200, 170, 110)  # warm amber

class Player:
    def __init__(self, start_col, start_row):
        # Grid position in tiles (not pixels)
        self.col = start_col
        self.row = start_row

    def move(self, d_col, d_row, room):
        """
        Attempts to move the player by (d_col, d_row) tiles.
        Uses Room.is_walkable() to check the target tile.
        """
        target_col = self.col + d_col
        target_row = self.row + d_row
        if room.is_walkable(target_col, target_row):
            self.col = target_col
            self.row = target_row

    def draw(self, screen):
        """
        Draws the player as a coloured rectangle.
        Converts grid position to pixel position.
        TILE_SIZE imported from constants — no longer passed as argument.
        """
        pixel_x = self.col * TILE_SIZE
        pixel_y = self.row * TILE_SIZE
        rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOUR, rect)