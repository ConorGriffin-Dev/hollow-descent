The Hollow Descent — Game Design Document

Vision Statement

The Hollow Descent is a Pygame-based roguelike dungeon crawler built in Python.
You play as a young Reader — someone born with the rare ability to perceive a
hidden layer of reality — who descends into an ancient structure called the
Underspire searching for a father who disappeared eleven years ago. Each of the
ten floors is a network of self-contained rooms explored one at a time, with a
minimap that builds only from where you have physically walked. Every floor is
sealed until you find and satisfy its unique gate requirement, forcing genuine
exploration before descent. Combat is turn-based, death is permanent, and every
run is procedurally generated. Completing all ten floors transitions the boy into
a vast fantasy world — the true destination the Underspire has been preparing him
for all along.

Core Pillars

- Tension — every decision should feel meaningful
- Discovery — the dungeon should always surprise
- Progression — each run you feel yourself growing
- Atmosphere — the world should feel alive and dark
- Worthiness — the dungeon is a test, not just a place

The World

The wider world to Vincent (The MC) is vastly unknown, as he has never left his farm and the surrounding village, once he was of age (16) he began asking questions about the disapperance of your father.
until one morning whilst working the farm, he falls and stumples into a crack between the earth revealing a small cavernous hollow under the land with a door looking right at him, with a note pinned to it.

  "Who ever finds this will uncover mysteries and wonders we above were never supposed to find" Signed F (Francis, father of Vincent)

The Underspire is not a dungeon. It is a threshold — a proving ground between
the overworld and a vast realm below. The factions, enemies, and magic
Vincent encounters are not native to the dungeon. They are from the world below,
using the Underspire as a conduit to push into the overworld above. The gate
requirements on each floor are underworld artifacts and commitments — proof of
worthiness demanded by the world below before it allows entry.

******
Factions

Names and full details to be defined by the designer at Phase 3.

Faction A — The Tragic Knights
Once noble. Followed a king into the Underspire centuries ago and never
returned as themselves. They remember who they were. Some will speak. Some
will beg to be ended. Some will try to recruit you.

*Faction B — The Hollowed
People who descended seeking something and lost themselves. The Underspire
took their names, faces, and reasons. They hoard items obsessively —
including story items sometimes.

*Faction C — The Veilborn
Native to the world below. Not human. They don't attack on sight — they
watch. They have their own politics and hierarchy. By floor 6 it becomes
clear they have been expecting someone like the boy for a very long time.

*Faction D — The Stranded Company
A mercenary group that entered the Underspire months ago on contract.
Scattered across multiple floors, depleted. Some have gone feral. Others
maintain discipline and will trade. Their captain knows things she shouldn't.
******

******
The Story — Floor by Floor

*Specific narrative content, character names, and dialogue to be defined
by the designer at Phase 3. The following is the structural framework.

| Floor | Story Beat |
|-------|-----------|
| 1-2 | The dungeon is too deliberate. Someone built this for a reason. |
| 3-4 | Faction A is guarding something below. One named member knew the boy's father. |
| 5 | The father's journal is found. He got far. He found something on floor 8 that should not exist. |
| 6 | A Veilborn speaks the boy's true name — the one only his father knew. |
| 7 | The mercenary captain reveals the truth. The Underspire is a tomb for something that isn't dead. The Veil has been weakening for thirty years. |
| 8 | A chamber with no door. Walls in an ancient language. Something made of collapsed light says: "You took long enough." |
| 9 | The father didn't disappear. He made a deal — bound himself to the entity to slow the Veil's collapse. He is still alive. Barely. The deal ends now. |
| 10 | The choice. Three endings. One secret. |
******

******
The Magic System

*System name and full lore to be defined by the designer at Phase 3.*

The boy is a Reader — someone who perceives a hidden layer of reality beneath
the physical world. This ability deepens as he descends.

| Tier | Name | Floor Unlocked | Cost | Effect |
|------|------|---------------|------|--------|
| 1 | Perception | 1 | None | Story items glow. Exits discovered faster. Passive. |
| 2 | Resonance | 3 | Requires story item | Touch an object — see its last moment of significance. |
| 3 | Inscription | 5 | HP | Mark a wall — enemies cannot perceive it. Mark a weapon — bypasses armor. |
| 4 | Unmaking | 8 | Severe | Destroy meaning, not matter. Enemy forgets why it fights. Door forgets it is a door. |
******


The Gate System

Every staircase is sealed until the player satisfies its floor-specific
requirement. Requirements are always findable on the current floor.
The player cannot descend without satisfying them.

Gate requirement types:

| Type | Description |
|------|-------------|
| Carry | Find and carry a specific item to the staircase |
| Speak | Make a spoken commitment at the staircase |
| Defeat | A specific named enemy must be dead |
| Solve | A condition across the floor must be met |
| Knowledge | Answer what the staircase asks using found information |
| Sacrifice | Give something up permanently |
| Sequence | Multiple steps completed in order |

*Specific gate content for each floor to be defined at Phase 3.*

| Transition | Type | Notes |
|------------|------|-------|
| Floor 1 → 2 | Carry | Simple. Teaches the system. |
| Floor 2 → 3 | Speak | The dungeon wants words. |
| Floor 3 → 4 | Defeat | Kill a named enemy. Claim their token. |
| Floor 4 → 5 | Solve | A condition across multiple rooms. |
| Floor 5 → 6 | Knowledge | Answer using information found on this floor. |
| Floor 6 → 7 | Sacrifice | Give something up permanently. |
| Floor 7 → 8 | Sequence | Multiple steps in order. |
| Floor 8 → 9 | Reader | Requires Reader ability to satisfy. |
| Floor 9 → 10 | Combined | Everything carried, learned, and sworn comes together. |

