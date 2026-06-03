import pygame
import sys
from engine.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE,
    ROOM_WIDTH, ROOM_HEIGHT, ROOM_COLS, ROOM_ROWS,
    COL_BACKGROUND
)
from engine.renderer import (
    draw_room, draw_sidebar, draw_message_log,
    draw_room_header, draw_game_over, draw_floor_items,
    draw_inventory_screen, draw_start_screen,
    draw_merchant_screen
)
from engine.game_state import GameState
from engine.constants import COL_BORDER, COL_TEXT_DIM, COL_TEXT_MID, COL_TITLE
from systems.save_system import save_game, load_game, save_exists
from entities.player import Player
from entities.behaviors import take_enemy_turn
from world.dungeon_gen import generate_floor
from systems.combat import resolve_player_attack, resolve_enemy_attack, check_level_up



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
    
    # ── Save game ─────────────────────────────────────────────────
    if event.key == pygame.K_F5:
        save_game(game_state)
        game_state.add_message("Game saved.")
        return

# ── Inventory open/close ──────────────────────────────────────
    if event.key == pygame.K_i:
        game_state.inventory_open = not game_state.inventory_open
        game_state.inventory_selected = 0
        return

    # ── Inventory navigation and actions ─────────────────────────
    if game_state.inventory_open:
        inventory = game_state.player.inventory

        if event.key == pygame.K_UP:
            game_state.inventory_selected = max(
                0, game_state.inventory_selected - 1
            )
        elif event.key == pygame.K_DOWN:
            game_state.inventory_selected = min(
                len(inventory) - 1,
                game_state.inventory_selected + 1
            )
        elif event.key == pygame.K_ESCAPE:
            game_state.inventory_open = False

        elif event.key == pygame.K_u:
            use_item(game_state)

        elif event.key == pygame.K_e:
            equip_item(game_state)

        elif event.key == pygame.K_d:
            drop_item(game_state)

        return

# ── Temporary dev heal — remove before release ────────────────
    if event.key == pygame.K_h:
        game_state.player.hp = game_state.player.max_hp
        game_state.add_message("DEV: Full heal.")
        return

# ── Pick up item ──────────────────────────────────────────────
    if event.key == pygame.K_g:
        pickup_item(game_state)
        return

    # ── Open chest ────────────────────────────────────────────────
    if event.key == pygame.K_f:
        open_chest(game_state)
        return

    # ── Merchant open/close ───────────────────────────────────────
    if event.key == pygame.K_m:
        room     = game_state.current_floor.get_current_room()
        merchant = room.special_state.get("merchant")
        if merchant:
            game_state.merchant_open     = not game_state.merchant_open
            game_state.merchant_selected = 0
        return

    # ── Merchant navigation and buying ────────────────────────────
    if game_state.merchant_open:
        room     = game_state.current_floor.get_current_room()
        merchant = room.special_state.get("merchant")

        if not merchant:
            game_state.merchant_open = False
            return

        if event.key == pygame.K_UP:
            game_state.merchant_selected = max(
                0, game_state.merchant_selected - 1
            )
        elif event.key == pygame.K_DOWN:
            game_state.merchant_selected = min(
                len(merchant.stock) - 1,
                game_state.merchant_selected + 1
            )
        elif event.key == pygame.K_ESCAPE:
            game_state.merchant_open = False
        elif event.key == pygame.K_b:
            buy_item(game_state, merchant)
        return

    if event.key not in direction_map:
        return
    
    d_col, d_row   = direction_map[event.key]
    target_col     = player.col + d_col
    target_row     = player.row + d_row

    # Check if target tile has a living enemy — if so attack it
    enemy = room.get_enemy_at(target_col, target_row)

    if enemy:
        # ── Player attacks enemy ──────────────────────────────────
        result = resolve_player_attack(
            player, enemy,
            floor_number = game_state.current_floor.number
        )
        game_state.add_message(result.message)

        if result.target_died:
            # Award XP
            player.xp += result.xp_gained
            game_state.add_message(f"You gain {result.xp_gained} XP.")
            
            # Check if room is now fully cleared
            room.all_enemies_dead()    

            # Award gold
            if result.gold_dropped > 0:
                player.gold += result.gold_dropped
                game_state.add_message(
                    f"You find {result.gold_dropped} gold."
                )

            # Drop item onto the floor at enemy position
            if result.item_dropped:
                result.item_dropped.floor_col = enemy.col
                result.item_dropped.floor_row = enemy.row
                room.items.append(result.item_dropped)
                game_state.add_message(
                    f"{enemy.name} drops {result.item_dropped.display_name()}."
                )

            # Check level up
            levelled = check_level_up(player)
            if levelled:
                game_state.add_message(
                    f"You are now level {player.level}!"
                )

        else:
            # Enemy counter attacks if still alive
            enemy_msg, damage = resolve_enemy_attack(enemy, player)
            game_state.add_message(enemy_msg)

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
            check_staircase(game_state)
            check_item_pickup(game_state)
            check_chest_interaction(game_state)
            check_merchant_interaction(game_state)
            
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

