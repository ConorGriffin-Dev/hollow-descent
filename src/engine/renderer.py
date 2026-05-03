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
            colour  = TILE_COLOURS.get(tile.type, (0, 0, 0))
            pixel_x = col_index * TILE_SIZE
            pixel_y = row_index * TILE_SIZE
            rect    = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, (20, 20, 20), rect, 1)

def draw_sidebar(screen, font, font_small, player_data):
    """
    Draws the sidebar panel on the right.
    Shows game title, player stats, HP/XP bars.
    """
    # Background
    sidebar_rect = pygame.Rect(ROOM_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COL_SIDEBAR, sidebar_rect)

    # Left border
    pygame.draw.line(screen, COL_BORDER, (ROOM_WIDTH, 0), (ROOM_WIDTH, WINDOW_HEIGHT), 1)

    x   = ROOM_WIDTH + 12
    y   = 14
    gap = 22

    def draw_text(text, colour, small=False):
        nonlocal y
        f       = font_small if small else font
        surface = f.render(text, True, colour)
        screen.blit(surface, (x, y))
        y += gap if not small else 16

    def draw_divider():
        nonlocal y
        y += 4
        pygame.draw.line(screen, COL_BORDER, (x, y), (ROOM_WIDTH + SIDEBAR_WIDTH - 12, y), 1)
        y += 8

    # Title
    draw_text("THE HOLLOW DESCENT", (100, 80, 50))
    draw_divider()

    # Character and floor
    draw_text("VINCENT", COL_TEXT_BRIGHT)
    draw_text(f"Floor  {player_data['floor']}", COL_TEXT_MID, small=True)
    draw_text(f"Level  {player_data['level']}", COL_TEXT_MID, small=True)
    draw_divider()

    # HP
    draw_text(f"HP   {player_data['hp']} / {player_data['max_hp']}", (180, 60, 60))
    draw_hp_bar(screen, x, y, player_data['hp'], player_data['max_hp'])
    y += 12

    # XP
    draw_text(f"XP   {player_data['xp']} / {player_data['xp_next']}", COL_TEXT_DIM, small=True)
    draw_xp_bar(screen, x, y, player_data['xp'], player_data['xp_next'])
    y += 12

    draw_divider()

    # Stats in a cleaner two-column layout
    draw_text("STATS", COL_TEXT_DIM, small=True)
    y += 4

    stats = [
        ("ATK", player_data['atk'],  (180,  80,  80)),
        ("DEF", player_data['def_'], (80,  120, 180)),
        ("SPD", player_data['spd'],  (80,  180, 120)),
        ("LCK", player_data['lck'],  (180, 160,  60)),
    ]

    for label, value, colour in stats:
        # Label
        label_surface = font_small.render(label, True, COL_TEXT_DIM)
        screen.blit(label_surface, (x, y))
        # Value in colour
        value_surface = font_small.render(str(value), True, colour)
        screen.blit(value_surface, (x + 50, y))
        y += 18

    draw_divider()

    # Gold
    gold_surface = font.render(f"Gold  {player_data['gold']}", True, (180, 160, 60))
    screen.blit(gold_surface, (x, y))

def draw_hp_bar(screen, x, y, hp, max_hp):
    """Draws a red HP bar scaled to current/max HP."""
    bar_width  = SIDEBAR_WIDTH - 24
    fill_width = int(bar_width * (hp / max_hp))
    # Background
    pygame.draw.rect(screen, (30, 10, 10), pygame.Rect(x, y, bar_width, 6))
    # Fill
    pygame.draw.rect(screen, (140, 30, 30), pygame.Rect(x, y, fill_width, 6))

def draw_xp_bar(screen, x, y, xp, xp_next):
    """Draws a blue XP bar scaled to current/next level XP."""
    bar_width  = SIDEBAR_WIDTH - 24
    fill_width = int(bar_width * (xp / xp_next))
    # Background
    pygame.draw.rect(screen, (10, 10, 30), pygame.Rect(x, y, bar_width, 6))
    # Fill
    pygame.draw.rect(screen, (30, 60, 140), pygame.Rect(x, y, fill_width, 6))

def draw_message_log(screen, font, font_small, messages, story_message=None):
    """
    Draws the split message log at the bottom of the window.

    Left side — general log showing last 3 combat/system messages.
    Right side — pinned story/quest panel showing the most recent
                 important message until it is replaced.

    messages        list of plain strings (combat, system, general)
    story_message   single string or None — the latest story/quest message
    """
    # Full log background
    log_rect = pygame.Rect(0, ROOM_HEIGHT, WINDOW_WIDTH, MESSAGE_HEIGHT)
    pygame.draw.rect(screen, COL_MESSAGELOG, log_rect)

    # Top border across full width
    pygame.draw.line(screen, COL_BORDER, (0, ROOM_HEIGHT), (WINDOW_WIDTH, ROOM_HEIGHT), 1)

    # Divider between general log and story panel
    # Story panel is the same width as the sidebar
    story_panel_x = ROOM_WIDTH
    pygame.draw.line(
        screen, COL_BORDER,
        (story_panel_x, ROOM_HEIGHT),
        (story_panel_x, WINDOW_HEIGHT),
        1
    )

    # ── Left side — general message log ──────────────────────────
    recent  = messages[-3:] if len(messages) >= 3 else messages[:]
    colours = [COL_TEXT_DIM, COL_TEXT_MID, COL_TEXT_BRIGHT]

    # Pad to always have 3 slots
    while len(recent) < 3:
        recent.insert(0, "")

    for i, msg in enumerate(recent):
        if msg:
            surface = font.render(f">  {msg}", True, colours[i])
            screen.blit(surface, (14, ROOM_HEIGHT + 8 + i * 22))

    # ── Right side — pinned story/quest panel ─────────────────────
    sx = story_panel_x + 12   # x position inside story panel
    sy = ROOM_HEIGHT + 10      # y start inside story panel

    if story_message:
        # STORY label
        label = font_small.render("STORY", True, COL_STORY_LABEL)
        screen.blit(label, (sx, sy))
        sy += 16

        # Word wrap the story message to fit the sidebar width
        words      = story_message.split()
        line       = ""
        max_width  = SIDEBAR_WIDTH - 24

        for word in words:
            test_line = f"{line} {word}".strip()
            if font_small.size(test_line)[0] <= max_width:
                line = test_line
            else:
                # Render current line and start a new one
                surface = font_small.render(line, True, COL_STORY_TEXT)
                screen.blit(surface, (sx, sy))
                sy  += 16
                line = word

        # Render the final line
        if line:
            surface = font_small.render(line, True, COL_STORY_TEXT)
            screen.blit(surface, (sx, sy))

    else:
        # No story message yet — show placeholder
        placeholder = font_small.render("No messages yet.", True, COL_TEXT_DIM)
        screen.blit(placeholder, (sx, sy + 10))