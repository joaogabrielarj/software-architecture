# 🚀 Quick Start - Event-Driven PyBoy

## ⚡ Início Rápido em 5 Minutos

### 1️⃣ Instalar Dependências (1 minuto)

```bash
# Instalar PyBoy
pip install pyboy
```

### 2️⃣ Testar o Sistema (1 minuto)

```bash
# Executar testes (não precisa de ROM)
python test_event_system.py
```

**Resultado esperado:**
```
============================================================
ALL TESTS COMPLETED SUCCESSFULLY!
============================================================
```

### 3️⃣ Entender a Estrutura (2 minutos)

**4 arquivos principais:**

1. **event_bus.py** - O "mensageiro" que distribui eventos
2. **event_processors.py** - 6 "ouvintes" que processam eventos
3. **pyboy_wrapper.py** - Detecta eventos do jogo
4. **main.py** - Orquestra tudo

### 4️⃣ Executar com ROM (1 minuto) - OPCIONAL

```bash
# Se você tiver um ROM de Game Boy
python main.py seu_jogo.gb

# Ou em modo headless (sem janela)
python main.py seu_jogo.gb --headless
```

---

## 📋 Comandos Essenciais

```bash
# Testar sistema
python test_event_system.py

# Executar com ROM
python main.py jogo.gb

# Executar sem interface gráfica
python main.py jogo.gb --headless

# Executar com logs detalhados
python main.py jogo.gb --debug

# Ver ajuda
python main.py --help
```

---

## 🎮 Como Jogar

1. Execute: `python main.py pokemon.gb`
2. Use o teclado:
   - **Setas**: Movimento
   - **Z**: Botão A
   - **X**: Botão B
   - **Enter**: Start
   - **Backspace**: Select
3. Pressione **Ctrl+C** para parar e ver relatório

---

## 📊 O Que Acontece Durante o Jogo

```
Você move → PyBoy detecta → Evento publicado → Processadores atualizam → Estatísticas registradas
```

**Exemplo:**

1. Você pressiona ↑ (cima)
2. PyBoy detecta mudança de posição
3. Wrapper publica evento `player_moved`
4. StepCounter recebe e incrementa contador
5. Quando você para (Ctrl+C), relatório é gerado

---

## 📈 Relatório de Exemplo

Ao parar o jogo, você verá algo assim:

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
  active_duration_seconds: 1845.0

[HEALTH_MONITOR]
  total_damage_taken: 250
  total_healing_received: 225
  knockouts: 1
============================================================
```

---

## 🔍 Estrutura de Arquivos para Iniciantes

```
📁 Exercício - EDA/
│
├── 🟢 COMECE AQUI
│   └── README.md                    ← Leia primeiro
│
├── 💻 CÓDIGO (não precisa modificar)
│   ├── event_bus.py                 ← Event Bus
│   ├── event_processors.py          ← 6 Processors
│   ├── pyboy_wrapper.py             ← Detecta eventos
│   └── main.py                      ← Execute este
│
├── 🧪 TESTE
│   └── test_event_system.py         ← Execute para testar
│
└── 📚 DOCS (se quiser saber mais)
    ├── INSTALL.md                   ← Instalação detalhada
    ├── USAGE_EXAMPLES.md            ← Exemplos de uso
    └── ARCHITECTURE.md              ← Arquitetura técnica
```

---

## ❓ FAQ Rápido

### P: Preciso modificar o código do PyBoy?
**R:** Não! Tudo funciona com wrappers externos.

### P: Preciso de um ROM para testar?
**R:** Não para testes básicos. Use `test_event_system.py`.

### P: Funciona com qualquer jogo de Game Boy?
**R:** Sim, mas detecção de eventos é otimizada para Pokémon Red/Blue.

### P: Como adiciono um novo processador?
**R:** Veja [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md#1-adicionar-processador-customizado)

### P: Onde ficam os logs?
**R:** Console e arquivo `gameplay.log`

---

## 🎯 Próximos Passos

Depois do Quick Start, explore:

1. 📖 **[README.md](../README.md)** - Documentação completa
2. 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura detalhada

---

## 🔧 Solução Rápida de Problemas

### ❌ Erro: `ModuleNotFoundError: No module named 'pyboy'`
```bash
pip install pyboy
```

### ❌ Erro: `SDL2 not found`
```bash
# Linux
sudo apt-get install libsdl2-dev

# macOS
brew install sdl2

# Windows - geralmente instala automaticamente
# Alternativa: use --headless
python main.py rom.gb --headless
```

### ❌ Erro: `ROM file not found`
```bash
# Use caminho completo
python main.py /caminho/completo/para/jogo.gb

# Ou navegue até o diretório do ROM
cd pasta_dos_roms
python ../main.py jogo.gb
```

---

## 🎓 Para Estudantes

### O Que Este Projeto Demonstra

✅ **Arquitetura Orientada a Eventos (EDA)**
✅ **Padrão Publish/Subscribe**
✅ **Desacoplamento de Componentes**
✅ **Princípios SOLID**
✅ **Clean Code**

### Requisitos do Projeto Individual (PDF)

- [x] Event Bus implementado
- [x] 5+ Event Processors (6 implementados)
- [x] Atualização em tempo real
- [x] Relatório final
- [x] Controle via teclado

**Status: 100% Completo** ✅

---

## 📞 Onde Encontrar Ajuda

| Preciso... | Arquivo |
|------------|---------|
| Instalar | Ver seção "Instalação" no README |
| Usar | [README.md](../README.md) |
| Entender | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

## ⏱️ Estimativa de Tempo

| Atividade | Tempo |
|-----------|-------|
| Instalar PyBoy | 1 min |
| Executar testes | 1 min |
| Ler README | 5 min |
| Testar com ROM | 2 min |
| Entender código | 15 min |
| Ler docs completas | 30 min |
| Modificar/estender | 1+ hora |

---

## 🎮 Dica: Onde Conseguir ROMs de Teste

**Legalmente:**

1. **Homebrew Games** (gratuitos):
   - https://hh.gbdev.io/
   - https://itch.io/games/tag-gb-studio

2. **Jogos comerciais**:
   - Extrair de cartuchos originais que você possui

**Para testes rápidos:**
- ROMs homebrew como "2048.gb" ou "Tobu Tobu Girl"
- Funcionam perfeitamente para testar o sistema

---

## 🏆 Checklist de Sucesso

- [ ] PyBoy instalado
- [ ] Testes executados com sucesso
- [ ] Entendi o fluxo básico
- [ ] Consegui executar com ROM (opcional)
- [ ] Vi um relatório ser gerado
- [ ] Explorei pelo menos 2 arquivos de código

**Parabéns! Você está pronto para usar o projeto!** 🎉

---

## 📝 Comandos Copiáveis

```bash
# Setup completo
pip install pyboy
python test_event_system.py
python main.py seu_jogo.gb

# Modo debug
python main.py seu_jogo.gb --debug

# Modo headless
python main.py seu_jogo.gb --headless

# Ver logs
tail -f gameplay.log
```

---

**Este é o jeito mais rápido de começar!**

Para informações detalhadas, consulte [README.md](../README.md).
