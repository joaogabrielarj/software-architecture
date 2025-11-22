"""
Event Processors - Handle specific events and maintain statistics.
Each processor is responsible for a specific aspect of game tracking.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.event_bus import Event, EventBus
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BattleCounterProcessor:
    """Tracks the number of battles that occur during gameplay."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.battle_count = 0
        self.battles_won = 0
        self.battles_lost = 0
        self.last_battle_time = None

        # Subscribe to battle events
        self.event_bus.subscribe("battle_started", self.on_battle_started)
        self.event_bus.subscribe("battle_ended", self.on_battle_ended)
        logger.info("BattleCounterProcessor initialized")

    def on_battle_started(self, event: Event) -> None:
        """Handle battle start event."""
        self.battle_count += 1
        self.last_battle_time = event.timestamp
        logger.info(f"Battle #{self.battle_count} started at {event.timestamp}")

    def on_battle_ended(self, event: Event) -> None:
        """Handle battle end event."""
        result = event.data.get("result", "unknown")
        if result == "won":
            self.battles_won += 1
        elif result == "lost":
            self.battles_lost += 1
        logger.info(f"Battle ended: {result}")

    def get_statistics(self) -> Dict[str, Any]:
        """Return battle statistics."""
        return {
            "total_battles": self.battle_count,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,
            "win_rate": self.battles_won / self.battle_count if self.battle_count > 0 else 0,
            "last_battle_time": self.last_battle_time
        }


class StepCounterProcessor:
    """Tracks the number of steps the player takes in the game."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.step_count = 0
        self.steps_by_direction = {"up": 0, "down": 0, "left": 0, "right": 0}

        # Subscribe to step events
        self.event_bus.subscribe("player_moved", self.on_player_moved)
        logger.info("StepCounterProcessor initialized")

    def on_player_moved(self, event: Event) -> None:
        """Handle player movement event."""
        self.step_count += 1
        direction = event.data.get("direction", "unknown")

        if direction in self.steps_by_direction:
            self.steps_by_direction[direction] += 1

        if self.step_count % 100 == 0:
            logger.info(f"Player has taken {self.step_count} steps")

    def get_statistics(self) -> Dict[str, Any]:
        """Return step statistics."""
        return {
            "total_steps": self.step_count,
            "steps_by_direction": self.steps_by_direction.copy()
        }


class GameTimeTracker:
    """Tracks gameplay time and session information."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.start_time = None
        self.end_time = None
        self.pause_count = 0
        self.total_pause_duration = 0
        self.current_pause_start = None

        # Subscribe to game lifecycle events
        self.event_bus.subscribe("game_started", self.on_game_started)
        self.event_bus.subscribe("game_ended", self.on_game_ended)
        self.event_bus.subscribe("game_paused", self.on_game_paused)
        self.event_bus.subscribe("game_resumed", self.on_game_resumed)
        logger.info("GameTimeTracker initialized")

    def on_game_started(self, event: Event) -> None:
        """Handle game start event."""
        self.start_time = event.timestamp
        logger.info(f"Game started at {self.start_time}")

    def on_game_ended(self, event: Event) -> None:
        """Handle game end event."""
        self.end_time = event.timestamp
        logger.info(f"Game ended at {self.end_time}")

    def on_game_paused(self, event: Event) -> None:
        """Handle game pause event."""
        self.pause_count += 1
        self.current_pause_start = event.timestamp
        logger.info("Game paused")

    def on_game_resumed(self, event: Event) -> None:
        """Handle game resume event."""
        if self.current_pause_start:
            pause_duration = (event.timestamp - self.current_pause_start).total_seconds()
            self.total_pause_duration += pause_duration
            self.current_pause_start = None
            logger.info(f"Game resumed after {pause_duration:.2f}s pause")

    def get_statistics(self) -> Dict[str, Any]:
        """Return time statistics."""
        if not self.start_time:
            return {"status": "not_started"}

        end = self.end_time or datetime.now()
        total_duration = (end - self.start_time).total_seconds()
        active_duration = total_duration - self.total_pause_duration

        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_duration_seconds": total_duration,
            "active_duration_seconds": active_duration,
            "pause_count": self.pause_count,
            "total_pause_duration_seconds": self.total_pause_duration
        }