def check_staircase(game_state):
    """
    Checks if Vincent is standing on a staircase tile.
    Descending generates or loads the next floor.
    Ascending loads the previous floor from cache.
    """
    player = game_state.player
    floor  = game_state.current_floor
    room   = floor.get_current_room()

    current_tile = room.get_tile(player.col, player.row)

    if current_tile.type == "staircase_down":
        if not floor.gate_requirement.satisfied:
            game_state.add_message(
                "The way down is sealed. You must prove your worth."
            )
            return

        # Cache current floor
        game_state.floor_cache[floor.number] = floor

        next_floor_number = floor.number + 1

        if next_floor_number > 10:
            game_state.add_message("You have reached the depths. Victory!")
            return

        # Load from cache or generate fresh
        if next_floor_number in game_state.floor_cache:
            next_floor = game_state.floor_cache[next_floor_number]
        else:
            next_floor = generate_floor(
                floor_number = next_floor_number,
                seed         = game_state.run_seed
            )

        # Transition
        game_state.current_floor        = next_floor
        game_state.player.current_floor = next_floor_number

        start_room         = next_floor.get_current_room()
        start_room.visited = True
        player.col         = start_room.width  // 2
        player.row         = start_room.height // 2

        game_state.add_message(f"You descend to floor {next_floor_number}.")
        save_game(game_state)

    elif current_tile.type == "staircase_up":
        if floor.number == 1:
            game_state.add_message(
                "The way back is sealed. There is only down."
            )
            return

        # Cache current floor
        game_state.floor_cache[floor.number] = floor

        prev_floor_number = floor.number - 1
        prev_floor        = game_state.floor_cache.get(prev_floor_number)

        if not prev_floor:
            game_state.add_message("You cannot go back.")
            return

        # Transition
        game_state.current_floor        = prev_floor
        game_state.player.current_floor = prev_floor_number

        staircase_room                 = prev_floor.rooms[prev_floor.staircase_room_id]
        prev_floor.player_current_room = prev_floor.staircase_room_id
        player.col                     = staircase_room.width  // 2
        player.row                     = staircase_room.height // 2

        game_state.add_message(f"You ascend to floor {prev_floor_number}.")
        
        
def check_item_pickup(game_state):
    """
    Checks if Vincent is standing on a tile with an item.
    If so, adds a pickup prompt to the message log.
    Called every time Vincent moves.
    """
    player = game_state.player
    room   = game_state.current_floor.get_current_room()

    for item in room.items:
        if item.floor_col == player.col and item.floor_row == player.row:
            game_state.add_message(
                f"You see {item.display_name()}. Press G to pick up."
            )
            return

