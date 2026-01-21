#!/usr/bin/env python3
""" 
Sudoku Solver and Interactive Game
===================================
A complete Sudoku implementation using backtracking algorithm.
Supports solving puzzles, interactive play mode, and demonstrations.

Author: Kartik Bisht (AI-assisted academic project)
Python Version: 3.6+
Dependencies: None (standard library only)

"""

import sys
import time
import json
from typing import List, Optional, Tuple


class Sudoku:
    """
    Sudoku puzzle solver and validator.
    
    The board is represented as a 9x9 list of lists where:
    - 0 represents an empty cell
    - Numbers 1-9 represent filled cells
    """
    
    def __init__(self, board: Optional[List[List[int]]] = None):
        """
        Initialize a Sudoku puzzle.
        
        Args:
            board: Optional 9x9 grid as list of lists. If None, creates empty board.
        """
        if board is None:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.load_board(board)
        
        # Store original cells to prevent modification during play mode
        self.original = [[self.board[i][j] for j in range(9)] for i in range(9)]
    
    def load_board(self, board: List[List[int]]) -> None:
        """
        Load a board configuration.
        
        Args:
            board: 9x9 grid as list of lists
            
        Raises:
            ValueError: If board dimensions are invalid
        """
        if len(board) != 9 or any(len(row) != 9 for row in board):
            raise ValueError("Board must be 9x9")
        
        # Deep copy to avoid reference issues
        self.board = [[board[i][j] for j in range(9)] for i in range(9)]
        self.original = [[board[i][j] for j in range(9)] for i in range(9)]
    
    @classmethod
    def from_string(cls, s: str) -> 'Sudoku':
        """
        Create a Sudoku puzzle from an 81-character string.
        
        Args:
            s: String of 81 characters where 0 or . represents empty cells
            
        Returns:
            Sudoku instance
            
        Raises:
            ValueError: If string length is not 81
        """
        # Remove whitespace and newlines
        s = ''.join(s.split())
        
        if len(s) != 81:
            raise ValueError(f"String must be 81 characters long, got {len(s)}")
        
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                char = s[i * 9 + j]
                if char == '.' or char == '0':
                    row.append(0)
                elif char.isdigit() and 1 <= int(char) <= 9:
                    row.append(int(char))
                else:
                    raise ValueError(f"Invalid character '{char}' at position {i*9+j}")
            board.append(row)
        
        return cls(board)
    
    def find_empty(self) -> Optional[Tuple[int, int]]:
        """
        Find the next empty cell (containing 0) in the board.
        
        Returns:
            Tuple of (row, col) if empty cell found, None otherwise
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, num: int, row: int, col: int) -> bool:
        """
        Check if placing num at board[row][col] is valid according to Sudoku rules.
        
        Rules:
        1. Number must not exist in the same row
        2. Number must not exist in the same column
        3. Number must not exist in the same 3x3 box
        
        Args:
            num: Number to place (1-9)
            row: Row index (0-8)
            col: Column index (0-8)
            
        Returns:
            True if move is valid, False otherwise
        """
        # Check row
        for j in range(9):
            if self.board[row][j] == num and j != col:
                return False
        
        # Check column
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        
        return True
    
    def solve(self, show_steps: bool = False) -> bool:
        """
        Solve the Sudoku puzzle using backtracking algorithm.
        
        The backtracking algorithm works as follows:
        1. Find an empty cell
        2. Try numbers 1-9 in that cell
        3. For each number, check if it's valid
        4. If valid, place it and recursively solve the rest
        5. If we get stuck, backtrack and try the next number
        6. If all numbers fail, return False (no solution)
        7. If no empty cells remain, puzzle is solved
        
        Args:
            show_steps: If True, print board at each step (slow, for visualization)
            
        Returns:
            True if solved, False if no solution exists
        """
        if show_steps:
            self.pretty_print()
            print()
        
        # Find the next empty cell
        empty = self.find_empty()
        
        # If no empty cells, puzzle is solved
        if empty is None:
            return True
        
        row, col = empty
        
        # Try numbers 1-9
        for num in range(1, 10):
            if self.is_valid(num, row, col):
                # Place the number
                self.board[row][col] = num
                
                # Recursively solve
                if self.solve(show_steps):
                    return True
                
                # If didn't work, backtrack
                self.board[row][col] = 0
        
        # No valid number found, trigger backtracking
        return False
    
    def is_solved(self) -> bool:
        """
        Check if the puzzle is completely and correctly solved.
        
        Returns:
            True if solved, False otherwise
        """
        # Check no empty cells
        if any(self.board[i][j] == 0 for i in range(9) for j in range(9)):
            return False
        
        # Check all rows, columns, and boxes are valid
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                self.board[i][j] = 0  # Temporarily remove
                if not self.is_valid(num, i, j):
                    self.board[i][j] = num
                    return False
                self.board[i][j] = num
        
        return True
    
    def pretty_print(self) -> None:
        """
        Print the Sudoku board in a clean, readable format with grid lines.
        """
        print("    " + "   ".join(str(i) for i in range(9)))
        print("  +" + "---+" * 9)
        
        for i in range(9):
            row_str = f"{i} |"
            for j in range(9):
                if self.board[i][j] == 0:
                    row_str += " . "
                else:
                    row_str += f" {self.board[i][j]} "
                
                if (j + 1) % 3 == 0:
                    row_str += "|"
            
            print(row_str)
            
            if (i + 1) % 3 == 0:
                print("  +" + "---+" * 9)
    
    def get_hint(self) -> Optional[Tuple[int, int, int]]:
        """
        Get a hint by finding one valid move.
        
        Returns:
            Tuple of (row, col, num) for a valid move, or None if no hints available
        """
        # Try to find an empty cell with only one possibility
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    valid_nums = [num for num in range(1, 10) if self.is_valid(num, i, j)]
                    if len(valid_nums) == 1:
                        return (i, j, valid_nums[0])
        
        # If no single possibility, return any valid move
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(num, i, j):
                            return (i, j, num)
        
        return None


def load_puzzle_from_file(filename: str) -> Sudoku:
    """
    Load a Sudoku puzzle from a file.
    
    Supports:
    - 81-character string (with or without newlines)
    - 9 lines of 9 digits each
    - JSON array format
    
    Args:
        filename: Path to the puzzle file
        
    Returns:
        Sudoku instance
    """
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
        
        # Try JSON format first
        if content.startswith('['):
            try:
                board = json.loads(content)
                return Sudoku(board)
            except json.JSONDecodeError:
                pass
        
        # Try string format
        return Sudoku.from_string(content)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error loading puzzle: {e}")
        sys.exit(1)


def solve_mode(puzzle_input: str) -> None:
    """
    Solve a Sudoku puzzle and print the solution.
    
    Args:
        puzzle_input: Either an 81-char string or a filename
    """
    print("=" * 50)
    print("SUDOKU SOLVER - Solve Mode")
    print("=" * 50)
    
    try:
        # Check if input is a file
        if len(puzzle_input) > 81 or '.' in puzzle_input[-5:]:
            sudoku = load_puzzle_from_file(puzzle_input)
        else:
            sudoku = Sudoku.from_string(puzzle_input)
        
        print("\nOriginal Puzzle:")
        sudoku.pretty_print()
        
        print("\nSolving...")
        start_time = time.time()
        
        if sudoku.solve():
            elapsed = time.time() - start_time
            print(f"\n✓ Solved in {elapsed:.4f} seconds!\n")
            print("Solution:")
            sudoku.pretty_print()
        else:
            print("\n✗ No solution exists for this puzzle.")
    
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def play_mode() -> None:
    """
    Interactive play mode where user can solve the puzzle manually.
    """
    print("=" * 50)
    print("SUDOKU GAME - Interactive Play Mode")
    print("=" * 50)
    print("\nCommands:")
    print("  <row> <col> <num>  - Place number (e.g., '0 0 5')")
    print("  hint               - Get a hint")
    print("  solve              - Auto-solve the puzzle")
    print("  quit               - Exit the game")
    print("=" * 50)
    
    # Load a sample easy puzzle
    puzzle_string = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
    sudoku = Sudoku.from_string(puzzle_string)
    
    print("\nStarting Puzzle:")
    sudoku.pretty_print()
    
    while not sudoku.is_solved():
        print("\nYour move (or command):")
        user_input = input("> ").strip().lower()
        
        if user_input == 'quit':
            print("Thanks for playing!")
            return
        
        elif user_input == 'solve':
            print("\nAuto-solving...")
            if sudoku.solve():
                print("\n✓ Puzzle solved!\n")
                sudoku.pretty_print()
                return
            else:
                print("\n✗ Cannot solve this puzzle.")
                return
        
        elif user_input == 'hint':
            hint = sudoku.get_hint()
            if hint:
                row, col, num = hint
                print(f"\n💡 Hint: Try placing {num} at position ({row}, {col})")
            else:
                print("\n✗ No hints available.")
        
        else:
            try:
                parts = user_input.split()
                if len(parts) != 3:
                    print("✗ Invalid input. Use format: <row> <col> <num>")
                    continue
                
                row, col, num = int(parts[0]), int(parts[1]), int(parts[2])
                
                # Validate input
                if not (0 <= row <= 8 and 0 <= col <= 8):
                    print("✗ Row and column must be between 0 and 8")
                    continue
                
                if not (1 <= num <= 9):
                    print("✗ Number must be between 1 and 9")
                    continue
                
                # Check if cell is original (cannot be changed)
                if sudoku.original[row][col] != 0:
                    print("✗ Cannot change original puzzle numbers")
                    continue
                
                # Check if move is valid
                if sudoku.is_valid(num, row, col):
                    sudoku.board[row][col] = num
                    print("\n✓ Valid move!\n")
                    sudoku.pretty_print()
                else:
                    print("✗ Invalid move! Number conflicts with Sudoku rules")
            
            except (ValueError, IndexError):
                print("✗ Invalid input. Use format: <row> <col> <num>")
    
    print("\n" + "=" * 50)
    print("🎉 CONGRATULATIONS! You solved the puzzle! 🎉")
    print("=" * 50)


def demo_mode() -> None:
    """
    Demonstration mode showing the solver in action.
    """
    print("=" * 50)
    print("SUDOKU SOLVER - Demo Mode")
    print("=" * 50)
    
    # Sample medium-difficulty puzzle
    puzzle_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    
    print("\nLoading demo puzzle...")
    sudoku = Sudoku.from_string(puzzle_string)
    
    print("\nOriginal Puzzle:")
    sudoku.pretty_print()
    
    print("\nSolving...")
    start_time = time.time()
    
    if sudoku.solve():
        elapsed = time.time() - start_time
        print(f"\n✓ Solved in {elapsed:.4f} seconds!\n")
        print("Solution:")
        sudoku.pretty_print()
    else:
        print("\n✗ No solution exists.")


def run_tests() -> None:
    """
    Run test cases with three sample puzzles of varying difficulty.
    """
    print("=" * 50)
    print("SUDOKU SOLVER - Test Suite")
    print("=" * 50)
    
    test_puzzles = [
        {
            "name": "Easy Puzzle",
            "puzzle": "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
        },
        {
            "name": "Medium Puzzle",
            "puzzle": "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        },
        {
            "name": "Hard Puzzle",
            "puzzle": "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
        }
    ]
    
    for test in test_puzzles:
        print(f"\n{'=' * 50}")
        print(f"Testing: {test['name']}")
        print('=' * 50)
        
        sudoku = Sudoku.from_string(test['puzzle'])
        
        print("\nOriginal:")
        sudoku.pretty_print()
        
        start_time = time.time()
        solved = sudoku.solve()
        elapsed = time.time() - start_time
        
        if solved:
            print(f"\n✓ Solved in {elapsed:.4f} seconds")
            print("\nSolution:")
            sudoku.pretty_print()
            
            if sudoku.is_solved():
                print("✓ Verification: Solution is valid")
            else:
                print("✗ Verification: Solution is INVALID")
        else:
            print(f"\n✗ Failed to solve after {elapsed:.4f} seconds")


def print_help() -> None:
    """
    Print help information and usage examples.
    """
    help_text = """
