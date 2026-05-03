import pygame
import sys
from engine.renderer import draw_room, TILE_SIZE
from entities.player import Player
from world.tile import WALL, FLOOR
from world.room import Room, Exit

# Window settings
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720
FPS           = 60
TITLE         = "The Hollow Descent"

def build_test_room():
    """
    Builds a hardcoded test Room using proper Tile objects.
    This will be replaced by the dungeon generator in a later step.
    W = wall tile, F = floor tile.
    """
    W = WALL
    F = FLOOR

    # 10 columns wide, 8 rows tall
    tile_grid = [
        [W, W, W, W, W, W, W, W, W, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, F, F, F, F, F, F, F, F, W],
        [W, W, W, W, W, W, W, W, W, W],
    ]

    return Room(
        id          = "room_001",
        name        = "The Entry Hollow",
        description = "Cold stone surrounds you. The door behind you is gone.",
        room_type   = "standard",
        width       = 10,
        height      = 8,
        tiles       = tile_grid,
        exits       = [],       # no exits yet — added in later step
        visited     = True,
        first_visit = True,
    )

def handle_input(event, player, room):
    """
    Maps WASD and arrow key presses to player movement.
    Passes the Room object so move() can check tile walkability.
    """
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_w, pygame.K_UP):
            player.move(0, -1, room)
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            player.move(0, 1, room)
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            player.move(-1, 0, room)
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            player.move(1, 0, room)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    # Build the test room
    room = build_test_room()

    # Place player at tile (1, 1) — first walkable floor tile
    player = Player(start_col=1, start_row=1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            handle_input(event, player, room)

        screen.fill((0, 0, 0))

        # Draw room then player on top
        draw_room(screen, room)
        player.draw(screen, TILE_SIZE)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()