def check_chest_interaction(game_state):
    """
    Checks if Vincent is adjacent to a chest tile.
    If so prompts the player to press E to open it.
    """
    player = game_state.player
    room   = game_state.current_floor.get_current_room()

    # Check all adjacent tiles for a closed chest
    for d_col, d_row in [(0,-1),(0,1),(-1,0),(1,0)]:
        check_col = player.col + d_col
        check_row = player.row + d_row

        if not (0 <= check_row < room.height and
                0 <= check_col < room.width):
            continue

        tile = room.get_tile(check_col, check_row)
        if tile.type == "chest_closed":
            game_state.add_message(
                "A chest. Press F to open it."
            )
            return

def open_chest(game_state):
    """
    Opens a chest adjacent to Vincent.
    Generates loot and places it on the floor.
    Replaces chest tile with open chest tile.
    """
    from world.tile import CHEST_OPEN
    from systems.loot import generate_drop

    player = game_state.player
    room   = game_state.current_floor.get_current_room()
    floor  = game_state.current_floor

    # Find adjacent closed chest
    for d_col, d_row in [(0,-1),(0,1),(-1,0),(1,0)]:
        check_col = player.col + d_col
        check_row = player.row + d_row

        if not (0 <= check_row < room.height and
                0 <= check_col < room.width):
            continue

        tile = room.get_tile(check_col, check_row)
        if tile.type == "chest_closed":
            # Open the chest
            room.tiles[check_row][check_col] = CHEST_OPEN

            # Update special state
            chest_key = f"chest_{check_col}_{check_row}"
            if chest_key in room.special_state:
                room.special_state[chest_key]["opened"] = True

            # Generate 1-2 items
            import random
            item_count = random.randint(1, 2)
            gold       = random.randint(5, 20) * floor.number

            # Award gold
            player.gold += gold
            game_state.add_message(f"The chest opens. You find {gold} gold.")

            # Generate and place items near the chest
            for i in range(item_count):
                item = generate_drop(floor.number)

                # Place item adjacent to chest on a walkable tile
                placed = False
                for dc, dr in [(0,1),(0,-1),(1,0),(-1,0)]:
                    adj_col = check_col + dc
                    adj_row = check_row + dr
                    if room.is_walkable(adj_col, adj_row):
                        item.floor_col = adj_col
                        item.floor_row = adj_row
                        placed = True
                        break

                # Fallback to player position if no adjacent tile free
                if not placed:
                    item.floor_col = player.col
                    item.floor_row = player.row

                room.items.append(item)

            return

    game_state.add_message("Nothing to open here.")
    
def check_merchant_interaction(game_state):
    """
    Checks if Vincent is adjacent to the merchant.
    If so prompts the player to press M to open the shop.
    """
    player = game_state.player
    room   = game_state.current_floor.get_current_room()
    merchant = room.special_state.get("merchant")

    if not merchant:
        return

    distance = max(
        abs(player.col - merchant.col),
        abs(player.row - merchant.row)
    )

    if distance <= 1:
        game_state.add_message("A merchant. Press M to trade.")    
        
def buy_item(game_state, merchant):
    """
    Purchases the selected item from the merchant.
    Checks player gold and inventory space before buying.
    Removes item from merchant stock on purchase.
    """
    player = game_state.player
    idx    = game_state.merchant_selected

    if idx >= len(merchant.stock):
        return

    item, price = merchant.stock[idx]

    # Check gold
    if player.gold < price:
        game_state.add_message(
            f"You need {price}g. You only have {player.gold}g."
        )
        return

    # Check inventory space
    if len(player.inventory) >= player.inventory_cap:
        game_state.add_message("Your inventory is full.")
        return

    # Complete purchase
    player.gold     -= price
    player.inventory.append(item)
    merchant.stock.pop(idx)

    game_state.add_message(
        f"You buy {item.display_name()} for {price}g."
    )

    # Adjust selected index
    game_state.merchant_selected = min(
        game_state.merchant_selected,
        len(merchant.stock) - 1
    )        

