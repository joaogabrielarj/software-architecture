# Event-Driven PyBoy

Sistema de arquitetura orientada a eventos integrado ao emulador PyBoy para Game Boy. Inspirado no "Twitter Plays Pokémon", rastreia eventos do jogo e gera relatórios estatísticos em tempo real.

## 🎯 Características

- **Event Bus** - Padrão Publish/Subscribe
- **6 Event Processors** - Rastreamento completo de eventos
- **Testes Automatizados** - Suite completa de testes
- **Modo Demo** - Simulação sem necessidade de ROM (Python 3.13+)
- **Relatórios em Tempo Real** - Estatísticas detalhadas

## 📁 Estrutura

```
.
├── src/                    # Código fonte
│   ├── event_bus.py        # Event Bus (Publish/Subscribe)
│   ├── event_processors.py # 6 Event Processors
│   ├── pyboy_wrapper.py    # Integração PyBoy
│   └── main.py             # Aplicação principal
│
├── tests/                  # Testes
│   └── test_event_system.py
│
├── docs/                   # Documentação
│   ├── QUICKSTART.md       # Guia rápido
│   └── ARCHITECTURE.md     # Arquitetura detalhada
│
├── config/                 # Configuração
│   └── requirements.txt
│
├── run.py                  # Executar jogo
├── run_tests.py            # Executar testes
└── demo_mode.py            # Modo demonstração
```

## 🚀 Instalação

```bash
# Clonar repositório
git clone https://github.com/joaogabrielarj/software-architecture.git
cd software-architecture

# Instalar dependências
pip install -r config/requirements.txt
```

### Requisitos do Sistema

- Python 3.8+
- SDL2 (opcional, apenas para interface gráfica)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libsdl2-dev
```

**macOS:**
```bash
brew install sdl2
```

## 🎮 Uso

### Testar sem ROM (Recomendado para começar)

```bash
python run_tests.py
```

### Modo Demonstração

```bash
# Demo padrão (30 segundos)
python demo_mode.py

# Demo personalizada
python demo_mode.py --duration 60
```

### Executar com ROM

```bash
# Com interface gráfica
python run.py seu_jogo.gb

# Sem interface (headless)
python run.py seu_jogo.gb --headless

# Com debug
python run.py seu_jogo.gb --debug
```

**Controles:**
- Setas: Movimento
- Z: Botão A
- X: Botão B
- Enter: Start
- Backspace: Select
- Ctrl+C: Parar e ver relatório

## 📊 Event Processors

O sistema inclui 6 processadores de eventos:

1. **BattleCounterProcessor** - Rastreia batalhas e resultados
2. **StepCounterProcessor** - Conta passos e direções
3. **GameTimeTracker** - Monitora tempo de jogo
4. **HealthMonitor** - Acompanha HP e dano
5. **InteractionTracker** - Registra interações com NPCs/itens
6. **ReportGenerator** - Gera relatórios consolidados

## 📈 Exemplo de Relatório

```
============================================================
GAMEPLAY STATISTICS REPORT
============================================================

[BATTLE_COUNTER]
  total_battles: 5
  battles_won: 3
  win_rate: 0.60

[STEP_COUNTER]
  total_steps: 1523
  steps_by_direction:
    up: 412
    down: 389
    left: 356
    right: 366

[GAME_TIME]
  total_duration_seconds: 1845.0

[HEALTH_MONITOR]
  total_damage_taken: 250
  knockouts: 1
============================================================
```

## 🏗️ Arquitetura

O projeto segue o padrão **Event-Driven Architecture (EDA)**:

```
PyBoy Emulator → Detecta eventos → Event Bus → Distribui para Processors → Gera relatório
```

### Padrões Utilizados

- **Publish/Subscribe** - Event Bus
- **Observer** - Event Processors
- **Facade** - PyBoy Wrapper
- **Strategy** - Diferentes processadores

Veja [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) para detalhes completos.

## 🧪 Testes

```bash
# Executar todos os testes
python run_tests.py

# Resultado esperado:
# ALL TESTS COMPLETED SUCCESSFULLY!
```

## 📝 Documentação

- [QUICKSTART.md](docs/QUICKSTART.md) - Guia de início rápido
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura detalhada

## ⚠️ Nota sobre ROMs

ROMs de jogos **não estão incluídos** neste repositório. Use apenas ROMs que você possui legalmente:

- ROMs homebrew (gratuitas e legais)
- ROMs extraídas de cartuchos que você possui

## 🐍 Compatibilidade Python

- **Python 3.8-3.12**: Suporte completo com PyBoy
- **Python 3.13+**: Use `demo_mode.py` (PyBoy ainda não suporta 3.13)

## 📄 Licença

Projeto educacional - Arquitetura de Software

## 👤 Autor

João Gabriel
