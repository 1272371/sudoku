# Sudoku Solver - Marjorie Sayer

import sys
import csv

def read_csv_file(filename):
    # read in unsolved sudoku from .csv file.
    matrix = []
    with file(filename, 'U') as fileHandle:
        csvReader = csv.reader(fileHandle, delimiter=',', quotechar='"')
        for row in csvReader:
            matrix.append(row)
    matrix = [[int(row[i]) for i in range(len(row))] for row in matrix]
    return matrix

def sum_list_lengths(matrix):
    """
    Checks the sum of the lengths of the 81 lists in the
    working sudoku. If the length is 81, all values are solved.
    :rtype : int
    """
    a = [[len(row[i]) for i in range(9)]for row in matrix]
    sumcollect = 0
    for i in range(9):
        test = sum(a[i])
        sumcollect = sumcollect + test
    return sumcollect


def zero_worker(work_list):
    # Converts zero (empty) entries in incoming raw sudoku to lists of
    # possibilities, from 1 through 9.
    result = [[row[i]] if row[i] != 0 else range(1, 10) for row in work_list for i in range(9)]
    result = [result[9*x:9*x + 9] for x in range(9)]
    if sum_list_lengths(result) > 81:
        return result
    else: print "error on input"


def row_reducer(matrix):
    # Reduces possibilities within rows according to the presence of values in rows.

    distinct = True
    result = [[[0]*9 for i in range(9)] for j in range(9)]
    for row in matrix:
        row_index = matrix.index(row)
        anti_vector = [row[x][0] for x in range(9) if len(row[x]) == 1]

        replacer = list(set(range(1, 10)) - set(anti_vector))

        row = [row[x] if len(row[x]) == 1 else list(set(row[x]) & set(replacer)) for x in range(9)]

        # Test for a contradiction caused by the reduction. An entry might be reduced
        # to zero if a bad hypothesis is made.
        len_vector = [len(row[x]) for x in range(9)]

        if min(len_vector) == 0:
            distinct = False

        # Test for a contradiction caused by repeated values in a row.
        units_vector = [row[n][0] for n in range(9) if len(row[n]) == 1]
        units_range = len(units_vector)
        bool_dups = [units_vector[i]==units_vector[j] for i in range(units_range) for j in range(units_range) if i != j]

        dup_test = any(bool_dups)
        if dup_test == True:
            distinct = False

        result[row_index] = row

    if sum_list_lengths(matrix) - sum_list_lengths(result) == 0:
        print "no improvement"

    return distinct, result

def example(matrix):
    success, matrix = row_reducer(matrix)

def column_reducer(matrix):
    # Reduces the possibilities within columns according to the presence of values in columns.

    matrix = [[row[i] for row in matrix] for i in range(9)]

    # reduce possibilities in the transpose using row_worker
    distinct, matrix = row_reducer(matrix)

    # Take the transpose again to produce a correct result.
    result = [[row[i] for row in matrix] for i in range(9)]

    return distinct, result


def sub_reducer(matrix):
    # Reduces possibilities in 3x3 sub-matrices according to presence of values in sub-matrices.

    mid_result = [[[0]*9 for i in range(9)] for j in range(9)]

    for k in range(9):
        jlower = 3*(k % 3)
        jupper = jlower + 3
        j_range = range(jlower, jupper)

        ilower = 3*(k // 3)
        iupper = ilower + 3
        i_range = range(ilower, iupper)

        mid_result[k] = [matrix[i][j] for i in i_range for j in j_range]

    distinct, mid_result = row_reducer(mid_result)

    # convert result back to format of sudoku - each row to correct 3x3 submatrix
    result = [[[0]*9 for i in range(9)] for j in range(9)]
    for n in range(9):
        xlower = 3*(n // 3)
        xupper = xlower + 3
        ylower = 3*(n % 3)
        yupper = ylower + 3
        x_range = range(xlower, xupper)
        y_range = range(ylower, yupper)
        result[n] = [mid_result[x][y] for x in x_range for y in y_range]

    return distinct, result


def endgame(work_list, path):
    # This function is only called if the sudoku is down to single entries
    # in all slots, i.e. if the sum_list_lengths is 81.
    # Writes the solution to a .csv file.
    if sum_list_lengths(work_list) == 81:
        flattened_work_list = [[int(row[i][0]) for i in range(len(row))] for row in work_list]
        with open(path, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for row in flattened_work_list:
                writer.writerow(row)
    endgame = 1
    return endgame


def solver(matrix):
    # Runs basic row/column/sub9 reduction until no there is no improvement.
    improved = 1
    iterations = 0
    while improved == 1:
        tester = sum_list_lengths(matrix)
        distinct, matrix = row_reducer(matrix)
        if distinct == False:
            print "none"
            return None
        distinct, matrix = column_reducer(matrix)
        if distinct == False:
            print "none"
            return None
        distinct, matrix = sub_reducer(matrix)
        if distinct == False:
            print "none"
            return None
        iterations += 1
        print "iterations =", iterations
        if tester - sum_list_lengths(matrix) == 0:
            improved = 0
    return matrix

def hypothesis(matrix):

    sum_ll = sum_list_lengths(matrix)
    if sum_ll == 81:
        success = True
        return success, matrix

    # find first list of length > 1:

    first_occ = [(i, j) for i in range(9) for j in range(9) if len(matrix[i][j]) > 1][0]
    first_x = first_occ[0]
    first_y = first_occ[1]
    replacement = matrix[first_x][first_y]
    test_mx = matrix
    # for each element in the replacement list, see what leads to an error and remove it.
    for k in replacement:
        new_replacement = replacement
        test_mx[first_x][first_y] = [k]
        result = solver(test_mx)
        if result is None:

            new_replacement.remove(k)
            matrix[first_x][first_y] = new_replacement
            success, result = hypothesis(matrix)
            return success, result

        if sum_list_lengths(result) == 81:
            success = True
            return success, result

        if sum_list_lengths(result) > 81:
            success, result = hypothesis(test_mx)
            if success == False:
                continue





if __name__ == '__main__':
    inputFile = sys.argv[1]
    dataMatrix = read_csv_file(inputFile)
    dataMatrix = zero_worker(dataMatrix)
    dataMatrix = solver(dataMatrix)
    print "dataMatrix after basic", dataMatrix
    if sum_list_lengths(dataMatrix) > 81:
        success, dataMatrix = hypothesis(dataMatrix)
    if sum_list_lengths(dataMatrix) == 81:
        outputFile = sys.argv[2]
        game_end = endgame(dataMatrix, outputFile)
    





    print dataMatrix