def pickup_item(game_state):
    """
    Picks up the item at Vincent's current position.
    Checks inventory cap before adding.
    Consumables stack up to 5 in one slot.
    Story items go into a separate list and don't count
    toward the cap after the second oath.
    """
    player = game_state.player
    room   = game_state.current_floor.get_current_room()

    # Find item at player position
    item_to_pickup = None
    for item in room.items:
        if item.floor_col == player.col and item.floor_row == player.row:
            item_to_pickup = item
            break

    if not item_to_pickup:
        return

    # Handle story items separately
    if item_to_pickup.is_story_item:
        player.story_items.append(item_to_pickup)
        room.items.remove(item_to_pickup)
        game_state.add_message(
            f"You take {item_to_pickup.display_name()}."
        )
        return

    # Check if consumable stacks with existing inventory item
    if item_to_pickup.category == "consumable":
        for existing in player.inventory:
            if existing.id == item_to_pickup.id:
                if existing.quantity >= 5:
                    # Stack is full — block pickup
                    game_state.add_message(
                        f"You already carry 5 {item_to_pickup.display_name()}s."
                    )
                    return
                else:
                    existing.quantity += 1
                    room.items.remove(item_to_pickup)
                    game_state.add_message(
                        f"You pick up {item_to_pickup.display_name()}. "
                        f"({existing.quantity}/5)"
                    )
                    return

    # Check inventory cap
    if len(player.inventory) >= player.inventory_cap:
        game_state.add_message(
            "Your inventory is full. Drop something first."
        )
        return

    # Add to inventory
    player.inventory.append(item_to_pickup)
    room.items.remove(item_to_pickup)
    game_state.add_message(
        f"You pick up {item_to_pickup.display_name()}."
    )

def use_item(game_state):
    """
    Uses the currently selected inventory item.
    Only consumables can be used.
    Fires the item effect and reduces quantity.
    Removes item from inventory if quantity reaches 0.
    """
    player    = game_state.player
    inventory = player.inventory

    if not inventory:
        return

    idx  = game_state.inventory_selected
    item = inventory[idx]

    if item.category != "consumable":
        game_state.add_message(f"You can't use {item.display_name()} like that.")
        return

    # Identify the item on use
    item.identified = True

    # Fire effect
    if item.effect == "heal":
        healed    = min(item.effect_value, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + item.effect_value)
        game_state.add_message(
            f"You drink {item.display_name()}. Restored {healed} HP."
        )

    elif item.effect == "reveal_map":
        # Mark all rooms on current floor as visited
        for room in game_state.current_floor.rooms.values():
            room.visited = True
            for exit in room.exits:
                exit.discovered = True
        game_state.add_message("The scroll burns. The floor reveals itself.")

    # Reduce quantity
    item.quantity -= 1
    if item.quantity <= 0:
        inventory.pop(idx)
        # Adjust selected index if needed
        game_state.inventory_selected = min(
            idx, len(inventory) - 1
        )

def equip_item(game_state):
    """
    Equips the selected weapon or armor item.
    Swaps with currently equipped item in that slot.
    Equipped item returns to inventory.
    Updates player stats immediately.
    """
    player    = game_state.player
    inventory = player.inventory

    if not inventory:
        return

    idx  = game_state.inventory_selected
    item = inventory[idx]

    if item.category not in ("weapon", "armor"):
        game_state.add_message(f"You can't equip {item.display_name()}.")
        return

    slot = item.slot

    # Unequip current item in that slot
    if player.equipped.get(slot):
        old_item = player.equipped[slot]

        # Remove stat bonuses from old item
        if old_item.category == "weapon":
            player.atk -= old_item.atk_bonus
        elif old_item.category == "armor":
            player.def_ -= old_item.def_bonus

        # Return old item to inventory
        inventory.append(old_item)

    # Equip new item
    player.equipped[slot] = item
    inventory.pop(idx)

    # Apply stat bonuses
    if item.category == "weapon":
        player.atk += item.atk_bonus
    elif item.category == "armor":
        player.def_ += item.def_bonus

    game_state.add_message(f"You equip {item.display_name()}.")

    # Adjust selected index
    game_state.inventory_selected = min(
        game_state.inventory_selected,
        len(inventory) - 1
    )

