import json
import os
from pathlib import Path

# Save file location
SAVE_DIR  = Path(__file__).parent.parent.parent / "saves"
SAVE_FILE = SAVE_DIR / "savegame.json"

def ensure_save_dir():
    """Creates the saves directory if it doesn't exist."""
    SAVE_DIR.mkdir(exist_ok=True)

def save_exists():
    """Returns True if a save file exists."""
    return SAVE_FILE.exists()

def serialize_item(item):
    """Converts an Item object to a JSON-serializable dict."""
    return {
        "id":           item.id,
        "true_name":    item.true_name,
        "mystery_name": item.mystery_name,
        "category":     item.category,
        "identified":   item.identified,
        "rarity":       item.rarity,
        "quantity":     item.quantity,
        "cursed":       item.cursed,
        "lore":         item.lore,
        "damage_dice":  item.damage_dice,
        "atk_bonus":    item.atk_bonus,
        "def_bonus":    item.def_bonus,
        "slot":         item.slot,
        "effect":       item.effect,
        "effect_value": item.effect_value,
        "is_story_item":item.is_story_item,
        "floor_col":    item.floor_col,
        "floor_row":    item.floor_row,
    }

def deserialize_item(data):
    """Rebuilds an Item object from a dict."""
    from systems.inventory import Item
    return Item(
        id            = data["id"],
        true_name     = data["true_name"],
        mystery_name  = data["mystery_name"],
        category      = data["category"],
        identified    = data["identified"],
        rarity        = data["rarity"],
        quantity      = data["quantity"],
        cursed        = data["cursed"],
        lore          = data["lore"],
        damage_dice   = data["damage_dice"],
        atk_bonus     = data["atk_bonus"],
        def_bonus     = data["def_bonus"],
        slot          = data["slot"],
        effect        = data["effect"],
        effect_value  = data["effect_value"],
        is_story_item = data["is_story_item"],
        floor_col     = data["floor_col"],
        floor_row     = data["floor_row"],
    )

def serialize_player(player):
    """Converts the Player object to a JSON-serializable dict."""
    equipped_data = {}
    for slot, item in player.equipped.items():
        equipped_data[slot] = serialize_item(item) if item else None

    return {
        "name":              player.name,
        "level":             player.level,
        "hp":                player.hp,
        "max_hp":            player.max_hp,
        "atk":               player.atk,
        "def_":              player.def_,
        "spd":               player.spd,
        "lck":               player.lck,
        "xp":                player.xp,
        "xp_next":           player.xp_next,
        "gold":              player.gold,
        "col":               player.col,
        "row":               player.row,
        "current_floor":     player.current_floor,
        "inventory":         [serialize_item(i) for i in player.inventory],
        "inventory_cap":     player.inventory_cap,
        "equipped":          equipped_data,
        "story_items":       [serialize_item(i) for i in player.story_items],
        "abilities":         player.abilities,
        "oaths_sworn":       player.oaths_sworn,
        "playstyle_counters":player.playstyle_counters,
    }

def deserialize_player(data):
    """Rebuilds a Player object from a dict."""
    from entities.player import Player

    player = Player()
    player.name              = data["name"]
    player.level             = data["level"]
    player.hp                = data["hp"]
    player.max_hp            = data["max_hp"]
    player.atk               = data["atk"]
    player.def_              = data["def_"]
    player.spd               = data["spd"]
    player.lck               = data["lck"]
    player.xp                = data["xp"]
    player.xp_next           = data["xp_next"]
    player.gold              = data["gold"]
    player.col               = data["col"]
    player.row               = data["row"]
    player.current_floor     = data["current_floor"]
    player.inventory         = [deserialize_item(i) for i in data["inventory"]]
    player.inventory_cap     = data["inventory_cap"]
    player.story_items       = [deserialize_item(i) for i in data["story_items"]]
    player.abilities         = data["abilities"]
    player.oaths_sworn       = data["oaths_sworn"]
    player.playstyle_counters= data["playstyle_counters"]

    # Rebuild equipped dict
    player.equipped = {}
    for slot, item_data in data["equipped"].items():
        player.equipped[slot] = deserialize_item(item_data) if item_data else None

    return player

def serialize_tile(tile):
    """Converts a Tile to a dict."""
    return {
        "type":         tile.type,
        "walkable":     tile.walkable,
        "blocks_sight": tile.blocks_sight,
    }

def deserialize_tile(data):
    """Rebuilds a Tile from a dict."""
    from world.tile import Tile
    return Tile(
        type         = data["type"],
        walkable     = data["walkable"],
        blocks_sight = data["blocks_sight"],
    )

def serialize_room(room):
    """Converts a Room to a dict."""
    return {
        "id":              room.id,
        "name":            room.name,
        "description":     room.description,
        "room_type":       room.room_type,
        "width":           room.width,
        "height":          room.height,
        "tiles":           [[serialize_tile(t) for t in row] for row in room.tiles],
        "exits":           [
            {
                "direction":  e.direction,
                "leads_to":   e.leads_to,
                "discovered": e.discovered,
            }
            for e in room.exits
        ],
        "items":           [serialize_item(i) for i in room.items],
        "visited":         room.visited,
        "first_visit":     room.first_visit,
        "enemies_cleared": room.enemies_cleared,
    }

