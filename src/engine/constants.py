# Central location for all game-wide constants.
# Import from here rather than defining in multiple files.

# Window
WINDOW_WIDTH   = 1280
WINDOW_HEIGHT  = 720
FPS            = 60
TITLE          = "The Hollow Descent"

# Layout
SIDEBAR_WIDTH  = 220
MESSAGE_HEIGHT = 80
ROOM_WIDTH     = WINDOW_WIDTH - SIDEBAR_WIDTH
ROOM_HEIGHT    = WINDOW_HEIGHT - MESSAGE_HEIGHT

# Tiles
TILE_SIZE      = 32
ROOM_COLS      = ROOM_WIDTH  // TILE_SIZE
ROOM_ROWS      = ROOM_HEIGHT // TILE_SIZE

# Colours
COL_BACKGROUND  = (0,   0,   0)
COL_SIDEBAR     = (12,  10,  8)
COL_MESSAGELOG  = (8,   8,   8)
COL_BORDER      = (55,  45,  35)

COL_TEXT_DIM    = (90,  80,  65)
COL_TEXT_MID    = (160, 145, 120)
COL_TEXT_BRIGHT = (220, 205, 175)

COL_TITLE       = (180, 130, 60)
COL_PLAYER_NAME = (230, 210, 170)

COL_HP_TEXT     = (210, 75,  75)
COL_HP_BAR_BG   = (50,  15,  15)
COL_HP_BAR_FILL = (180, 45,  45)

COL_XP_TEXT     = (90,  130, 200)
COL_XP_BAR_BG   = (10,  15,  40)
COL_XP_BAR_FILL = (45,  80,  180)

COL_ATK         = (210, 90,  90)
COL_DEF         = (90,  140, 210)
COL_SPD         = (90,  200, 140)
COL_LCK         = (200, 180, 70)

COL_GOLD        = (200, 175, 60)
COL_PLAYER      = (200, 170, 110)

# Story panel colours
COL_STORY_LABEL = (100, 160, 120)     # muted green for STORY label
COL_STORY_TEXT  = (170, 210, 185)     # soft green-white for story text