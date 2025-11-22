#!/usr/bin/env python3
"""
Demo Mode - Simula execução do jogo sem PyBoy
Útil quando PyBoy não pode ser instalado (Python 3.13+)
"""

import sys
import time
import random
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
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

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GameSimulator:
    """Simula gameplay de um jogo Game Boy"""

    def __init__(self, event_bus: EventBus, rom_name: str):
        self.event_bus = event_bus
        self.rom_name = rom_name
        self.running = True

    def simulate_gameplay(self, duration_seconds: int = 30):
        """Simula uma sessão de jogo"""
        print("\n" + "="*60)
        print(f"🎮 MODO DEMO - Simulando {self.rom_name}")
        print("="*60)
        print("\nSimulando gameplay por ~{} segundos...".format(duration_seconds))
        print("(Pressione Ctrl+C a qualquer momento para parar)\n")

        # Start game
        self.event_bus.publish("game_started", {"rom": self.rom_name})
        time.sleep(1)

        start_time = time.time()
        step_count = 0

        try:
            while self.running and (time.time() - start_time) < duration_seconds:
                # Simular movimento aleatório
                if random.random() < 0.7:  # 70% chance de movimento
                    direction = random.choice(["up", "down", "left", "right"])
                    step_count += 1
                    self.event_bus.publish("player_moved", {
                        "direction": direction,
                        "position": (step_count, step_count, 1),
                        "step_number": step_count
                    })

                    if step_count % 10 == 0:
                        print(f"  🚶 {step_count} passos dados...")

                # Simular batalha ocasional
                if step_count > 0 and step_count % 30 == 0:
                    self._simulate_battle()

                # Simular interações
                if random.random() < 0.1:  # 10% chance
                    self._simulate_interaction()

                time.sleep(0.1)  # Pausa entre ações

        except KeyboardInterrupt:
            print("\n\n⏸️  Gameplay interrompido pelo usuário")

        # End game
        self.event_bus.publish("game_ended", {
            "total_frames": int((time.time() - start_time) * 60),
            "total_steps": step_count
        })

    def _simulate_battle(self):
        """Simula uma batalha"""
        print("\n  ⚔️  Batalha iniciada!")
        self.event_bus.publish("battle_started", {"frame": 1000})
        time.sleep(0.5)

        # Simular alguns ataques
        for _ in range(random.randint(2, 4)):
            damage = random.randint(10, 30)
            self.event_bus.publish("player_damaged", {
                "damage": damage,
                "current_health": 100 - damage,
                "previous_health": 100
            })
            time.sleep(0.3)

        # Resultado aleatório
        result = random.choice(["won", "won", "lost"])  # 66% chance de vitória
        self.event_bus.publish("battle_ended", {
            "frame": 1500,
            "result": result
        })

        emoji = "🎉" if result == "won" else "💀"
        print(f"  {emoji} Batalha {result}!")

        # Cura após batalha
        if result == "won":
            time.sleep(0.2)
            self.event_bus.publish("player_healed", {
                "healing": 20,
                "current_health": 100,
                "previous_health": 80
            })

    def _simulate_interaction(self):
        """Simula interação com NPC ou item"""
        interaction_type = random.choice(["npc", "item", "door"])

        if interaction_type == "npc":
            self.event_bus.publish("npc_interaction", {"npc_id": random.randint(1, 10)})
            print("  💬 Conversa com NPC")
        elif interaction_type == "item":
            items = ["Potion", "Pokeball", "Antidote", "Poké Flute"]
            item = random.choice(items)
            self.event_bus.publish("item_collected", {"item": item})
            print(f"  📦 Item coletado: {item}")
        else:
            self.event_bus.publish("door_opened", {})
            print("  🚪 Porta aberta")


def main():
    """Executa o modo demo"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Modo Demo - Simula execução do jogo"
    )
    parser.add_argument(
        "rom",
        type=str,
        nargs="?",
        default="demo.gb",
        help="Nome do ROM (apenas para exibição)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Duração da simulação em segundos (padrão: 30)"
    )

    args = parser.parse_args()

    # Initialize Event Bus
    event_bus = EventBus()

    # Initialize Event Processors
    processors = {
        "battle_counter": BattleCounterProcessor(event_bus),
        "step_counter": StepCounterProcessor(event_bus),
        "game_time": GameTimeTracker(event_bus),
        "health_monitor": HealthMonitor(event_bus),
        "interaction_tracker": InteractionTracker(event_bus)
    }

    # Initialize Report Generator
    report_generator = ReportGenerator(event_bus, processors)

    # Create and run simulator
    simulator = GameSimulator(event_bus, args.rom)
    simulator.simulate_gameplay(args.duration)


if __name__ == "__main__":
    main()
