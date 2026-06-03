from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class Item:
    """
    Represents any item in the game.
    Weapons, armor, consumables, materials, and story items
    all use this same structure with different fields populated.
    """
    id: str
    true_name: str              # shown when identified
    mystery_name: str           # shown when unidentified
    category: str               # "weapon" "armor" "consumable"
                                # "material" "story"
    identified: bool = False    # False = shows mystery_name
    rarity: str = "common"      # "common" "uncommon" "rare" "legendary"
    quantity: int = 1           # consumables stack up to 5
    cursed: bool = False        # cursed items can't be unequipped
    lore: str = ""              # read by Resonance ability later

    # Weapon stats
    damage_dice: str = ""       # e.g. "1d6" "2d4" "+2"
    atk_bonus: int = 0

    # Armor stats
    def_bonus: int = 0
    slot: str = ""              # "helmet" "chest" "gloves" "boots" "weapon"

    # Consumable effect
    effect: str = ""            # "heal" "identify" "teleport" etc
    effect_value: int = 0       # how much the effect does

    # Story item flag
    is_story_item: bool = False
    
    # Position on room floor (set when dropped)
    floor_col: int = 0
    floor_row: int = 0

    def display_name(self):
        """
        Returns the name to show the player.
        Unidentified items show their mystery name.
        """
        if self.identified:
            return self.true_name
        return self.mystery_name

    def short_desc(self):
        """
        Returns a short description for the inventory UI.
        """
        if not self.identified:
            return "???"

        if self.category == "weapon":
            return f"{self.damage_dice} ATK+{self.atk_bonus}"
        elif self.category == "armor":
            return f"DEF+{self.def_bonus}"
        elif self.category == "consumable":
            return f"{self.effect} {self.effect_value}"
        return ""


# ── Item definitions ──────────────────────────────────────────────
# Pre-built item instances used as templates by the loot system.
# The loot system copies these and assigns them to drops.

# Weapons
IRON_DAGGER = Item(
    id           = "iron_dagger",
    true_name    = "Iron Dagger",
    mystery_name = "a worn blade",
    category     = "weapon",
    identified   = True,
    rarity       = "common",
    damage_dice  = "1d4",
    atk_bonus    = 1,
    slot         = "weapon",
    lore         = "A simple blade. Many hands have held it."
)

IRON_SWORD = Item(
    id           = "iron_sword",
    true_name    = "Iron Sword",
    mystery_name = "a dull sword",
    category     = "weapon",
    identified   = True,
    rarity       = "common",
    damage_dice  = "2d4",
    atk_bonus    = 2,
    slot         = "weapon",
    lore         = "Standard issue. Nothing remarkable."
)

BONE_STAFF = Item(
    id           = "bone_staff",
    true_name    = "Bone Staff",
    mystery_name = "a pale staff",
    category     = "weapon",
    identified   = True,
    rarity       = "uncommon",
    damage_dice  = "1d6",
    atk_bonus    = 3,
    slot         = "weapon",
    lore         = "Carved from something that was once alive."
)

# Armor
LEATHER_CHEST = Item(
    id           = "leather_chest",
    true_name    = "Leather Chest",
    mystery_name = "worn leather",
    category     = "armor",
    identified   = True,
    rarity       = "common",
    def_bonus    = 3,
    slot         = "chest",
    lore         = "Cracked and stiff but better than nothing."
)

IRON_HELMET = Item(
    id           = "iron_helmet",
    true_name    = "Iron Helmet",
    mystery_name = "a dented helm",
    category     = "armor",
    identified   = True,
    rarity       = "common",
    def_bonus    = 2,
    slot         = "helmet",
    lore         = "A dent on the left side. Someone survived."
)

# Consumables
HEALTH_POTION = Item(
    id           = "health_potion",
    true_name    = "Health Potion",
    mystery_name = "a red potion",
    category     = "consumable",
    identified   = False,
    rarity       = "common",
    quantity     = 1,
    effect       = "heal",
    effect_value = 30,
    lore         = "Smells faintly of iron."
)

STRONG_POTION = Item(
    id           = "strong_potion",
    true_name    = "Strong Health Potion",
    mystery_name = "a dark red potion",
    category     = "consumable",
    identified   = False,
    rarity       = "uncommon",
    quantity     = 1,
    effect       = "heal",
    effect_value = 60,
    lore         = "Thick and warm."
)

SCROLL_OF_LIGHT = Item(
    id           = "scroll_of_light",
    true_name    = "Scroll of Light",
    mystery_name = "a pale scroll",
    category     = "consumable",
    identified   = False,
    rarity       = "uncommon",
    quantity     = 1,
    effect       = "reveal_map",
    effect_value = 0,
    lore         = "The ink glows faintly in the dark."
)

# Item pool by floor — used by loot system to pick appropriate drops
ITEM_POOL = {
    "common_weapons":    [IRON_DAGGER, IRON_SWORD],
    "uncommon_weapons":  [BONE_STAFF],
    "common_armor":      [LEATHER_CHEST, IRON_HELMET],
    "common_consumables":[HEALTH_POTION],
    "uncommon_consumables": [STRONG_POTION, SCROLL_OF_LIGHT],
}