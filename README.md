# Sudoku Solver & Interactive Game (Python)

A terminal-based Sudoku Solver and Interactive Game built using Python.  
This project solves Sudoku puzzles using the **backtracking algorithm** and also allows users to **play Sudoku interactively in the terminal**.

---

## ✨ Features
- 🧩 Solve any valid 9×9 Sudoku puzzle
- 🎮 Interactive play mode in terminal
- 💡 Hint system for valid moves
- ⚡ Auto-solve option
- 🧪 Demo and test modes
- 📄 Clean ASCII board display
- ❌ No external libraries (standard library only)

---

## 🧠 Concepts Used
- Object-Oriented Programming (OOP)
- Recursion
- Backtracking Algorithm
- Input validation
- Command-line arguments

---

## 🚀 How to Run

Make sure Python **3.6 or higher** is installed.

### ▶️ Play Sudoku interactively
```bash
python sudoku.py --play
```

#### 🎮 In-Game Commands

Once interactive mode starts, you can use the following commands:

- `<row> <col> <num>` → Place a number on the board  
  Example:
  ```bash
  0 0 5
  ```
  This places the number **5** at row 0, column 0.

- `hint` → Get a valid move suggestion.

- `solve` → Automatically solve the current puzzle.

- `quit` → Exit the game.
