from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class GameState:
    """
    The single source of truth for the entire game run.
    Every system reads from and writes to GameState only.
    The Renderer reads GameState — it never modifies it.
    """
    player: object                          # Player instance
    current_floor: object                   # Floor instance
    floor_cache: Dict[int, object] = field(default_factory=dict)
    # floor_cache stores serialized floors by floor number
    # so backtracking restores exact state

    run_seed: int  = 0
    turn_count: int = 0

    # Controls which systems are active this frame
    game_phase: str = "exploring"
    # "exploring" "combat" "merchant" "gate" "transition"
    # "story"     "game_over"

    # Message logs
    messages: List[str]      = field(default_factory=list)
    story_message: Optional[str] = None
    # story_message is a single pinned string
    # replaced when a new story event fires

    # Story and quest flags — track narrative state across the run
    flags: Dict[str, bool] = field(default_factory=dict)
    # e.g. flags["journal_found"]  = True
    #      flags["voryn_spoke"]    = True
    #      flags["veil_weakened"]  = False
    
    # Inventory screen state
    inventory_open: bool = False
    inventory_selected: int = 0    # currently highlighted slot index

    def add_message(self, text):
        """Appends a general message to the log."""
        self.messages.append(text)

    def set_story_message(self, text):
        """
        Sets the pinned story panel message.
        Replaces whatever was there before.
        """
        self.story_message = text

    def set_flag(self, key, value=True):
        """Sets a named story flag."""
        self.flags[key] = value

    def get_flag(self, key):
        """Returns a story flag value. Defaults to False if not set."""
        return self.flags.get(key, False)