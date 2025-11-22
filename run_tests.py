#!/usr/bin/env python3
"""
Test runner for Event-Driven PyBoy.
Executes all tests from the project root.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run tests
from tests.test_event_system import simulate_gameplay, test_event_bus_basic

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
