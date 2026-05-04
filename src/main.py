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
from entities.behaviors import take_enemy_turn
from world.dungeon_gen import generate_floor
from engine.renderer import draw_room, draw_sidebar, draw_message_log, draw_room_header
from systems.combat import resolve_player_attack, resolve_enemy_attack, check_level_up
from engine.renderer import (
    draw_room, draw_sidebar, draw_message_log,
    draw_room_header, draw_game_over
)

def handle_input(event, game_state):
    """
    Maps WASD and arrow keys to player movement or combat.
    If the target tile contains a living enemy — attack it.
    If the tile is walkable — move into it.
    All input routed through GameState.
    """
    if event.type != pygame.KEYDOWN:
        return
    
    # Don't process input if game is already over
    if game_state.game_phase == "game_over":
        return

    player = game_state.player
    floor  = game_state.current_floor
    room   = floor.get_current_room()

    # Map key to intended direction
    direction_map = {
        pygame.K_w:     (0,  -1),
        pygame.K_UP:    (0,  -1),
        pygame.K_s:     (0,   1),
        pygame.K_DOWN:  (0,   1),
        pygame.K_a:     (-1,  0),
        pygame.K_LEFT:  (-1,  0),
        pygame.K_d:     (1,   0),
        pygame.K_RIGHT: (1,   0),
    }

    if event.key not in direction_map:
        return

    d_col, d_row   = direction_map[event.key]
    target_col     = player.col + d_col
    target_row     = player.row + d_row

    # Check if target tile has a living enemy — if so attack it
    enemy = room.get_enemy_at(target_col, target_row)

    if enemy:
        # ── Player attacks enemy ──────────────────────────────────
        result = resolve_player_attack(player, enemy)
        game_state.add_message(result.message)

        if result.target_died:
            # Award XP
            player.xp += result.xp_gained
            game_state.add_message(
                f"You gain {result.xp_gained} XP."
            )

            # Check for level up
            levelled = check_level_up(player)
            if levelled:
                game_state.add_message(
                    f"You are now level {player.level}!"
                )

        else:
            # ── Enemy attacks back if still alive ─────────────────
            enemy_msg, damage = resolve_enemy_attack(enemy, player)
            game_state.add_message(enemy_msg)

            # Check if Vincent died
            if player.hp <= 0:
                game_state.game_phase = "game_over"
                game_state.add_message(
                    "Darkness takes you. The Underspire claims another."
                )

    else:
        # No enemy — attempt normal movement
        prev_col, prev_row = player.col, player.row
        player.move(d_col, d_row, room)

        if player.col != prev_col or player.row != prev_row:
            check_exit_discovery(player, room)
            check_room_transition(game_state)
            
    # ── Enemy turns ───────────────────────────────────────────────
    if game_state.game_phase != "game_over":
        room = game_state.current_floor.get_current_room()
        for enemy in room.enemies:
            if enemy.alive:
                take_enemy_turn(
                    enemy,
                    game_state.player,
                    room,
                    game_state
                )
                # Stop immediately if Vincent died this turn
                if game_state.game_phase == "game_over":
                    break


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
            # ESC quits from the game over screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state.game_phase == "game_over":
                        pygame.quit()
                        sys.exit()
            handle_input(event, game_state)

        screen.fill(COL_BACKGROUND)

        if game_state.game_phase == "game_over":
            # Show game over screen instead of normal game
            draw_game_over(screen, font, font_small)
        else:
            # Normal game rendering
            current_room = game_state.current_floor.get_current_room()

            draw_room(screen, current_room)
            for enemy in current_room.enemies:
                enemy.draw(screen)
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

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()