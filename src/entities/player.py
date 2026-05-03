import pygame

# Player visual (temporary rectangle until sprites are added)
PLAYER_COLOUR = (200, 170, 110)  # warm amber

class Player:
    def __init__(self, start_col, start_row):
        # Grid position in tiles (not pixels)
        self.col = start_col
        self.row = start_row

    def move(self, d_col, d_row, room):
        """
        Attempts to move the player by (d_col, d_row) tiles.
        Uses Room.is_walkable() to check if the target tile allows movement.
        """
        target_col = self.col + d_col
        target_row = self.row + d_row

        # Only move if the target tile is walkable
        if room.is_walkable(target_col, target_row):
            self.col = target_col
            self.row = target_row

    def draw(self, screen, tile_size):
        """
        Draws the player as a coloured rectangle.
        Converts grid position to pixel position for Pygame.
        """
        pixel_x = self.col * tile_size
        pixel_y = self.row * tile_size

        rect = pygame.Rect(pixel_x, pixel_y, tile_size, tile_size)
        pygame.draw.rect(screen, PLAYER_COLOUR, rect)