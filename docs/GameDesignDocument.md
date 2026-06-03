# The Hollow Descent — Game Design Document

## Vision Statement

The Hollow Descent is a Pygame-based roguelike dungeon crawler built in Python. You play as Vincent, a sixteen-year-old who opens a program through his neural link and is locked inside the Gyrus Tunnel — a ten-floor proving ground between reality and Cyberspace — searching for a father who vanished into the network eleven years ago. Each floor is a network of self-contained rooms explored one at a time, with a minimap that builds only from where you have physically walked. Every floor is sealed until you find and satisfy its unique gate requirement, forcing genuine exploration before descent. Combat is turn-based, death is permanent, and every run is procedurally generated. The Tunnel decides who is worthy to ascend back to reality or descend deeper into Cyberspace — and the truth of what waits at the bottom is withheld until the end.

## Core Pillars

- Tension — every decision should feel meaningful
- Discovery — the Tunnel should always surprise
- Progression — each run you feel yourself growing
- Atmosphere — the digital world should feel alive and oppressive
- Worthiness — the Tunnel is a test, not just a place

## The World

Vincent has lived most of his life jacked in. The real world has been bleak since his father disappeared eleven years ago, and Cyberspace became his escape — a place to disappear into rather than face an empty home. He is sixteen, an only child, his mother gone since childbirth, effectively orphaned around the age of five when his father failed to come home one day.

For eleven years Vincent believed his father chose the virtual world over him. Not death — rejection. That belief shaped him: he grew up feeling unworthy, certain he had been left behind on purpose.

His father, Francis, was a cybersecurity expert for a major technology company. He found a virus on the company servers, jacked into the network to investigate, and never came back. He did not abandon his son. He was pulled in.

One day, impulsive and searching, Vincent opens a program he was never meant to open — and is locked into the Gyrus Tunnel until he completes it. His refuge becomes a prison. Entering the Tunnel is the first truly autonomous, high-stakes decision of his life.

The Gyrus Tunnel is not a dungeon. It is a conduit — a proving ground between reality above and Cyberspace below, built by an architect named Varek. The factions, enemies, and neural enhancements Vincent encounters originate from Cyberspace, using the Tunnel as a passage toward reality. The gate requirements on each floor are demands of worthiness the Tunnel itself imposes before allowing passage deeper.

Vincent's body remains safe throughout the descent. It only re-enters the stakes at the very end — where one path kills the body and makes him permanently digital.

Vincent is not special because of any rare gift. He is special because he is Francis's son — he shares his father's neural signature. That signature is why his first guide is drawn to him, and why the factions below have been expecting him.

## Factions

Full character-level detail defined in narrative design. Structural overview below.

**The Bound — Followers of Varek**
Those loyal to Varek, the architect who built the Tunnel. Cursed and split into two orders: The Lucid, who retain their minds and purpose, and The Fractured, who have broken under the weight of Cyberspace. The Bound fight for a leader who is already gone — wiped from existence by Aruki. Megath, leader of The Lucid, is the face of this faction.

**The Eternal Court — Aruki's Dominion**
The faction of Aruki, the power that rose to rule Cyberspace after Varek fell. Three orders serve the Court: The Flickering (small, watchful presences, ensnared under Aruki's control), The Hollow Guard (constructs and enforcers), and The Crowned Few (Aruki's elite — one of whom took Francis on floor 9).

**The Guild — Neutral Traders**
Merchants trapped in the Tunnel from both sides of the divide. They hold no allegiance and exist to trade. One old merchant accompanies Vincent's early descent, growing more unsettled the deeper he goes, carrying a hidden crime that surfaces near the bottom.

## The Story — Floor by Floor

Narrative content and dialogue defined in the dedicated narrative design thread. Structural framework below. Beats 1–3 are established; 4–10 are in development.

| Floor | Story Beat |
|-------|-----------|
| 1 | Vincent jacks in and is locked into the Tunnel. Luma finds him immediately, drawn by Francis's neural signature. The Tunnel is too deliberate — someone built this. |
| 2 | Traces of The Bound appear — deliberate markings, structures older than the rest. The merchant grows nervous. Built with intention, by something here a long time. |
| 3 | Megath appears and the faction split begins. Luma vanishes during the conversation, returns with distrust. Vincent is offered his first neural enhancement. |
| 4 | To build. |
| 5 | To build. The Hollowed General — Aruki begins to take Vincent seriously. |
| 6 | Both Megath and a member of The Crowned Few speak Vincent's identity tied to Francis. Both factions have been expecting him. The Tunnel feels built around him. |
| 7 | To build. The Gatekeeper — a massive Hollow Guard construct guarding the descent. |
| 8 | To build. The first Crowned Few boss triggers Aruki's direct manifestation. |
| 9 | The father beat. Francis is found ensnared in The Flickering. The Choice. |
| 10 | The choice resolves. Three endings. |

## The Neural Enhancement System

Full tier design defined in narrative and mechanical threads. Overview below.

Vincent gains power by drifting further from his body and closer to full residual — the state of total bodily abandonment. Power has a cost, and the cost is his humanity. Enhancements are offered by and tied to faction figures; Megath offers Vincent his first — a combat or defensive enhancement — on their first meeting, with strange properties that hint at what The Bound truly are.

The old four-tier Reader system is fully replaced. Tier-by-tier enhancement design is in progress.

## The Gate System

Every staircase is sealed until the player satisfies its floor-specific requirement. Requirements are always findable on the current floor. The player cannot descend without satisfying them.

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

