import pygame
from engine.constants import (
    TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT,
    SIDEBAR_WIDTH, MESSAGE_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COL_SIDEBAR, COL_MESSAGELOG, COL_BORDER,
    COL_TEXT_DIM, COL_TEXT_MID, COL_TEXT_BRIGHT,
    COL_TITLE, COL_PLAYER_NAME,
    COL_HP_TEXT, COL_HP_BAR_BG, COL_HP_BAR_FILL,
    COL_XP_TEXT, COL_XP_BAR_BG, COL_XP_BAR_FILL,
    COL_ATK, COL_DEF, COL_SPD, COL_LCK, COL_GOLD,
    COL_STORY_LABEL, COL_STORY_TEXT
)

# Colours per tile type (temporary — replaced by sprites later)
TILE_COLOURS = {
    "wall":           (35,  30,  25),
    "floor":          (75,  65,  55),
    "door":           (100, 70,  40),
    "staircase_down": (80,  50, 100),
    "staircase_up":   (80,  50, 100),
}

# Minimap cell size in pixels
MINIMAP_CELL = 10
MINIMAP_GAP  = 3

# Minimap room colours
COL_MM_CURRENT   = (200, 170, 110)   # amber — current room
COL_MM_VISITED   = (80,  70,  55)    # dim brown — visited
COL_MM_STORY     = (90,  160, 110)   # green — story item room
COL_MM_MERCHANT  = (90,  120, 180)   # blue — merchant room
COL_MM_DANGER    = (160, 60,  60)    # red — danger room
COL_MM_CONNECTOR = (55,  45,  35)    # dim — exit connectors

def draw_room(screen, room):
    """
    Draws the full tile grid of a Room object.
    Renders exit positions as visible openings in the walls.
    """
    # Build set of exit tile positions for quick lookup
    exit_positions = set()
    for exit in room.exits:
        col, row = get_exit_tile_position(room, exit.direction)
        exit_positions.add((col, row))
        if exit.direction in ("north", "south"):
            exit_positions.add((col - 1, row))
            exit_positions.add((col + 1, row))
        else:
            exit_positions.add((col, row - 1))
            exit_positions.add((col, row + 1))

    for row_index, row_tiles in enumerate(room.tiles):
        for col_index, tile in enumerate(row_tiles):
            if (col_index, row_index) in exit_positions:
                colour = (55, 45, 35)
            else:
                colour = TILE_COLOURS.get(tile.type, (0, 0, 0))

            pixel_x = col_index * TILE_SIZE
            pixel_y = row_index * TILE_SIZE
            rect    = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, (18, 15, 12), rect, 1)

