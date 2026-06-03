# Floor represents one complete level of the Underspire.
# A floor is a graph of connected rooms — not a single large grid.
# The player navigates between rooms via exits.

from dataclasses import dataclass, field
from typing import Dict, Optional
from world.room import Room

@dataclass
class GateRequirement:
    floor_number: int
    type: str               # "carry" "speak" "defeat" "solve"
                            # "knowledge" "sacrifice" "sequence"
    description: str        # shown at the sealed staircase
    inscription: str        # carved text above the archway
    condition: Dict         # what must be true to open the gate
    satisfied: bool = False # flips to True when condition is met

@dataclass
class Floor:
    number: int                         # floor 1-10
    rooms: Dict[str, Room]              # room_id → Room
    start_room_id: str                  # where player arrives from above
    staircase_room_id: str              # where the descent staircase is
    gate_requirement: GateRequirement   # what seals the staircase
    seed: int                           # used to regenerate floor if needed
    player_current_room: str            # room_id of player's current room

    def get_current_room(self):
        """Returns the Room the player is currently in."""
        return self.rooms[self.player_current_room]

    def get_room(self, room_id):
        """Returns a Room by its id."""
        return self.rooms.get(room_id)