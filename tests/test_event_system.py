#!/usr/bin/env python3
"""
Test script to validate the Event Bus and Event Processors.
Simulates game events without requiring a ROM file.
"""

import sys
import time
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def simulate_gameplay():
    """Simulate a complete gameplay session with various events."""

    print("="*60)
    print("Testing Event-Driven Architecture")
    print("Simulating gameplay events...")
    print("="*60 + "\n")

    # Initialize Event Bus
    event_bus = EventBus()

    # Initialize all event processors
    processors = {
        "battle_counter": BattleCounterProcessor(event_bus),
        "step_counter": StepCounterProcessor(event_bus),
        "game_time": GameTimeTracker(event_bus),
        "health_monitor": HealthMonitor(event_bus),
        "interaction_tracker": InteractionTracker(event_bus)
    }

    # Initialize Report Generator
    report_generator = ReportGenerator(event_bus, processors)

    print("\n✓ All components initialized\n")
    time.sleep(1)

    # Simulate game start
    print("1. Starting game...")
    event_bus.publish("game_started", {"rom": "test_game.gb"})
    time.sleep(0.5)

    # Simulate player movements
    print("\n2. Simulating player movements...")
    directions = ["up", "up", "right", "right", "down", "left", "up", "right"]
    for i, direction in enumerate(directions, 1):
        event_bus.publish("player_moved", {
            "direction": direction,
            "position": (i, i, 1),
            "step_number": i
        })
        time.sleep(0.2)

    print(f"   ✓ Moved {len(directions)} steps")

    # Simulate NPC interactions
    print("\n3. Simulating NPC interactions...")
    for i in range(3):
        event_bus.publish("npc_interaction", {"npc_id": i})
        time.sleep(0.2)
    print("   ✓ Interacted with 3 NPCs")

    # Simulate item collection
    print("\n4. Simulating item collection...")
    items = ["Potion", "Pokeball", "Antidote"]
    for item in items:
        event_bus.publish("item_collected", {"item": item})
        time.sleep(0.2)
    print(f"   ✓ Collected {len(items)} items")

    # Simulate battle
    print("\n5. Simulating battle...")
    event_bus.publish("battle_started", {"frame": 1000})
    time.sleep(0.5)

    # Simulate taking damage during battle
    event_bus.publish("player_damaged", {
        "damage": 25,
        "current_health": 75,
        "previous_health": 100
    })
    time.sleep(0.3)

    event_bus.publish("player_damaged", {
        "damage": 15,
        "current_health": 60,
        "previous_health": 75
    })
    time.sleep(0.3)

    # Win the battle
    event_bus.publish("battle_ended", {
        "frame": 1500,
        "result": "won"
    })
    print("   ✓ Battle completed (won)")

    # Simulate healing
    print("\n6. Simulating healing...")
    event_bus.publish("player_healed", {
        "healing": 30,
        "current_health": 90,
        "previous_health": 60
    })
    time.sleep(0.3)
    print("   ✓ Player healed")

    # Simulate second battle (lost)
    print("\n7. Simulating second battle...")
    event_bus.publish("battle_started", {"frame": 2000})
    time.sleep(0.3)

    event_bus.publish("player_damaged", {
        "damage": 90,
        "current_health": 0,
        "previous_health": 90
    })
    time.sleep(0.2)

    event_bus.publish("player_fainted", {"frame": 2100})
    time.sleep(0.2)

    event_bus.publish("battle_ended", {
        "frame": 2200,
        "result": "lost"
    })
    print("   ✓ Battle completed (lost)")

    # More movements
    print("\n8. Simulating more movements...")
    for i in range(5):
        event_bus.publish("player_moved", {
            "direction": "up",
            "position": (i+10, i+10, 1),
            "step_number": len(directions) + i + 1
        })
        time.sleep(0.1)
    print("   ✓ Moved 5 more steps")

    # Simulate game end
    print("\n9. Ending game...\n")
    time.sleep(0.5)
    event_bus.publish("game_ended", {
        "total_frames": 3000,
        "total_steps": len(directions) + 5
    })

    print("\n" + "="*60)
    print("Simulation complete!")
    print("="*60)

    # Print event statistics
    print(f"\nTotal events published: {len(event_bus.get_event_history())}")
    print(f"Total subscribers: {event_bus.get_subscribers_count()}")


def test_event_bus_basic():
    """Test basic Event Bus functionality."""

    print("\n" + "="*60)
    print("Testing Event Bus Basic Functionality")
    print("="*60 + "\n")

    event_bus = EventBus()
    received_events = []

    def test_callback(event):
        received_events.append(event)

    # Test subscribe
    event_bus.subscribe("test_event", test_callback)
    print("✓ Subscribed to test_event")

    # Test publish
    event_bus.publish("test_event", {"data": "test"})
    assert len(received_events) == 1, "Should receive 1 event"
    print("✓ Published and received event")

    # Test unsubscribe
    event_bus.unsubscribe("test_event", test_callback)
    event_bus.publish("test_event", {"data": "test2"})
    assert len(received_events) == 1, "Should still have 1 event after unsubscribe"
    print("✓ Unsubscribed successfully")

    # Test multiple subscribers
    callbacks = [lambda e: None for _ in range(3)]
    for cb in callbacks:
        event_bus.subscribe("multi_test", cb)

    assert event_bus.get_subscribers_count("multi_test") == 3
    print("✓ Multiple subscribers registered")

    print("\n✓ All Event Bus tests passed!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("EVENT-DRIVEN PYBOY - SYSTEM TEST")
    print("="*60)

    # Run basic tests
    test_event_bus_basic()

    # Run full simulation
    simulate_gameplay()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")
