# Sudoku Solver - Marjorie Sayer

import sys
import csv

def read_csv_file(filename):
    """
    Reads in unsolved sudoku from .csv file.
    Formats the entries as a 9x9 matrix of lists.
    """
    matrix = []
    with file(filename, 'U') as fileHandle:
        csvReader = csv.reader(fileHandle, delimiter=',', quotechar='"')
        for row in csvReader:
            matrix.append(row)
    matrix = [[int(elem) for elem in row] for row in matrix]
    return matrix

def sum_list_lengths(matrix):
    """
    Computes the sum of the lengths of the 81 lists in the
    working sudoku. If the length is 81, all lists are length 1.
    """
    a = [[len(elem) for elem in row]for row in matrix]
    sumcollect = sum(sum(row) for row in a)

    return sumcollect


def zero_worker(work_list):
    """
    Converts zero entries in initial sudoku matrix to lists of
    possibilities, from 1 through 9.
    """
    result = [[elem] if elem != 0 else range(1, 10) for row in work_list for elem in row]
    result = [result[9*x:9*x + 9] for x in range(9)]
    if sum_list_lengths(result) > 81:
        return result
    elif sum_list_lengths(result) < 81:
        print "error on input"


def row_reducer(matrix):
    """
    Reduces possibilities within rows according to the presence of values in rows.
    Tests for over-reduction (an entry reduced to an empty list), and duplicate entries.
    """

    distinct = True
    result = [[[0]*9 for i in range(9)] for j in range(9)]
    for row in matrix:
        row_index = matrix.index(row)
        # anti_vector is the set of existing fully reduced values in the row.
        anti_vector = [row[x][0] for x in range(9) if len(row[x]) == 1]

        # replacer is the complement of anti_vector in the set 1 through 9.
        replacer = list(set(range(1, 10)) - set(anti_vector))

        # Replace non-unit-length lists with the intersection of list and replacer:
        row = [elem if len(elem) == 1 else list(set(elem) & set(replacer)) for elem in row]

        # Test for zero-length entries.

        len_vector = [len(elem) for elem in row]
        if min(len_vector) == 0:
            distinct = False
            return distinct, matrix
            break

        # Test for duplicate entries.
        units_vector = [elem[0] for elem in row if len(elem) == 1]
        units_range = len(units_vector)
        bool_dups = [units_vector[i]==units_vector[j] for i in range(units_range) for j in range(units_range) if i != j]

        dup_test = any(bool_dups)
        if dup_test == True:
            distinct = False
            return distinct, matrix
            break

        result[row_index] = row

    if distinct == True:
        return distinct, result
    else:
        return distinct, matrix

def column_reducer(matrix):
    """
    Reduces the possibilities within columns according to the presence of values in columns.
    """

    # Obtain the transpose of matrix, in order to work on rows:
    result = [[row[i] for row in matrix] for i in range(9)]

    # Reduce possibilities in the transpose using row_worker:
    distinct, result = row_reducer(result)

    # Take the transpose again to change rows to columns.
    result = [[row[i] for row in result] for i in range(9)]

    # A value of distinct = False means a problem with the current entry hypothesis
    if distinct == True:
        return distinct, result
    else:
        return distinct, matrix



def sub_reducer(matrix):
    """
    Reduces possibilities in 3x3 sub-matrices according to presence of values in sub-matrices.
    """
    mid_result = [[[0]*9 for i in range(9)] for j in range(9)]

    # Convert the nine 3x3 sub-matrices to rows, to allow row reduction:
    for k in range(9):
        jlower = 3*(k % 3)
        jupper = jlower + 3
        j_range = range(jlower, jupper)

        ilower = 3*(k // 3)
        iupper = ilower + 3
        i_range = range(ilower, iupper)

        mid_result[k] = [matrix[i][j] for i in i_range for j in j_range]

    distinct, mid_result = row_reducer(mid_result)

    # A value of distinct = False means a problem with the current entry hypothesis
    if distinct == False:
        return distinct, matrix

    # Convert result back to format of sudoku - each row to correct 3x3 submatrix
    result = [[[0]*9 for i in range(9)] for j in range(9)]
    for n in range(9):
        xlower = 3*(n // 3)
        xupper = xlower + 3
        ylower = 3*(n % 3)
        yupper = ylower + 3
        x_range = range(xlower, xupper)
        y_range = range(ylower, yupper)
        result[n] = [mid_result[x][y] for x in x_range for y in y_range]

    # A value of distinct = False means a problem with the current entry hypothesis
    if distinct == True:
        return distinct, result
    else:
        return distinct, matrix


def endgame(work_list, path):
    """
    This function is only called if the sudoku is down to single entries
    in all slots, i.e. if the sum_list_lengths is 81.
    Writes the solution to a .csv file.
    """
    if sum_list_lengths(work_list) == 81:
        flattened_work_list = [[int(elem[0]) for elem in row] for row in work_list]
        with open(path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for row in flattened_work_list:
                writer.writerow(row)
    endgame = 1
    return endgame


def solver(matrix):
    """
    Runs basic row/column/sub9 reduction until no there is no improvement.
    """
    improved = 1
    iterations = 0
    distinct = True
    go_back = matrix
    while improved == 1:
        tester = sum_list_lengths(matrix)

        distinct, matrix = row_reducer(matrix)
        if distinct == False:
            return distinct, go_back
        distinct, matrix = column_reducer(matrix)
        if distinct == False:
            return distinct, go_back
        distinct, matrix = sub_reducer(matrix)
        if distinct == False:
            return distinct, go_back
        iterations += 1
        # If too many iterations occur, there could be a problem.
        if iterations > 20:
            break

        # Test to see if the matrix has been reduced:
        elif tester - sum_list_lengths(matrix) == 0:
            improved = 0

    return distinct, matrix

def hypothesis(matrix):
    """
    Solves sudoku puzzles by setting a value and testing
    for success or failure.
    """
    # First make sure the matrix needs more work.
    sum_ll = sum_list_lengths(matrix)
    if sum_ll == 81:
        success = True
        return success, matrix

    # Find first list of length > 1:

    first_occ = [(i, j) for i in range(9) for j in range(9) if len(matrix[i][j]) > 1][0]
    first_x = first_occ[0]
    first_y = first_occ[1]
    replacement = matrix[first_x][first_y]
    test_mx = matrix
    # For each element in the replacement list, see what leads to an error and remove it.
    take_out = 0
    for k in replacement:

        new_replacement = replacement
        test_mx[first_x][first_y] = [k]
        distinct, result = solver(test_mx)
        # If distinct has a value False there is over-reduction or duplicate entries.
        # This means that k is a bad hypothesis.
        if distinct == False:
            take_out = k
            break

        else:
            # Keep going with this hypothesis until success or failure:
            success, test_mx = hypothesis(test_mx)
            return success, test_mx

    # If there was a bad hypothesis, this code removes it from consideration and
    # marches forward with a reduced sudoku matrix, until there is success or failure.
    new_replacement.remove(take_out)
    matrix[first_x][first_y] = new_replacement
    success, matrix = hypothesis(matrix)
    return success, matrix

if __name__ == '__main__':
    """
    Main sudoku solver program.
    """
    inputFile = sys.argv[1]
    dataMatrix = read_csv_file(inputFile)
    dataMatrix = zero_worker(dataMatrix)
    distinct, dataMatrix = solver(dataMatrix)
    if sum_list_lengths(dataMatrix) > 81:
        success, dataMatrix = hypothesis(dataMatrix)
    if sum_list_lengths(dataMatrix) == 81:
        outputFile = sys.argv[2]
        game_end = endgame(dataMatrix, outputFile)

