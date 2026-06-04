from systems.pathfinding import astar

# How close an enemy must be to detect the player
DETECTION_RADIUS = 6    # tiles (Chebyshev distance)

def get_detection_radius(enemy):
    """
    Returns the detection radius for this enemy.
    Some enemy types will have larger or smaller radii later.
    """
    return DETECTION_RADIUS

def can_detect_player(enemy, player):
    """
    Returns True if the enemy is close enough to detect Vincent.
    Uses Chebyshev distance — same metric as A*.
    """
    distance = max(
        abs(enemy.col - player.col),
        abs(enemy.row - player.row)
    )
    return distance <= get_detection_radius(enemy)

def get_tile_occupied_by_enemy(room, col, row, excluding=None):
    """
    Returns True if a living enemy (other than excluding) is on this tile.
    Used to prevent enemies stacking on the same tile.
    """
    for enemy in room.enemies:
        if enemy is excluding:
            continue
        if enemy.alive and enemy.col == col and enemy.row == row:
            return True
    return False

def run_aggressive_behavior(enemy, player, room):
    """
    Aggressive behavior — always moves toward the player.
    Uses A* to find the shortest path.
    Takes one step per turn toward Vincent.
    Does nothing if player is not detected.
    """
    if not can_detect_player(enemy, player):
        return

    # Find path from enemy to player
    path = astar(
        enemy.col, enemy.row,
        player.col, player.row,
        room
    )

    # Path includes start position — step 1 is the next tile
    if len(path) < 2:
        return

    next_col, next_row = path[1]

    # Don't move onto a tile occupied by another enemy
    if get_tile_occupied_by_enemy(room, next_col, next_row, excluding=enemy):
        return

    # Don't move onto the player's tile — that triggers combat
    # Combat is handled by the player walking into enemies
    if next_col == player.col and next_row == player.row:
        return

    enemy.col = next_col
    enemy.row = next_row

def run_coward_behavior(enemy, player, room):
    """
    Coward behavior — moves away from the player when HP is low.
    Switches to aggressive when HP is above 50%.
    """
    hp_percent = enemy.hp / enemy.max_hp

    if hp_percent > 0.5:
        # Healthy — act aggressive
        run_aggressive_behavior(enemy, player, room)
        return

    if not can_detect_player(enemy, player):
        return

    # Move away — find tile that maximises distance from player
    best_col, best_row = enemy.col, enemy.row
    best_distance      = 0

    for d_col, d_row in [(0,-1),(0,1),(-1,0),(1,0)]:
        target_col = enemy.col + d_col
        target_row = enemy.row + d_row

        if not (0 <= target_row < room.height and
                0 <= target_col < room.width):
            continue

        if not room.tiles[target_row][target_col].walkable:
            continue

        if get_tile_occupied_by_enemy(room, target_col, target_row, excluding=enemy):
            continue

        distance = max(
            abs(target_col - player.col),
            abs(target_row - player.row)
        )

        if distance > best_distance:
            best_distance = distance
            best_col      = target_col
            best_row      = target_row

    enemy.col = best_col
    enemy.row = best_row

def take_enemy_turn(enemy, player, room, game_state):
    """
    Runs the correct behavior for this enemy based on its behavior type.
    Called once per enemy per player turn.

    If the enemy is adjacent to the player after moving —
    it attacks automatically.
    """
    if not enemy.alive:
        return

    # Run movement behavior
    if enemy.behavior == "aggressive":
        run_aggressive_behavior(enemy, player, room)
    elif enemy.behavior == "coward":
        run_coward_behavior(enemy, player, room)
    # More behaviors added in Phase 2

    # Check if enemy is now adjacent to player — attack if so
    distance = max(
        abs(enemy.col - player.col),
        abs(enemy.row - player.row)
    )

    if distance == 1:
        from systems.combat import resolve_enemy_attack
        msg, damage = resolve_enemy_attack(enemy, player)
        game_state.add_message(msg)

        if player.hp <= 0:
            game_state.game_phase = "game_over"
            game_state.add_message(
                "Your signal collapses. The Tunnel claims another mind."
            )