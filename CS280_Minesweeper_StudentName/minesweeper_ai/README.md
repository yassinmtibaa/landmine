# Minesweeper AI Project

**CS280 – Introduction to Artificial Intelligence**  
**Project Assignment 1**  
Mediterranean Institute of Technology (MedTech)

---

## 📋 Project Overview

This project implements an intelligent agent capable of playing Minesweeper using logical inference, knowledge representation, and probabilistic decision-making. The AI uses propositional logic to deduce safe moves and mine locations, and employs probability calculations when complete certainty is not possible.

---

## 🎯 Key Features

### AI Capabilities
- **Logical Inference**: Uses propositional logic to deduce safe cells and mine locations
- **Knowledge Representation**: Maintains sentences of the form `{cells} = count`
- **Subset Inference**: Generates new knowledge by comparing existing sentences
- **Probabilistic Reasoning**: Makes optimal guesses when certain moves aren't available
- **Iterative Learning**: Continuously updates knowledge base as new information is revealed

### Implementation Features
- Interactive pygame-based GUI
- Automated AI gameplay with visualization
- Comprehensive testing framework
- Performance evaluation across multiple difficulty levels
- Detailed statistics and analytics

---

## 📁 Project Structure

```
minesweeper_ai/
│
├── minesweeper.py       # Game environment and logic
├── ai_agent.py          # AI agent with inference engine
├── runner.py            # Pygame GUI for interactive play
├── test_ai.py           # Testing and evaluation framework
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Extract the project files**
   ```bash
   unzip CS280_Minesweeper_<YourName>.zip
   cd minesweeper_ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install pygame directly:
   ```bash
   pip install pygame
   ```

---

## 💻 Usage

### 1. Interactive GUI Mode

Run the visual interface to play manually or watch the AI:

```bash
python runner.py
```

**Controls:**
- **Left Click**: Reveal a cell
- **Right Click**: Flag a cell as a mine
- **AI Move Button**: Let the AI make one move (or toggle continuous play)
- **Reset Button**: Start a new game

### 2. Testing and Evaluation

Run comprehensive tests to evaluate AI performance:

```bash
python test_ai.py
```

This will:
- Run a single game with detailed output
- Test on beginner difficulty (100 games)
- Compare performance across 5 difficulty levels
- Generate statistical reports

### 3. Custom Testing

You can also import and use the testing framework programmatically:

```python
from test_ai import MinesweeperTester

tester = MinesweeperTester()

# Run 50 games on 8x8 board with 10 mines
stats = tester.run_multiple_games(height=8, width=8, mines=10, num_games=50)
tester.print_statistics(stats)
```

---

## 🧠 AI Algorithm Explanation

### Knowledge Representation

The AI maintains a knowledge base of **sentences**, where each sentence is of the form:

```
{Cell1, Cell2, Cell3, ...} = Count
```

This means: "Among these cells, exactly `Count` of them contain mines."

**Example:**
- `{(0,0), (0,1), (1,0)} = 2` means 2 of these 3 cells are mines

### Inference Rules

#### 1. **Direct Inference**
- If `count = 0`: All cells are safe
- If `count = len(cells)`: All cells are mines

#### 2. **Subset Inference**
If Sentence A is a subset of Sentence B:
```
A: {A, B} = 1
B: {A, B, C, D} = 3
→ New: {C, D} = 2
```

### Decision Making Process

1. **Mark Known Safe/Mines**: Apply direct inference rules
2. **Generate New Knowledge**: Use subset inference to create new sentences
3. **Make Safe Move**: If any safe cell is known, move there
4. **Probabilistic Move**: Calculate mine probability for each unknown cell and choose the safest

### Example Walkthrough

```
Initial Board (all hidden):
? ? ?
? ? ?
? ? ?

Move 1: Reveal (1,1) → Shows "2"
Knowledge: {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)} = 2

Move 2: Reveal (0,0) → Shows "0"
Knowledge: All neighbors of (0,0) are safe
New moves: (0,1), (1,0)

... (continues with logical inference and probabilistic reasoning)
```

---

## 📊 Performance Metrics

The AI is evaluated on:

