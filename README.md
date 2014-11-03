
## Sudoku Puzzle Solver in Python

Usage: python sudoku.py input.csv output.csv

### Background

A sudoku is a 9x9 array of the digits 1 through 9 such that each row and column contain all nine digits with no repeats. If you divide the 9x9 array evenly into 3x3 submatrices, each 3x3 submatrix also has all nine distinct digits. 

A sudoku puzzle is a 9x9 array with some of the entries filled in, and it's the job of the solver to fill in the blanks. A well-formed puzzle has a unique solution. The more entries filled in, the easier the puzzle is to solve; the fewer, the harder. Too few entries might not have a unique solution. For some patterns of entries, a solution might not exist. 

One solution method is to check the presence of existing entries in rows, columns, and 3x3 submatrices, and reduce the possibilities for blank entries until all blanks are determined. Another method is to hypothesize a value for a blank, test it, and see if a solution arises. The first method works on fairly easy sudoku puzzles, but is not enough for harder puzzles. The second method is expensive because it requires a lot of testing and tracking.

My program uses the first method, and if no solution can be found, invokes the second method to converge to a solution. 




