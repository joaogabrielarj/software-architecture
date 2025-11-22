"""
PyBoy Wrapper - Integrates PyBoy emulator with the Event Bus.
Monitors game state and publishes events for processors to consume.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pyboy import PyBoy
from src.event_bus import EventBus
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PyBoyEventWrapper:
    """
    Wraps PyBoy emulator and publishes events to the Event Bus.
    Detects game state changes and emits appropriate events.
    """

    def __init__(self, event_bus: EventBus, rom_path: str, window_type: str = "SDL2"):
        """
        Initialize PyBoy wrapper.

        Args:
            event_bus: The event bus to publish events to
            rom_path: Path to the Game Boy ROM file
            window_type: PyBoy window type (SDL2, headless, etc.)
        """
        self.event_bus = event_bus
        self.rom_path = rom_path
        self.pyboy: Optional[PyBoy] = None
        self.window_type = window_type

        # Game state tracking
        self.previous_position = None
        self.previous_health = None
        self.in_battle = False
        self.step_count = 0
        self.frame_count = 0

        # Configuration
        self.frames_per_step_check = 60  # Check for steps every ~1 second at 60 FPS

        logger.info(f"PyBoyEventWrapper initialized with ROM: {rom_path}")

    def start(self) -> None:
        """Start the PyBoy emulator."""
        try:
            self.pyboy = PyBoy(
                self.rom_path,
                window_type=self.window_type
            )
            logger.info("PyBoy emulator started successfully")
            self.event_bus.publish("game_started", {"rom": self.rom_path})
        except Exception as e:
            logger.error(f"Failed to start PyBoy: {e}")
            raise

    def stop(self) -> None:
        """Stop the PyBoy emulator."""
        if self.pyboy:
            self.event_bus.publish("game_ended", {
                "total_frames": self.frame_count,
                "total_steps": self.step_count
            })
            self.pyboy.stop()
            logger.info("PyBoy emulator stopped")

    def tick(self) -> bool:
        """
        Process one frame of emulation and emit events.

        Returns:
            True if emulator is still running, False otherwise
        """
        if not self.pyboy:
            return False

        try:
            # Tick the emulator for one frame
            self.pyboy.tick()
            self.frame_count += 1

            # Check game state periodically to detect events
            if self.frame_count % self.frames_per_step_check == 0:
                self._check_for_events()

            return not self.pyboy.stopped
        except Exception as e:
            logger.error(f"Error during emulation tick: {e}")
            return False

    def _check_for_events(self) -> None:
        """Check game state and publish appropriate events."""
        try:
            # Get current game state from memory
            # Note: Memory addresses are game-specific (these are examples for Pokémon)
            current_position = self._get_player_position()
            current_health = self._get_player_health()
            in_battle = self._is_in_battle()

            # Detect movement/steps
            if current_position != self.previous_position and current_position is not None:
                self._handle_movement(current_position)
                self.previous_position = current_position

            # Detect battle start/end
            if in_battle and not self.in_battle:
                self._handle_battle_start()
            elif not in_battle and self.in_battle:
                self._handle_battle_end()

            self.in_battle = in_battle

            # Detect health changes
            if current_health != self.previous_health and current_health is not None:
                self._handle_health_change(current_health)
                self.previous_health = current_health

        except Exception as e:
            logger.debug(f"Error checking game events: {e}")

    def _get_player_position(self) -> Optional[tuple]:
        """
        Get current player position from game memory.
        Memory addresses are game-specific.
        """
        try:
            # Example memory addresses for Pokémon Red/Blue
            # These would need to be adjusted for specific games
            x_pos = self.pyboy.get_memory_value(0xD362)
            y_pos = self.pyboy.get_memory_value(0xD361)
            map_id = self.pyboy.get_memory_value(0xD35E)
            return (x_pos, y_pos, map_id)
        except:
            return None

    def _get_player_health(self) -> Optional[int]:
        """Get current player health from game memory."""
        try:
            # Example memory address for Pokémon Red/Blue
            # Current HP of first Pokémon in party
            hp_high = self.pyboy.get_memory_value(0xD16C)
            hp_low = self.pyboy.get_memory_value(0xD16D)
            return (hp_high << 8) | hp_low
        except:
            return None

    def _is_in_battle(self) -> bool:
        """Check if currently in a battle."""
        try:
            # Example memory address for Pokémon Red/Blue
            # Battle type indicator (0 = no battle)
            battle_type = self.pyboy.get_memory_value(0xD057)
            return battle_type != 0
        except:
            return False

    def _handle_movement(self, new_position: tuple) -> None:
        """Handle player movement event."""
        if self.previous_position is None:
            return

        old_x, old_y, old_map = self.previous_position
        new_x, new_y, new_map = new_position

        # Determine direction if on same map
        if old_map == new_map:
            direction = "unknown"
            if new_x > old_x:
                direction = "right"
            elif new_x < old_x:
                direction = "left"
            elif new_y > old_y:
                direction = "down"
            elif new_y < old_y:
                direction = "up"

            self.step_count += 1
            self.event_bus.publish("player_moved", {
                "direction": direction,
                "position": new_position,
                "step_number": self.step_count
            })

    def _handle_battle_start(self) -> None:
        """Handle battle start event."""
        logger.info("Battle started!")
        self.event_bus.publish("battle_started", {
            "frame": self.frame_count
        })

    def _handle_battle_end(self) -> None:
        """Handle battle end event."""
        logger.info("Battle ended!")
        # Try to determine battle result
        result = "unknown"  # Would need game-specific logic
        self.event_bus.publish("battle_ended", {
            "frame": self.frame_count,
            "result": result
        })

    def _handle_health_change(self, new_health: int) -> None:
        """Handle health change event."""
        if self.previous_health is None:
            return

        health_delta = new_health - self.previous_health

        if health_delta < 0:
            # Player took damage
            self.event_bus.publish("player_damaged", {
                "damage": abs(health_delta),
                "current_health": new_health,
                "previous_health": self.previous_health
            })

            if new_health == 0:
                self.event_bus.publish("player_fainted", {
                    "frame": self.frame_count
                })
        elif health_delta > 0:
            # Player healed
            self.event_bus.publish("player_healed", {
                "healing": health_delta,
                "current_health": new_health,
                "previous_health": self.previous_health
            })

    def press_button(self, button: str) -> None:
        """
        Simulate button press.

        Args:
            button: Button name (up, down, left, right, a, b, start, select)
        """
        if not self.pyboy:
            return

        button_map = {
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
            "a": "a",
            "b": "b",
            "start": "start",
            "select": "select"
        }

        if button.lower() in button_map:
            self.pyboy.send_input(button_map[button.lower()])
            logger.debug(f"Button pressed: {button}")

    def get_screen_image(self):
        """Get current screen image."""
        if self.pyboy:
            return self.pyboy.screen_image()
        return None

    def save_state(self, filename: str) -> None:
        """Save emulator state to file."""
        if self.pyboy:
            with open(filename, "wb") as f:
                self.pyboy.save_state(f)
            logger.info(f"State saved to {filename}")

    def load_state(self, filename: str) -> None:
        """Load emulator state from file."""
        if self.pyboy:
            with open(filename, "rb") as f:
                self.pyboy.load_state(f)
            logger.info(f"State loaded from {filename}")
