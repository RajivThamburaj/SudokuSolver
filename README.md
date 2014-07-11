# Sudoku Solver

This application solves Sudoku puzzles, providing options for GUI and command-line interfaces as well as an importable module for use in other programs.

### Build Instructions

Run `SudokuSolver/solver.py` to launch the GUI solver. Run `SudokuSolver/board.py` to launch the command-line interface.

### Other Applications

Import the `board` module and instantiate a `Board` object. The initializer takes two arguments: a string corresponding to the numbers on the board (with no spaces, in the form `"130204...007809"`) and an integer corresponding to the width of the board (default value is `9`). Call `isSolvable()` on the `Board` to determine whether the board can be solved (this determines whether the puzzle contains any trivial inconsistencies). Call `trySolve()` on the `Board` object, then call `wasSolved()` to determine whether a correct solution was found (there are certain nontrivial inconsistencies that can only be discovered if a solution is attempted). The solution will then be contained in the object’s `numbers` property, a string of numbers in the same format as the input to the constructor.