def deserialize_room(data):
    """Rebuilds a Room from a dict."""
    from world.room import Room, Exit

    tiles = [
        [deserialize_tile(t) for t in row]
        for row in data["tiles"]
    ]

    exits = [
        Exit(
            direction  = e["direction"],
            leads_to   = e["leads_to"],
            discovered = e["discovered"],
        )
        for e in data["exits"]
    ]

    return Room(
        id              = data["id"],
        name            = data["name"],
        description     = data["description"],
        room_type       = data["room_type"],
        width           = data["width"],
        height          = data["height"],
        tiles           = tiles,
        exits           = exits,
        items           = [deserialize_item(i) for i in data["items"]],
        visited         = data["visited"],
        first_visit     = data["first_visit"],
        enemies_cleared = data["enemies_cleared"],
    )

def serialize_floor(floor):
    """Converts a Floor to a dict. Enemies not saved — respawn on load."""
    from world.floor import GateRequirement

    return {
        "number":              floor.number,
        "rooms":               {k: serialize_room(v) for k, v in floor.rooms.items()},
        "start_room_id":       floor.start_room_id,
        "staircase_room_id":   floor.staircase_room_id,
        "player_current_room": floor.player_current_room,
        "seed":                floor.seed,
        "gate": {
            "floor_number": floor.gate_requirement.floor_number,
            "type":         floor.gate_requirement.type,
            "description":  floor.gate_requirement.description,
            "inscription":  floor.gate_requirement.inscription,
            "condition":    floor.gate_requirement.condition,
            "satisfied":    floor.gate_requirement.satisfied,
        }
    }

def deserialize_floor(data, run_seed):
    """
    Rebuilds a Floor from saved data.
    Restores room exploration state, items, and exits exactly.
    Respawns 60% of enemies that were killed — survivors stay put.
    Living enemies from the save are restored at their exact positions.
    """
    from world.floor import Floor, GateRequirement
    from world.dungeon_gen import generate_floor

    # Regenerate fresh floor to get base enemy pool
    fresh_floor = generate_floor(data["number"], run_seed)

    # Restore saved room state
    for room_id, room_data in data["rooms"].items():
        if room_id in fresh_floor.rooms:
            saved_room = deserialize_room(room_data)
            room       = fresh_floor.rooms[room_id]

            # Restore exploration state
            room.visited         = saved_room.visited
            room.first_visit     = saved_room.first_visit
            room.exits           = saved_room.exits
            room.items           = saved_room.items
            room.enemies_cleared = saved_room.enemies_cleared
            room.special_state   = saved_room.special_state

            # Enemy respawn logic — 60% of dead enemies respawn
            # Living enemies are not touched
            if saved_room.enemies_cleared:
                # Room was fully cleared — respawn 60% fresh
                import random
                original_count = len(room.enemies)
                respawn_count  = int(original_count * 0.6)
                room.enemies   = room.enemies[:respawn_count]
            # If not cleared — keep fresh enemies from generator
            # They represent enemies that were never killed

    fresh_floor.player_current_room        = data["player_current_room"]
    fresh_floor.gate_requirement.satisfied = data["gate"]["satisfied"]

    return fresh_floor

def save_game(game_state):
    """
    Serializes the complete game state to JSON.
    Saves player, current floor, all cached floors, and flags.
    """
    ensure_save_dir()

    # Serialize all cached floors plus current floor
    all_floors = {}
    for floor_num, floor in game_state.floor_cache.items():
        all_floors[str(floor_num)] = serialize_floor(floor)

    # Add current floor
    current = game_state.current_floor
    all_floors[str(current.number)] = serialize_floor(current)

    data = {
        "version":      "0.1.0",
        "run_seed":     game_state.run_seed,
        "turn_count":   game_state.turn_count,
        "game_phase":   game_state.game_phase,
        "player":       serialize_player(game_state.player),
        "current_floor_number": current.number,
        "floors":       all_floors,
        "flags":        game_state.flags,
        "messages":     game_state.messages[-20:],  # last 20 messages
        "story_message":game_state.story_message,
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_game():
    """
    Loads the game state from the save file.
    Returns a fully reconstructed GameState object.
    """
    from engine.game_state import GameState

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    run_seed = data["run_seed"]
    player   = deserialize_player(data["player"])

    # Rebuild all floors
    floors = {}
    for floor_num_str, floor_data in data["floors"].items():
        floor_num          = int(floor_num_str)
        floors[floor_num]  = deserialize_floor(floor_data, run_seed)

    current_floor_number = data["current_floor_number"]
    current_floor        = floors[current_floor_number]

    # Floor cache is everything except current floor
    floor_cache = {
        k: v for k, v in floors.items()
        if k != current_floor_number
    }

    game_state = GameState(
        player        = player,
        current_floor = current_floor,
        floor_cache   = floor_cache,
        run_seed      = run_seed,
    )

    game_state.turn_count    = data["turn_count"]
    game_state.game_phase    = data["game_phase"]
    game_state.flags         = data["flags"]
    game_state.messages      = data["messages"]
    game_state.story_message = data["story_message"]

    return game_state