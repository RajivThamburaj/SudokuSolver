# Sudoku Solver

This application solves Sudoku puzzles, providing options for GUI and command-line interfaces as well as an importable module for use in other programs.

### How to Run (GUI)

Run `SudokuSolver/solver.py` to launch the GUI solver.

### How to Run (CLI)

Run `SudokuSolver/board.py` to launch the command-line interface.

### How to Use in Other Applications

<<<<<<< HEAD
Import the `board` module and instantiate a `Board` object. The initializer takes two arguments: a string corresponding to the numbers on the board (with no spaces, in the form `”130204...007809”`) and an integer corresponding to the width of the board (default value is `9`). Call `solve()` on the `Board` object. The solution will then be contained in the object’s `numbers` property, a string of numbers in the same format as the input to the constructor.
=======
Import the `board` module and instantiate a `Board` object. The initializer takes two arguments: a string corresponding to the numbers on the board (with no spaces, in the form `"130204...007809"`) and an integer corresponding to the width of the board (default value is `9`).
>>>>>>> FETCH_HEAD