- **Win Rate**: Percentage of games won
- **Average Moves**: Mean number of moves per game
- **Safe Move Accuracy**: Percentage of moves that were logically certain
- **Random Move Efficiency**: Performance when guessing is required

### Typical Results (100 games, Beginner difficulty: 8×8, 10 mines)
- Win Rate: ~60-85%
- Average Moves: ~30-40
- Safe Move Accuracy: ~70-80%

---

## 🎮 Game Configurations

### Predefined Difficulty Levels

| Level | Dimensions | Mines | Difficulty |
|-------|-----------|-------|-----------|
| Beginner | 8×8 | 10 | Easy |
| Intermediate | 16×16 | 40 | Medium |
| Expert | 16×30 | 99 | Hard |

You can customize these in the code by modifying the constants in `runner.py`:

```python
HEIGHT = 8
WIDTH = 8
MINES = 10
```

---

## 🔧 Code Architecture

### Classes and Modules

#### **minesweeper.py**
- `Minesweeper`: Game environment
  - Board initialization with random mine placement
  - Mine detection
  - Neighbor counting
  - Win condition checking

#### **ai_agent.py**
- `Sentence`: Logical statement representation
  - Knowledge about specific cells and mine counts
  - Inference methods (known_mines, known_safes)
  
- `MinesweeperAI`: Intelligent agent
  - Knowledge base management
  - Logical inference engine
  - Probabilistic decision making
  - Move selection (safe/random)

#### **runner.py**
- Pygame-based visualization
- User interaction handling
- AI automation controls
- Real-time knowledge display

#### **test_ai.py**
- `MinesweeperTester`: Evaluation framework
  - Single game execution with detailed logging
  - Batch testing across multiple games
  - Statistical analysis
  - Performance comparison across difficulties

---

## 📝 Technical Implementation Details

### Key Algorithms

1. **Knowledge Update (`add_knowledge`)**
   - Creates new sentence from revealed cell
   - Triggers inference cascade
   - Cleans up knowledge base

2. **Inference Engine (`_infer_knowledge`)**
   - Iteratively applies direct inference rules
   - Marks safe cells and mines
   - Continues until no new information can be derived

3. **Subset Inference (`_infer_from_subsets`)**
   - Compares all sentence pairs
   - Generates new sentences from set differences
   - Adds derived knowledge to base

4. **Probabilistic Move Selection (`make_random_move`)**
   - Calculates mine probability for each cell
   - Selects cell with lowest risk
   - Falls back to random selection if no probability data available

---

## 🐛 Troubleshooting

### Common Issues

**Issue: pygame not found**
```bash
pip install pygame --upgrade
```

**Issue: Display not working**
- Ensure you have a graphical environment
- Try running in a local environment (not SSH)

**Issue: Games run too fast**
- Adjust `ai_move_delay` in `runner.py` (line 34)

---

## 🎓 Learning Objectives Achieved

This project demonstrates:
- ✅ Knowledge representation using propositional logic
- ✅ Logical inference and constraint satisfaction
- ✅ Decision-making under uncertainty
- ✅ Probabilistic reasoning
- ✅ Agent design and implementation
- ✅ Performance evaluation and testing

---

## 🔮 Future Improvements

Potential enhancements:
- Advanced probability models (Bayesian inference)
- Pattern recognition for common configurations
- Machine learning for move optimization
- Multi-agent collaboration
- Constraint satisfaction problem (CSP) formulation

---

## 📚 References

- CS50 AI Minesweeper Project: https://cs50.harvard.edu/ai/projects/1/minesweeper/
- Russell & Norvig, "Artificial Intelligence: A Modern Approach"
- Propositional Logic and Inference Rules
- Probability Theory and Decision Making

---

## 👤 Author Information

**Student Name(s)**: Yassine Mtibaa & Youssef Ben Moussa  
**Course**: CS280 – Introduction to Artificial Intelligence  
**Institution**: Mediterranean Institute of Technology (MedTech)  
**Date**: February 2026

---

## 📜 License

This project is submitted as coursework for CS280 at MedTech.
Academic integrity policies apply.

---

**End of README**