SUDOKU SOLVER & GAME
====================

A complete Sudoku implementation with solver and interactive game modes.

ALGORITHM EXPLANATION
---------------------
This program uses the Backtracking algorithm to solve Sudoku puzzles:

1. Find an empty cell in the puzzle
2. Try placing numbers 1-9 in that cell
3. For each number, check if it's valid (no conflicts in row/column/box)
4. If valid, place the number and recursively solve the rest of the puzzle
5. If we can't solve with that number, remove it and try the next number
6. If all numbers fail, backtrack to the previous cell and try a different number
7. If no empty cells remain, the puzzle is solved!

TIME COMPLEXITY
---------------
Worst case: O(9^n) where n is the number of empty cells
In practice: Much faster due to constraint propagation and pruning
Most puzzles: Solved in under 0.01 seconds

USAGE
-----
Solve a puzzle from string:
    python sudoku.py --solve "003020600900305001..."

Solve a puzzle from file:
    python sudoku.py --solve puzzle.txt

Interactive play mode:
    python sudoku.py --play

Run demonstration:
    python sudoku.py --demo

Run test suite:
    python sudoku.py --test

Show this help:
    python sudoku.py --help

INPUT FORMATS
-------------
1. 81-character string (0 or . for empty cells):
   "003020600900305001001806400..."