class HealthMonitor:
    """Monitors player health and damage events."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.damage_taken = 0
        self.healing_received = 0
        self.knockouts = 0
        self.current_health = 100
        self.max_health = 100

        # Subscribe to health events
        self.event_bus.subscribe("player_damaged", self.on_player_damaged)
        self.event_bus.subscribe("player_healed", self.on_player_healed)
        self.event_bus.subscribe("player_fainted", self.on_player_fainted)
        logger.info("HealthMonitor initialized")

    def on_player_damaged(self, event: Event) -> None:
        """Handle damage event."""
        damage = event.data.get("damage", 0)
        self.damage_taken += damage
        self.current_health = max(0, self.current_health - damage)
        logger.debug(f"Player took {damage} damage. Current health: {self.current_health}")

    def on_player_healed(self, event: Event) -> None:
        """Handle healing event."""
        healing = event.data.get("healing", 0)
        self.healing_received += healing
        self.current_health = min(self.max_health, self.current_health + healing)
        logger.debug(f"Player healed {healing}. Current health: {self.current_health}")

    def on_player_fainted(self, event: Event) -> None:
        """Handle faint/knockout event."""
        self.knockouts += 1
        self.current_health = 0
        logger.info(f"Player fainted! Total knockouts: {self.knockouts}")

    def get_statistics(self) -> Dict[str, Any]:
        """Return health statistics."""
        return {
            "current_health": self.current_health,
            "max_health": self.max_health,
            "total_damage_taken": self.damage_taken,
            "total_healing_received": self.healing_received,
            "knockouts": self.knockouts,
            "net_damage": self.damage_taken - self.healing_received
        }


class InteractionTracker:
    """Tracks player interactions with NPCs and objects."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.npc_interactions = 0
        self.items_collected = 0
        self.doors_opened = 0
        self.menus_opened = 0

        # Subscribe to interaction events
        self.event_bus.subscribe("npc_interaction", self.on_npc_interaction)
        self.event_bus.subscribe("item_collected", self.on_item_collected)
        self.event_bus.subscribe("door_opened", self.on_door_opened)
        self.event_bus.subscribe("menu_opened", self.on_menu_opened)
        logger.info("InteractionTracker initialized")

    def on_npc_interaction(self, event: Event) -> None:
        """Handle NPC interaction event."""
        self.npc_interactions += 1
        logger.debug(f"NPC interaction #{self.npc_interactions}")

    def on_item_collected(self, event: Event) -> None:
        """Handle item collection event."""
        self.items_collected += 1
        item_name = event.data.get("item", "unknown")
        logger.debug(f"Item collected: {item_name}")

    def on_door_opened(self, event: Event) -> None:
        """Handle door opening event."""
        self.doors_opened += 1

    def on_menu_opened(self, event: Event) -> None:
        """Handle menu opening event."""
        self.menus_opened += 1

    def get_statistics(self) -> Dict[str, Any]:
        """Return interaction statistics."""
        return {
            "npc_interactions": self.npc_interactions,
            "items_collected": self.items_collected,
            "doors_opened": self.doors_opened,
            "menus_opened": self.menus_opened
        }


class ReportGenerator:
    """Generates comprehensive reports from all event processors."""

    def __init__(self, event_bus: EventBus, processors: Dict[str, Any]):
        self.event_bus = event_bus
        self.processors = processors
        self.reports_generated = 0

        # Subscribe to report request events
        self.event_bus.subscribe("generate_report", self.on_generate_report)
        self.event_bus.subscribe("game_ended", self.on_game_ended)
        logger.info("ReportGenerator initialized")

    def on_generate_report(self, event: Event) -> None:
        """Handle report generation request."""
        report = self.generate_report()
        self.print_report(report)
        self.reports_generated += 1

    def on_game_ended(self, event: Event) -> None:
        """Automatically generate report when game ends."""
        logger.info("\n" + "="*60)
        logger.info("GAME ENDED - Generating Final Report")
        logger.info("="*60)
        report = self.generate_report()
        self.print_report(report)

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive statistics report."""
        report = {
            "generated_at": datetime.now(),
            "statistics": {}
        }

        for processor_name, processor in self.processors.items():
            if hasattr(processor, 'get_statistics'):
                report["statistics"][processor_name] = processor.get_statistics()

        return report

    def print_report(self, report: Dict[str, Any]) -> None:
        """Print formatted report to console."""
        print("\n" + "="*60)
        print(f"GAMEPLAY STATISTICS REPORT")
        print(f"Generated at: {report['generated_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        for processor_name, stats in report["statistics"].items():
            print(f"\n[{processor_name.upper()}]")
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.2f}")
                elif isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"  {key}: {value}")

        print("\n" + "="*60 + "\n")

    def get_statistics(self) -> Dict[str, Any]:
        """Return report generator statistics."""
        return {
            "reports_generated": self.reports_generated
        }
