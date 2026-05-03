# Central location for all game-wide constants.
# Import from here rather than defining in multiple files.

# Window
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720
FPS           = 60
TITLE         = "The Hollow Descent"

# Layout
SIDEBAR_WIDTH = 220
ROOM_WIDTH    = WINDOW_WIDTH - SIDEBAR_WIDTH   # 1060px
ROOM_HEIGHT   = WINDOW_HEIGHT                  # 720px

# Tiles
TILE_SIZE     = 32
ROOM_COLS     = ROOM_WIDTH  // TILE_SIZE       # 33
ROOM_ROWS     = ROOM_HEIGHT // TILE_SIZE       # 22