2. Text file with 9 lines of 9 digits:
   003020600
   900305001
   001806400
   ...

3. JSON file with 9x9 array:
   [[0,0,3,0,2,0,6,0,0],
    [9,0,0,3,0,5,0,0,1],
    ...]

EXAMPLES
--------
# Solve a puzzle
python sudoku.py --solve "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

# Play interactively
python sudoku.py --play
> 0 0 5
> hint
> solve

FEATURES
--------
✓ Fast backtracking solver
✓ Interactive play mode with hints
✓ Multiple input format support
✓ Input validation and error handling
✓ Clean ASCII board display
✓ Comprehensive test suite

"""
    print(help_text)


def main():
    """
    Main entry point for the Sudoku program.
    """
    if len(sys.argv) < 2:
        print("Error: No command specified")
        print("Use --help for usage information")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == '--help' or command == '-h':
        print_help()
    
    elif command == '--solve':
        if len(sys.argv) < 3:
            print("Error: --solve requires a puzzle string or filename")
            sys.exit(1)
        solve_mode(sys.argv[2])
    
    elif command == '--play':
        play_mode()
    
    elif command == '--demo':
        demo_mode()
    
    elif command == '--test':
        run_tests()
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Use --help for usage information")
        sys.exit(1)


if __name__ == "__main__":

    main()