Floor Structure

Each floor is a network of self-contained rooms. The player is always inside
exactly one room. The room fills the game window. Exits on the walls lead to
adjacent rooms.

Floor size by room count:

| Floor | Room Count |
|-------|-----------|
| 1 | 8-10 |
| 2 | 10-12 |
| 3 | 12-14 |
| 4 | 14-16 |
| 5 | 16-18 |
| 6 | 18-20 |
| 7 | 20-23 |
| 8 | 23-26 |
| 9 | 26-29 |
| 10 | 30-35 |

Room types:

| Type | Description |
|------|-------------|
| Standard | Most common. Enemies, loot, or nothing. |
| Corridor | Narrow connector. Occasional ambush. |
| Chamber | Large. Stronger enemies. Guaranteed loot. |
| Boss Antechamber | One in, one out. Final preparation before descent. |
| Merchant | Door closes behind you. Safe. Trade here. |
| Secret | No markers. Found by exploring walls. |
| Trap | Looks standard. Isn't. |
| Sanctuary | Rare. Enemies won't enter. Rest here. |

The Minimap

Blank on floor arrival. Fills in only as the player explores. Exits only
appear on the minimap once physically discovered by moving close to them.

| Symbol | Meaning |
|--------|---------|
| [▶] | Current room |
| [■] | Visited room |
| [▼] | Staircase down (only shown once visited) |
| [▲] | Staircase up (only shown once visited) |
| [!] | Story item room |
| [S] | Merchant room |
| [☠] | Room where HP dropped below 20% |

The Inventory

| Property | Value |
|----------|-------|
| Starting cap | 12 slots |
| After second oath | 16 slots |
| Maximum possible | 20 slots (legendary item) |
| Story items | Count toward cap before second oath. Free slot after. |
| Weapons | 1 equipped, others take inventory slots |
| Armor | 4 pieces — helmet, chest, gloves, boots |
| Consumables | Stack up to 5 of same type in 1 slot |
| Materials | Crafting components |
| Gold | Tracked separately, no cap |

Identification system:
Items appear with mystery descriptions until identified. Identified by:
scroll, Resonance ability, using it, or paying a merchant.

| Mystery Description | Possible True Identity |
|--------------------|----------------------|
| "a murky grey potion" | Potion of Fortitude or Weakness |
| "a black-edged scroll" | Scroll of Flame or Unmaking |
| "a tarnished copper ring" | Ring of Luck or Cursed Binding |
potentially more to be added

Combat

Turn-based. Player acts, then every enemy in the room acts.

Player actions: Attack / Use Item / Use Ability / Retreat to exit

Damage formula:
base        =  roll weapon dice (e.g. 2d4)
total_atk   =  base + ATK stat
damage      =  max(1, total_atk - defender DEF)
crit        =  LCK * 0.01 chance to double damage

Enemy behaviors:

| Behavior | Description | Floors |
|----------|-------------|--------|
| Aggressive | Always paths toward player | 1+ |
| Ranged | Maintains distance, attacks from far | 1+ |
| Patrol | Fixed route until player spotted, then chases | 2+ |
| Coward | Retreats when HP is low | 2+ |
| Coordinator | Flanks simultaneously with another enemy | 3+ |
| Adapter | Changes behavior based on player actions | 7+ |

Death: Permadeath. The run ends. Start from floor 1.

Character Progression

No class selected at start. Playstyle defines build across three paths.
The game tracks behavior and weights level-up perk options toward the
dominant path while always offering at least one off-path option.

| Path | Focus | Feel |
|------|-------|------|
| Blade | Physical combat, weapons | Brutal, high risk/reward |
| Reader | Magic abilities, oaths | Strategic, costly, powerful |
| Shadow | Stealth, positioning | Tense, resource-efficient |

Backtracking

Both ascending and descending staircases always exist on every floor.

| Consequence | Detail |
|-------------|--------|
| Enemies | Respawn at 60% count in random positions |
| Resources | Potions used, gold spent, HP lost — none restored |
| Story time | Certain timed story elements advance |
| Explored map | Perfectly preserved |

******
Story Items

Nine items across ten floors. Each reveals part of the mystery and provides
a gameplay benefit. All nine are required for the secret ending.

*Item names and specific content to be defined at Phase 3.*

| Floor | Type | Gameplay Benefit |
|-------|------|-----------------|
| 1 | Carry item | Opens locked doors on floor 2 |
| 2 | NPC item | Changes a named enemy encounter on floor 4 |
| 3 | Navigation item | Points toward staircase on large floors |
| 5 | CRITICAL | Father's journal. Hints at secret ending. |
| 6 | CRITICAL | Required for secret ending. No exceptions. |
| 7 | Cache item | Reveals hidden gear cache on floor 9 |
| 9 | Memory item | Full HP restore — only one available after floor 8 |
******

******
The Three Endings

*Full ending content to be written at Phase 3.*

| Ending | Condition | Summary |
|--------|-----------|---------|
| One | Default | Take the father's place. He goes free. You stay. |
| Two | Default | Destroy the entity. The Veil collapses. Everything inside releases. |
| Three (Secret) | All story items + Veilborn Cipher | A third option the entity doesn't want found. Your father's journal hinted at it. |
******

Technical Overview

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Renderer | Pygame |
| Tile Size | 32×32 pixels |
| Assets | Free pixel art pack (TBD) |
| Testing | pytest |
| Version Control | Git + GitHub |
| Containerisation | Docker |
| Save System | JSON |
| Distribution | GitHub → Itch.io → Steam |