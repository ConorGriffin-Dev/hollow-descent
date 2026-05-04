import random
from dataclasses import dataclass
from typing import Optional

def roll_dice(notation):
    """
    Rolls dice from standard notation string.
    Examples: "1d6" "2d4" "1d8+2"
    Returns the integer result.
    """
    # Split on + for bonus
    bonus = 0
    if "+" in notation:
        notation, bonus_str = notation.split("+")
        bonus = int(bonus_str)

    # Split on d for count and sides
    count, sides = notation.split("d")
    count = int(count)
    sides = int(sides)

    return sum(random.randint(1, sides) for _ in range(count)) + bonus

@dataclass
class CombatResult:
    """
    Holds the result of a single combat exchange.
    Returned by resolve_player_attack() so the game loop
    can log messages and update state cleanly.
    """
    hit: bool                       # did the attack land
    damage: int                     # damage dealt
    is_crit: bool                   # was it a critical hit
    target_died: bool               # did the target die
    xp_gained: int                  # XP awarded if target died
    message: str                    # human readable result message

def resolve_player_attack(player, enemy):
    """
    Resolves one attack from Vincent against an enemy.

    Formula from TDD:
      base      = roll weapon dice (default 1d6 unarmed)
      total_atk = base + player.atk
      damage    = max(1, total_atk - enemy.def_)
      crit      = random() < player.lck * 0.01 → damage * 2

    Returns a CombatResult dataclass.
    """
    # Roll base damage — unarmed for now, weapon dice added in Phase 2
    base      = roll_dice("1d6")
    total_atk = base + player.atk
    damage    = max(1, total_atk - enemy.def_)

    # Check for critical hit
    crit_chance = player.lck * 0.01
    is_crit     = random.random() < crit_chance
    if is_crit:
        damage *= 2

    # Apply damage to enemy
    enemy.hp   -= damage
    target_died = enemy.hp <= 0

    if target_died:
        enemy.hp    = 0
        enemy.alive = False

    # Build result message
    if is_crit:
        message = f"Critical hit! You strike {enemy.name} for {damage} damage."
    else:
        message = f"You attack {enemy.name} for {damage} damage."

    if target_died:
        message += f" {enemy.name} is slain."

    return CombatResult(
        hit         = True,
        damage      = damage,
        is_crit     = is_crit,
        target_died = target_died,
        xp_gained   = enemy.xp_reward if target_died else 0,
        message     = message
    )

def resolve_enemy_attack(enemy, player):
    """
    Resolves one attack from an enemy against Vincent.

    Formula mirrors player attack but uses enemy stats.
    Enemies deal minimum 1 damage even against high DEF.

    Returns a message string for the log.
    """
    base      = roll_dice("1d4")
    total_atk = base + enemy.atk
    damage    = max(1, total_atk - player.def_)

    # Apply damage to player
    player.hp -= damage

    message = f"{enemy.name} strikes you for {damage} damage."

    if player.hp <= 0:
        player.hp = 0
        message  += " You have been slain."

    return message, damage

def check_level_up(player):
    """
    Checks if the player has enough XP to level up.
    Increases level, recalculates stats, resets XP threshold.
    Returns True if a level up occurred.
    """
    if player.xp < player.xp_next:
        return False

    player.level   += 1
    player.xp      -= player.xp_next

    # XP threshold scales with level — each level needs more XP
    player.xp_next  = int(100 * (player.level ** 1.5))

    # Stat increases on level up
    player.max_hp  += 15
    player.hp       = player.max_hp   # full heal on level up
    player.atk     += 2
    player.def_    += 1

    return True