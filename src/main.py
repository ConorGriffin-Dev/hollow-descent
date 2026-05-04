import pygame
import sys
from engine.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    ROOM_WIDTH, ROOM_HEIGHT, ROOM_COLS, ROOM_ROWS,
    COL_BACKGROUND
)
from engine.renderer import draw_room, draw_sidebar, draw_message_log
from engine.game_state import GameState
from entities.player import Player
from world.dungeon_gen import generate_floor
from engine.renderer import draw_room, draw_sidebar, draw_message_log, draw_room_header

def handle_input(event, game_state):
    """
    Maps WASD and arrow keys to player movement.
    Checks for exit transitions when player walks into an exit tile.
    All input routed through GameState.
    """
    if event.type != pygame.KEYDOWN:
        return

    player = game_state.player
    floor  = game_state.current_floor
    room   = floor.get_current_room()

    # Store position before move to detect if player actually moved
    prev_col, prev_row = player.col, player.row

    if event.key in (pygame.K_w, pygame.K_UP):
        player.move(0, -1, room)
    elif event.key in (pygame.K_s, pygame.K_DOWN):
        player.move(0, 1, room)
    elif event.key in (pygame.K_a, pygame.K_LEFT):
        player.move(-1, 0, room)
    elif event.key in (pygame.K_d, pygame.K_RIGHT):
        player.move(1, 0, room)

    # Check for exit discovery after every move
    if player.col != prev_col or player.row != prev_row:
        check_exit_discovery(player, room)
        check_room_transition(game_state)

def check_exit_discovery(player, room):
    """
    Checks if the player is close enough to discover any exits.
    Marks exits as discovered so they appear on the minimap.
    Discovery radius is 2 tiles normally.
    """
    DISCOVERY_RADIUS = 2

    for exit in room.exits:
        if exit.discovered:
            continue

        # Get the tile position of this exit on the room border
        exit_col, exit_row = get_exit_position(room, exit.direction)

        # Chebyshev distance — max of horizontal and vertical distance
        distance = max(
            abs(player.col - exit_col),
            abs(player.row - exit_row)
        )

        if distance <= DISCOVERY_RADIUS:
            exit.discovered = True

def get_exit_position(room, direction):
    """
    Returns the tile position (col, row) of an exit
    based on which wall it is on.
    Exits are centred on their respective walls.
    """
    centre_col = room.width  // 2
    centre_row = room.height // 2

    positions = {
        "north": (centre_col, 0),
        "south": (centre_col, room.height - 1),
        "east":  (room.width - 1, centre_row),
        "west":  (0, centre_row),
    }
    return positions[direction]

def check_room_transition(game_state):
    """
    Checks if the player has walked into an exit tile.
    If so, transitions them to the connected room.
    Places Vincent at the opposite exit of the new room.
    """
    player = game_state.player
    floor  = game_state.current_floor
    room   = floor.get_current_room()

    for exit in room.exits:
        exit_col, exit_row = get_exit_position(room, exit.direction)

        if player.col == exit_col and player.row == exit_row:
            # Transition to the connected room
            next_room = floor.get_room(exit.leads_to)
            if next_room:
                floor.player_current_room = next_room.id

                # Mark new room as visited
                if not next_room.visited:
                    next_room.visited     = True
                    next_room.first_visit = True
                    game_state.add_message(f"You enter {next_room.name}.")
                else:
                    next_room.first_visit = False

                # Place player at the opposite exit of the new room
                opposite = {
                    "north": "south",
                    "south": "north",
                    "east":  "west",
                    "west":  "east",
                }
                opp_direction = opposite[exit.direction]
                opp_exit      = next((
                    e for e in next_room.exits
                    if e.direction == opp_direction
                ), None)

                if opp_exit:
                    opp_col, opp_row = get_exit_position(next_room, opp_direction)
                    # Place player one step inside the room from the exit
                    offsets = {
                        "north": (0,  1),
                        "south": (0, -1),
                        "east":  (-1, 0),
                        "west":  (1,  0),
                    }
                    off_col, off_row = offsets[opp_direction]
                    player.col = opp_col + off_col
                    player.row = opp_row + off_row
                else:
                    # Fallback — place at room centre
                    player.col = next_room.width  // 2
                    player.row = next_room.height // 2

            break

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    # Fonts
    font       = pygame.font.SysFont("Courier New", 13)
    font_small = pygame.font.SysFont("Courier New", 11)

    # Generate floor 1
    floor = generate_floor(floor_number=1, seed=42)

    # Initialise player at the start room centre
    start_room = floor.get_current_room()
    player     = Player(col=start_room.width // 2, row=start_room.height // 2)

    # Initialise GameState
    game_state = GameState(
        player        = player,
        current_floor = floor,
        run_seed      = 42,
    )

    # Mark start room as visited
    start_room.visited     = True
    start_room.first_visit = False

    # Starting messages
    game_state.add_message("You descend into the Underspire.")
    game_state.add_message(f"You stand in {start_room.name}.")
    game_state.set_story_message(
        "The door behind you is gone. Only the dark remains."
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            handle_input(event, game_state)

        screen.fill(COL_BACKGROUND)

        # Get current room from GameState
        current_room = game_state.current_floor.get_current_room()

        # Draw in order — room, player, UI on top
        draw_room(screen, current_room)
        game_state.player.draw(screen)
        draw_room(screen, current_room)
        game_state.player.draw(screen)
        draw_room_header(screen, font, current_room)
        draw_sidebar(
            screen, font, font_small,
            game_state.player.to_sidebar_dict(),
            game_state.current_floor,
            game_state.current_floor.player_current_room
        )
        draw_message_log(
            screen, font, font_small,
            game_state.messages,
            game_state.story_message
        )
        draw_sidebar(
            screen, font, font_small,
            game_state.player.to_sidebar_dict(),
            game_state.current_floor,
            game_state.current_floor.player_current_room
        )
        draw_message_log(
            screen, font, font_small,
            game_state.messages,
            game_state.story_message
        )

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()