import pygame
import sys
from engine.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    ROOM_WIDTH, ROOM_HEIGHT, ROOM_COLS, ROOM_ROWS,
    COL_BACKGROUND
)
from engine.renderer import draw_room, draw_sidebar, draw_message_log
from entities.player import Player
from world.tile import WALL, FLOOR
from world.room import Room

def build_test_room():
    """
    Builds a test room sized to fill the room viewport.
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

def handle_input(event, player, room, messages):
    """
    Maps WASD and arrow keys to player movement.
    Appends a message to the log on each move.
    """
    if event.type == pygame.KEYDOWN:
        moved = False
        if event.key in (pygame.K_w, pygame.K_UP):
            player.move(0, -1, room)
            moved = True
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            player.move(0, 1, room)
            moved = True
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            player.move(-1, 0, room)
            moved = True
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            player.move(1, 0, room)
            moved = True


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    # Load font — pygame's default monospace font, size 13
    # Two font sizes — regular for headers, small for detail text
    font = pygame.font.SysFont("Courier New", 13)
    font_small = pygame.font.SysFont("Courier New", 11)

    # Build test room
    room = build_test_room()

    # Place player at first walkable tile
    player = Player(start_col=1, start_row=1)

    # Message log — starts with the room entry message
    messages = [
        "You descend into the Underspire.",
        "The Entry Hollow. Cold stone surrounds you.",
    ]

    # Story message — None until a story event fires
    # Replaced by the most recent story/quest message when triggered
    story_message = "The journal reads: your father was here."  # placeholder for testing
    
    # Placeholder player data for sidebar
    # Will be replaced by real Player object data later
    player_data = {
        "floor":   1,
        "hp":      100,
        "max_hp":  100,
        "xp":      0,
        "xp_next": 100,
        "level":   1,
        "atk":     5,
        "def_":    2,
        "spd":     10,
        "lck":     5,
        "gold":    0,
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_input(event, player, room, messages)

        screen.fill(COL_BACKGROUND)

        # Draw in order — room, player, UI panels on top
        draw_room(screen, room)
        player.draw(screen)
        draw_sidebar(screen, font, font_small, player_data)
        draw_message_log(screen, font, font_small, messages, story_message)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()