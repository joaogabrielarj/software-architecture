#!/usr/bin/env python3
"""
Main Application - Event-Driven PyBoy Integration
Orchestrates the Event Bus, Event Processors, and PyBoy Emulator.
"""

import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.event_bus import EventBus
from src.event_processors import (
    BattleCounterProcessor,
    StepCounterProcessor,
    GameTimeTracker,
    HealthMonitor,
    InteractionTracker,
    ReportGenerator
)
from src.pyboy_wrapper import PyBoyEventWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('gameplay.log')
    ]
)
logger = logging.getLogger(__name__)


class GameApplication:
    """Main application orchestrating all components."""

    def __init__(self, rom_path: str, window_type: str = "SDL2"):
        """
        Initialize the application.

        Args:
            rom_path: Path to the Game Boy ROM file
            window_type: PyBoy window type (SDL2 for GUI, headless for no display)
        """
        logger.info("="*60)
        logger.info("Event-Driven PyBoy Application Starting")
        logger.info("="*60)

        # Initialize Event Bus
        self.event_bus = EventBus()
        logger.info("Event Bus created")

        # Initialize Event Processors
        self.processors = {
            "battle_counter": BattleCounterProcessor(self.event_bus),
            "step_counter": StepCounterProcessor(self.event_bus),
            "game_time": GameTimeTracker(self.event_bus),
            "health_monitor": HealthMonitor(self.event_bus),
            "interaction_tracker": InteractionTracker(self.event_bus)
        }

        # Initialize Report Generator (depends on processors)
        self.report_generator = ReportGenerator(self.event_bus, self.processors)
        self.processors["report_generator"] = self.report_generator

        logger.info(f"Initialized {len(self.processors)} event processors")

        # Initialize PyBoy Wrapper
        self.pyboy_wrapper = PyBoyEventWrapper(
            self.event_bus,
            rom_path,
            window_type=window_type
        )

        logger.info("All components initialized successfully")

    def run(self) -> None:
        """Run the main game loop."""
        try:
            # Start the emulator
            self.pyboy_wrapper.start()

            logger.info("\n" + "="*60)
            logger.info("Game is running! Use keyboard to control.")
            logger.info("Press Ctrl+C to stop and generate report.")
            logger.info("="*60 + "\n")

            # Main game loop
            running = True
            while running:
                running = self.pyboy_wrapper.tick()

        except KeyboardInterrupt:
            logger.info("\n\nKeyboard interrupt received. Stopping game...")

        except Exception as e:
            logger.error(f"Error during game execution: {e}", exc_info=True)

        finally:
            # Stop emulator and generate final report
            self.pyboy_wrapper.stop()
            logger.info("Application shut down successfully")

    def generate_manual_report(self) -> None:
        """Manually trigger report generation."""
        self.event_bus.publish("generate_report", {})


def main():
    """Entry point for the application."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Event-Driven PyBoy - Play Game Boy games with event tracking"
    )
    parser.add_argument(
        "rom",
        type=str,
        help="Path to the Game Boy ROM file (.gb or .gbc)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (headless mode)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate ROM file exists
    rom_path = Path(args.rom)
    if not rom_path.exists():
        logger.error(f"ROM file not found: {args.rom}")
        sys.exit(1)

    if not rom_path.suffix.lower() in ['.gb', '.gbc']:
        logger.warning(f"File extension '{rom_path.suffix}' is not a typical Game Boy ROM")

    # Determine window type
    window_type = "headless" if args.headless else "SDL2"

    # Create and run application
    try:
        app = GameApplication(str(rom_path), window_type=window_type)
        app.run()
    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
