import random
from dataclasses import dataclass, field
from typing import Optional

def roll_dice(notation):
    """
    Rolls dice from standard notation string.
    Examples: "1d6" "2d4" "1d8+2"
    Returns the integer result.
    """
    bonus = 0
    if "+" in notation:
        notation, bonus_str = notation.split("+")
        bonus = int(bonus_str)

    count, sides = notation.split("d")
    count = int(count)
    sides = int(sides)

    return sum(random.randint(1, sides) for _ in range(count)) + bonus

@dataclass
class CombatResult:
    """
    Holds the result of a single combat exchange.
    Now includes loot dropped on enemy death.
    """
    hit: bool
    damage: int
    is_crit: bool
    target_died: bool
    xp_gained: int
    gold_dropped: int           # gold dropped on death
    item_dropped: object        # Item or None
    message: str

def resolve_player_attack(player, enemy, floor_number=1):
    """
    Resolves one attack from Vincent against an enemy.
    Rolls loot on enemy death and includes it in the result.

    Formula:
      base      = roll weapon dice
      total_atk = base + player.atk
      damage    = max(1, total_atk - enemy.def_)
      crit      = LCK * 0.01 chance to double damage
    """
    # Use equipped weapon dice if available, otherwise unarmed
    if hasattr(player, 'equipped') and player.equipped.get("weapon"):
        weapon     = player.equipped["weapon"]
        dice       = weapon.damage_dice if weapon.damage_dice else "1d6"
        atk_bonus  = weapon.atk_bonus
    else:
        dice      = "1d6"    # unarmed
        atk_bonus = 0

    base      = roll_dice(dice)
    total_atk = base + player.atk + atk_bonus
    damage    = max(1, total_atk - enemy.def_)

    # Critical hit check
    crit_chance = player.lck * 0.01
    is_crit     = random.random() < crit_chance
    if is_crit:
        damage *= 2

    # Apply damage
    enemy.hp   -= damage
    target_died = enemy.hp <= 0

    if target_died:
        enemy.hp    = 0
        enemy.alive = False

    # Roll loot if enemy died
    gold_dropped = 0
    item_dropped = None

    if target_died:
        from systems.loot import roll_loot
        gold_dropped, item_dropped = roll_loot(enemy, floor_number)

    # Build message
    if is_crit:
        message = f"Critical hit! You strike {enemy.name} for {damage} damage."
    else:
        message = f"You attack {enemy.name} for {damage} damage."

    if target_died:
        message += f" {enemy.name} is slain."

    return CombatResult(
        hit          = True,
        damage       = damage,
        is_crit      = is_crit,
        target_died  = target_died,
        xp_gained    = enemy.xp_reward if target_died else 0,
        gold_dropped = gold_dropped,
        item_dropped = item_dropped,
        message      = message
    )

def resolve_enemy_attack(enemy, player):
    """
    Resolves one attack from an enemy against Vincent.
    Returns a message string and damage value.
    """
    base      = roll_dice("1d4")
    total_atk = base + enemy.atk
    damage    = max(1, total_atk - player.def_)

    player.hp -= damage

    message = f"{enemy.name} strikes you for {damage} damage."

    if player.hp <= 0:
        player.hp = 0
        message  += " You have been slain."

    return message, damage

def check_level_up(player):
    """
    Checks if the player has enough XP to level up.
    Returns True if a level up occurred.
    """
    if player.xp < player.xp_next:
        return False

    player.level  += 1
    player.xp     -= player.xp_next
    player.xp_next = int(100 * (player.level ** 1.5))

    # Stat increases
    player.max_hp += 15
    player.hp      = player.max_hp
    player.atk    += 2
    player.def_   += 1

    return True