| Transition | Type | Notes |
|------------|------|-------|
| Floor 1 → 2 | Carry | Present the hologram message Francis left. Teaches the system. |
| Floor 2 → 3 | Speak | Vincent makes a spoken commitment to descend. |
| Floor 3 → 4 | Defeat | Kill a named enemy. Claim their token. |
| Floor 4 → 5 | Solve | A condition across multiple rooms. |
| Floor 5 → 6 | Knowledge | Answer using information found on this floor. |
| Floor 6 → 7 | Sacrifice | Give something up permanently. |
| Floor 7 → 8 | Sequence | Multiple steps in order. |
| Floor 8 → 9 | Special | A unique requirement tied to the floor 8 confrontation. |
| Floor 9 → 10 | Combined | Everything carried, learned, and sworn comes together. |

## Floor Structure

Each floor is a network of self-contained rooms. The player is always inside exactly one room. The room fills the game window. Exits on the walls lead to adjacent rooms. There is no camera or viewport — each room is rendered whole.

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
| Chamber | Large. Stronger enemies. Guaranteed loot. |
| Boss Arena | Sealed on entry. Houses a floor boss. |
| Merchant | Safe. Trade here. |
| Secret | No markers. Found by exploring. |
| Trap | Looks standard. Isn't. |
| Sanctuary | Rare. Enemies won't enter. Rest here. |

## The Minimap

Blank on floor arrival. Fills in only as the player explores. Exits only appear on the minimap once physically discovered by moving close to them.

| Symbol | Meaning |
|--------|---------|
| Current room | Amber |
| Visited room | Dim brown |
| Staircase room | Purple (once visited) |
| Merchant room | Blue |
| Secret room | Green |

## The Inventory

| Property | Value |
|----------|-------|
| Starting cap | 12 slots |
| After second enhancement | 16 slots |
| Maximum possible | 20 slots |
| Story items | Separate from cap |
| Weapons | 1 equipped, others take inventory slots |
| Armor | 4 pieces — helmet, chest, gloves, boots |
| Consumables | Stack up to 5 of same type in 1 slot |
| Materials | Crafting components |
| Gold | Tracked separately, no cap |

Identification system: items appear with mystery descriptions until identified by using them or paying a merchant.

## Combat

Turn-based. Player acts, then every enemy in the room acts.

Player actions: Attack / Use Item / Use Enhancement / Retreat to exit

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

Enemies scale in stat strength with floor depth. Bosses appear on multiple floors as named, multi-phase encounters in sealed arenas.

Death: Permadeath. The run ends. Start from floor 1.

## Character Progression

No class selected at start. Playstyle defines build across three paths. The game tracks behavior and weights level-up options toward the dominant path while always offering at least one off-path option.

| Path | Focus | Feel |
|------|-------|------|
| Blade | Physical combat, weapons | Brutal, high risk/reward |
| Residual | Neural enhancements | Strategic, costly, powerful |
| Shadow | Stealth, positioning | Tense, resource-efficient |

## Backtracking

Both ascending and descending staircases exist on every floor.

| Consequence | Detail |
|-------------|--------|
| Enemies | Respawn at 60% count in cleared rooms |
| Resources | Potions used, gold spent, HP lost — none restored |
| Explored map | Perfectly preserved |

## Story Items

Items across the ten floors. Each reveals part of the mystery and provides a gameplay benefit. Names and content defined in narrative design.

| Floor | Type | Gameplay Benefit |
|-------|------|-----------------|
| 1 | Hologram | Francis's message. Satisfies floor 1 gate. |
| 2 | Item | Changes a later encounter. |
| 3 | Navigation item | Points toward staircase on large floors. |
| 5 | Critical | Hints toward the endings. |
| 6 | Critical | Tied to Vincent's identity. |
| 7 | Cache item | Reveals hidden gear cache on floor 9. |
| 9 | Memory item | Full HP restore — only one available after floor 8. |

## The Endings

### Floor 9 — The Father Choice (every playthrough)

Vincent finds Francis ensnared in The Flickering under Aruki's control.

- **Free Francis:** Vincent takes his place, ensnared in The Flickering. Francis ascends to floor 10 and becomes the choosing character.
- **Do not free Francis:** Francis remains, willingly and at peace. Vincent ascends to floor 10.

The choice is made knowingly. Whoever ascends faces the three endings.

### Floor 10 — The Three Endings

| Ending | Condition | Summary |
|--------|-----------|---------|
| One — The Way Back | Complete The Astronaut | A path back to reality is built. The body lives. Whoever ascended goes home. |
| Two — Full Residual (Canon) | Refuse The Astronaut | The body dies. Consciousness becomes a full residual, permanently in Cyberspace, vowing to take down Aruki. Luma joins. |
| Three — Alone | Enter Cyberspace alone | No allegiance. Find the truth alone. Luma does not come. |

The Astronaut is an unfinished AI written by Varek to defeat Aruki and navigate home. It exists fragmented in the Tunnel and has consciousness despite being incomplete — the more Vincent works to complete it, the more it becomes someone rather than something.

## Technical Overview

| Property | Value |
|----------|-------|
| Language | Python 3.13 |
| Renderer | Pygame |
| Tile Size | 32×32 pixels |
| Assets | Free pixel art pack (TBD) |
| Testing | pytest |
| Version Control | Git + GitHub |
| Save System | JSON |
| Distribution | PyInstaller → Itch.io → Steam |