def drop_item(game_state):
    """
    Drops the selected item onto the current room floor.
    Item appears at Vincent's current position.
    Removes item from inventory.
    """
    player    = game_state.player
    inventory = player.inventory

    if not inventory:
        return

    idx  = game_state.inventory_selected
    item = inventory[idx]

    # Place item at Vincent's feet
    item.floor_col = player.col
    item.floor_row = player.row

    # Add to room items
    room = game_state.current_floor.get_current_room()
    room.items.append(item)

    # Remove from inventory
    inventory.pop(idx)

    game_state.add_message(f"You drop {item.display_name()}.")

    # Adjust selected index
    game_state.inventory_selected = min(
        game_state.inventory_selected,
        len(inventory) - 1
    )

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont("Courier New", 13)
    font_small = pygame.font.SysFont("Courier New", 11)

    # ── Start screen loop ─────────────────────────────────────────
    has_save   = save_exists()
    game_state = None

    while game_state is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_n:
                    # New game — random seed
                    import random as _random
                    run_seed = _random.randint(0, 999999)
                    floor    = generate_floor(floor_number=1, seed=run_seed)
                    player   = Player(col=1, row=1)

                    game_state = GameState(
                        player        = player,
                        current_floor = floor,
                        run_seed      = run_seed,
                    )

                    start_room             = floor.get_current_room()
                    start_room.visited     = True
                    start_room.first_visit = False
                    player.col             = start_room.width  // 2
                    player.row             = start_room.height // 2

                    game_state.add_message("You descend into the Underspire.")
                    game_state.add_message(f"You stand in {start_room.name}.")
                    game_state.set_story_message(
                        "The door behind you is gone. Only the dark remains."
                    )

                elif event.key == pygame.K_c and has_save:
                    # Load existing save
                    game_state = load_game()
                    game_state.add_message("Welcome back.")

        draw_start_screen(screen, font, font_small, has_save)
        pygame.display.flip()
        clock.tick(FPS)

    # ── Main game loop ────────────────────────────────────────────
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state.game_phase == "game_over":
                        pygame.quit()
                        sys.exit()
            handle_input(event, game_state)

        screen.fill(COL_BACKGROUND)

        if game_state.game_phase == "game_over":
            draw_game_over(screen, font, font_small)
        else:
            current_room = game_state.current_floor.get_current_room()

            draw_room(screen, current_room)
            draw_floor_items(screen, current_room)
            if "merchant" in current_room.special_state:
                current_room.special_state["merchant"].draw(screen)
            for enemy in current_room.enemies:
                enemy.draw(screen)
            game_state.player.draw(screen)
            draw_room_header(screen, font, current_room)
            draw_sidebar(
                screen, font, font_small,
                game_state.player.to_sidebar_dict(game_state.current_floor),
                game_state.current_floor,
                game_state.current_floor.player_current_room
            )
            draw_message_log(
                screen, font, font_small,
                game_state.messages,
                game_state.story_message
            )

            if game_state.inventory_open:
                draw_inventory_screen(
                    screen, font, font_small,
                    game_state.player,
                    game_state.inventory_selected
                )
                
            if game_state.merchant_open:
                room     = game_state.current_floor.get_current_room()
                merchant = room.special_state.get("merchant")
                if merchant:
                    draw_merchant_screen(
                        screen, font, font_small,
                        merchant,
                        game_state.player.gold,
                        game_state.merchant_selected
                    )    
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()