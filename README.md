
## Sudoku Puzzle Solver in Python

Usage: python sudoku.py input.csv output.csv

### Background

A sudoku is a 9x9 array of the digits 1 through 9 such that each row and column contain all nine digits with no repeats. If you divide the 9x9 array evenly into 3x3 submatrices, each 3x3 submatrix also has all nine distinct digits. 

A sudoku puzzle is a 9x9 array with some of the entries filled in, and it's the job of the solver to fill in the blanks. A well-formed puzzle has a unique solution. The more entries filled in, the easier the puzzle is to solve; the fewer, the harder. Too few entries might not have a unique solution. For some patterns of entries, a solution might not exist. 

One solution method is to check the presence of existing entries in rows, columns, and 3x3 submatrices, and reduce the possibilities for blank entries until all blanks are narrowed down to one possibility. A second method is to hypothesize a value for a blank, test it, and see if a solution arises. The first method works on fairly easy sudoku puzzles, but is not enough for harder puzzles. The second method can be expensive because it requires a lot of testing and tracking.

My program uses the first method, and if no solution can be found, invokes the second method to converge to a solution. 

### How It Works

The program reads in a .csv file with 9 rows and 9 columns, with zeros representing blank entries. The output, if there are no errors, is a .csv file with blank entries filled in. 

The sudoku matrix is stored as a matrix of lists. Filled entries have lists with only one component. Blank entries have longer lists containing all possibilities that have not been ruled out yet. Because the entries are lists, it is easy to tell if a matrix is fully reduced (solved): all of its lists have length one, and the sum of all lengths is 81. That is the "is done?" test used throughout. 

The program uses functional programming style. I chose that style over object-oriented just because I'm a little more comfortable with it - I'm relatively new to Python. The program employs the two algorithms mentioned in the Background section: row/column/sub9 reduction and hypothesis testing. As a first pass, it tries row/column/sub9 reduction, making sure to keep row/column/sub9 values distinct. If that works, the program ends. 

If the sudoku is unsolved after the first pass, the hypothesis function carries out hypothesis testing. It looks for the first instance of an unreduced list, and tests reducing it to its first element. If a solution results, the program ends. If the hypothesis is bad and results in over-reduction (lists of length zero) or duplicated entries, the bad hypothesis is removed and the hypothesis function calls itself on the reduced sudoku matrix. 

If the hypothesis is neither a clear solution nor a failure, hypothesis calls itself and keeps going until there is a solution or failure. 

This program works on easy up to fairly difficult sudoku puzzles. 

There are several puzzles to try in this repo: sudoku_data.csv is easy, sudo101.csv is medium, and sudo162.csv fairly hard. 