def get_exit_tile_position(room, direction):
    """
    Returns the (col, row) tile position of an exit
    based on which wall it sits on.
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

def draw_sidebar(screen, font, font_small, player_data, floor, current_room_id):
    """
    Draws the sidebar panel on the right.
    Shows title, player stats, HP/XP bars, and minimap.
    """
    # Background
    sidebar_rect = pygame.Rect(ROOM_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COL_SIDEBAR, sidebar_rect)

    # Left border
    pygame.draw.line(screen, COL_BORDER, (ROOM_WIDTH, 0), (ROOM_WIDTH, WINDOW_HEIGHT), 2)

    x         = ROOM_WIDTH + 14
    y         = 16
    bar_width = SIDEBAR_WIDTH - 28

    def draw_text(text, colour, small=False):
        nonlocal y
        f       = font_small if small else font
        surface = f.render(text, True, colour)
        screen.blit(surface, (x, y))
        y += 18 if small else 22

    def draw_divider():
        nonlocal y
        y += 5
        pygame.draw.line(
            screen, COL_BORDER,
            (x, y), (x + bar_width, y), 1
        )
        y += 10

    def draw_bar(bg_col, fill_col, current, maximum, height=6):
        nonlocal y
        fill = int(bar_width * min(current / maximum, 1.0))
        pygame.draw.rect(screen, bg_col,   pygame.Rect(x, y, bar_width, height))
        pygame.draw.rect(screen, fill_col, pygame.Rect(x, y, fill,      height))
        pygame.draw.rect(screen, COL_BORDER, pygame.Rect(x, y, bar_width, height), 1)
        y += height + 8

    # ── Title ──────────────────────────────────────────────────────
    draw_text("THE HOLLOW DESCENT", COL_TITLE)
    draw_divider()

    # ── Character ──────────────────────────────────────────────────
    draw_text("VINCENT", COL_PLAYER_NAME)
    draw_text(f"Floor  {player_data['floor']} / 10", COL_TEXT_MID, small=True)
    draw_text(f"Level  {player_data['level']}", COL_TEXT_MID, small=True)
    draw_text(f"Rooms  {player_data['rooms_visited']} / {player_data['rooms_total']}", COL_TEXT_DIM, small=True)
    draw_divider()

    # ── HP ─────────────────────────────────────────────────────────
    draw_text(f"HP   {player_data['hp']} / {player_data['max_hp']}", COL_HP_TEXT)
    draw_bar(COL_HP_BAR_BG, COL_HP_BAR_FILL, player_data['hp'], player_data['max_hp'])

    # ── XP ─────────────────────────────────────────────────────────
    draw_text(f"XP   {player_data['xp']} / {player_data['xp_next']}", COL_XP_TEXT, small=True)
    draw_bar(COL_XP_BAR_BG, COL_XP_BAR_FILL, player_data['xp'], player_data['xp_next'], height=4)

    draw_divider()

    # ── Stats ──────────────────────────────────────────────────────
    draw_text("STATS", COL_TEXT_DIM, small=True)
    y += 4

    for label, value, colour in [
        ("ATK", player_data['atk'],  COL_ATK),
        ("DEF", player_data['def_'], COL_DEF),
        ("SPD", player_data['spd'],  COL_SPD),
        ("LCK", player_data['lck'],  COL_LCK),
    ]:
        screen.blit(font_small.render(label,       True, COL_TEXT_DIM), (x,      y))
        screen.blit(font_small.render(str(value),  True, colour),       (x + 55, y))
        y += 18

    draw_divider()

    # ── Gold ───────────────────────────────────────────────────────
    draw_text(f"Gold   {player_data['gold']}", COL_GOLD)

    draw_divider()

    # ── Minimap ────────────────────────────────────────────────────
    draw_text("MAP", COL_TEXT_DIM, small=True)
    y += 4

    if floor:
        draw_minimap(screen, font_small, floor, current_room_id, x, y)

def draw_minimap(screen, font, floor, current_room_id, start_x, start_y):
    """
    Draws the minimap inside the sidebar.
    Only visited rooms are shown — blank until explored.
    Exits only appear once discovered.
    Rooms are small coloured squares connected by lines.
    """
    # Assign a grid position to each room based on connections.
    # Start from the start room at (0,0) and walk the graph.
    positions = {}
    assign_minimap_positions(floor, positions)

    if not positions:
        return

    # Find bounds of the position grid
    all_cols = [p[0] for p in positions.values()]
    all_rows = [p[1] for p in positions.values()]
    min_col  = min(all_cols)
    min_row  = min(all_rows)

    # Minimap available width inside sidebar
    max_map_width = SIDEBAR_WIDTH - 28

    for room_id, (grid_col, grid_row) in positions.items():
        room = floor.rooms.get(room_id)
        if not room or not room.visited:
            continue   # only draw visited rooms

        # Convert grid position to pixel position
        px = start_x + (grid_col - min_col) * (MINIMAP_CELL + MINIMAP_GAP)
        py = start_y + (grid_row - min_row) * (MINIMAP_CELL + MINIMAP_GAP)

        # Skip if outside sidebar bounds
        if px + MINIMAP_CELL > ROOM_WIDTH + SIDEBAR_WIDTH - 4:
            continue

        # Pick room colour based on type and state
        if room_id == current_room_id:
            colour = COL_MM_CURRENT
        elif room_id == floor.staircase_room_id:
            colour = (80, 50, 100)      # purple — staircase room
        elif room.room_type == "merchant":
            colour = COL_MM_MERCHANT
        elif room.room_type == "secret":
            colour = COL_MM_STORY
        else:
            colour = COL_MM_VISITED

        # Draw room square
        pygame.draw.rect(screen, colour, pygame.Rect(px, py, MINIMAP_CELL, MINIMAP_CELL))

        # Draw discovered exit connectors
        for exit in room.exits:
            if not exit.discovered:
                continue

            # Only draw connector if destination room is visited
            dest = floor.rooms.get(exit.leads_to)
            if not dest or not dest.visited:
                continue

            # Draw a small line from room centre toward exit direction
            cx = px + MINIMAP_CELL // 2
            cy = py + MINIMAP_CELL // 2

            offsets = {
                "north": (0,  -(MINIMAP_CELL // 2 + MINIMAP_GAP // 2)),
                "south": (0,   (MINIMAP_CELL // 2 + MINIMAP_GAP // 2)),
                "east":  ( (MINIMAP_CELL // 2 + MINIMAP_GAP // 2), 0),
                "west":  (-(MINIMAP_CELL // 2 + MINIMAP_GAP // 2), 0),
            }
            ox, oy = offsets[exit.direction]
            pygame.draw.line(
                screen, COL_MM_CONNECTOR,
                (cx, cy), (cx + ox, cy + oy), 2
            )

def assign_minimap_positions(floor, positions, room_id=None, col=0, row=0, visited=None):
    """
    Recursively assigns grid positions to rooms by walking the graph.
    Starts from the floor's start room at grid (0, 0).
    Each exit moves one step in the corresponding direction.
    Only assigns positions to visited rooms.
    """
    if visited is None:
        visited  = set()
        room_id  = floor.start_room_id

    if room_id in visited:
        return

    visited.add(room_id)
    room = floor.rooms.get(room_id)

    if not room or not room.visited:
        return

    positions[room_id] = (col, row)

    direction_offsets = {
        "north": (0,  -1),
        "south": (0,   1),
        "east":  ( 1,  0),
        "west":  (-1,  0),
    }

    for exit in room.exits:
        if exit.discovered:
            d_col, d_row = direction_offsets[exit.direction]
            assign_minimap_positions(
                floor, positions,
                room_id = exit.leads_to,
                col     = col + d_col,
                row     = row + d_row,
                visited = visited
            )

def draw_message_log(screen, font, font_small, messages, story_message=None):
    """
    Draws the split message log at the bottom of the window.
    Left side — general log, last 3 messages.
    Right side — pinned story/quest panel.
    """
    # Background
    log_rect = pygame.Rect(0, ROOM_HEIGHT, WINDOW_WIDTH, MESSAGE_HEIGHT)
    pygame.draw.rect(screen, COL_MESSAGELOG, log_rect)

    # Top border
    pygame.draw.line(screen, COL_BORDER, (0, ROOM_HEIGHT), (WINDOW_WIDTH, ROOM_HEIGHT), 1)

    # Divider between general log and story panel
    pygame.draw.line(
        screen, COL_BORDER,
        (ROOM_WIDTH, ROOM_HEIGHT),
        (ROOM_WIDTH, WINDOW_HEIGHT), 1
    )

    # ── Left — general log ─────────────────────────────────────────
    recent  = messages[-3:] if len(messages) >= 3 else messages[:]
    colours = [COL_TEXT_DIM, COL_TEXT_MID, COL_TEXT_BRIGHT]

    while len(recent) < 3:
        recent.insert(0, "")

    for i, msg in enumerate(recent):
        if msg:
            surface = font.render(f">  {msg}", True, colours[i])
            screen.blit(surface, (14, ROOM_HEIGHT + 8 + i * 22))

    # ── Right — story panel ────────────────────────────────────────
    sx = ROOM_WIDTH + 12
    sy = ROOM_HEIGHT + 10

    if story_message:
        label = font_small.render("STORY", True, COL_STORY_LABEL)
        screen.blit(label, (sx, sy))
        sy += 16

        words     = story_message.split()
        line      = ""
        max_width = SIDEBAR_WIDTH - 24

        for word in words:
            test = f"{line} {word}".strip()
            if font_small.size(test)[0] <= max_width:
                line = test
            else:
                screen.blit(font_small.render(line, True, COL_STORY_TEXT), (sx, sy))
                sy  += 16
                line = word

        if line:
            screen.blit(font_small.render(line, True, COL_STORY_TEXT), (sx, sy))
    else:
        screen.blit(
            font_small.render("No messages yet.", True, COL_TEXT_DIM),
            (sx, sy + 10)
        )
        
def draw_room_header(screen, font, room):
    """
    Draws the current room name at the bottom of the room area
    just above the message log. Gives the player a sense of place.
    """
    # Semi-transparent dark bar behind the text
    bar_rect = pygame.Rect(0, ROOM_HEIGHT - 24, ROOM_WIDTH, 24)
    pygame.draw.rect(screen, (10, 8, 6), bar_rect)

    # Top border of the bar
    pygame.draw.line(
        screen, COL_BORDER,
        (0, ROOM_HEIGHT - 24),
        (ROOM_WIDTH, ROOM_HEIGHT - 24), 1
    )

    # Room name left aligned
    name_surface = font.render(room.name, True, COL_TEXT_MID)
    screen.blit(name_surface, (14, ROOM_HEIGHT - 18))

    # Room type right aligned — dim, small
    type_surface = font.render(room.room_type.upper(), True, COL_TEXT_DIM)
    type_x       = ROOM_WIDTH - type_surface.get_width() - 14
    screen.blit(type_surface, (type_x, ROOM_HEIGHT - 18))     
    
def draw_game_over(screen, font, font_small):
    """
    Draws the game over screen.
    Full screen dark overlay with death message.
    Player presses R to restart or ESC to quit.
    """
    # Dark overlay
    screen.fill((5, 0, 0))

    # Centre of screen
    cx = WINDOW_WIDTH  // 2
    cy = WINDOW_HEIGHT // 2

    # Title
    title = font.render("YOU HAVE FALLEN", True, (160, 40, 40))
    screen.blit(title, (cx - title.get_width() // 2, cy - 60))

    # Subtitle
    sub = font_small.render(
        "The Underspire claims another soul.", True, (80, 40, 40)
    )
    screen.blit(sub, (cx - sub.get_width() // 2, cy - 30))

    # Instructions
    inst = font_small.render(
        "Press ESC to quit.", True, (60, 40, 40)
    )
    screen.blit(inst, (cx - inst.get_width() // 2, cy + 20))   