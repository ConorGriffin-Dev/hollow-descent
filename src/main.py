import pygame
import sys
from engine.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    SIDEBAR_WIDTH, ROOM_WIDTH, ROOM_COLS, ROOM_ROWS
)
from engine.renderer import draw_room, draw_sidebar
from entities.player import Player
from world.tile import WALL, FLOOR
from world.room import Room

def build_test_room():
    """
    Builds a test room sized to fill the full room viewport.
    Walls on edges, floor in the interior.
    """
    W = WALL
    F = FLOOR

    tile_grid = []
    for row in range(ROOM_ROWS):
        tile_row = []
        for col in range(ROOM_COLS):
            if row == 0 or row == ROOM_ROWS - 1:
                tile_row.append(W)
            elif col == 0 or col == ROOM_COLS - 1:
                tile_row.append(W)
            else:
                tile_row.append(F)
        tile_grid.append(tile_row)

    return Room(
        id          = "room_001",
        name        = "The Entry Hollow",
        description = "Cold stone surrounds you. The door behind you is gone.",
        room_type   = "standard",
        width       = ROOM_COLS,
        height      = ROOM_ROWS,
        tiles       = tile_grid,
        exits       = [],
        visited     = True,
        first_visit = True,
    )

def handle_input(event, player, room):
    """
    Maps WASD and arrow keys to player movement.
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

    room   = build_test_room()
    player = Player(start_col=1, start_row=1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_input(event, player, room)

        screen.fill((0, 0, 0))
        draw_room(screen, room)
        player.draw(screen)
        draw_sidebar(screen, WINDOW_WIDTH, ROOM_WIDTH, SIDEBAR_WIDTH, WINDOW_HEIGHT)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()