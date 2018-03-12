# sudoku
Solving sudoku as an optimization problem

This is a silly attempt to see if we can write a sudoku solver which
treats the puzzle as an optimization problem.

Each square in the board is an 9-dimensional unit vector. The
sudoku constraint is equivalent to the statement that the unit
vectors are orthogonal.

In additiona to a numpy solver, there are scripts for inputting
the initial board configurations and for displaying the solution
as it progresses.
