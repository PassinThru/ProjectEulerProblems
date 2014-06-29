rowsPerGrid = 9
columnsPerRow = 9
lengthOfSquare = 3

def readGrids():
    """Read in the grids. File structure consists of one line "Grid <number>" followed by
    9 lines of 9 digit numbers. Input is known to be properly formatted; in real world,
    checking for correct number of rows, lengths of columns, verification of digits only, etc.,
    would be added.

    :return: list of lists of 9 lists of 9 element lists representing 9x9 matrices
    """
    
    grids = []
    g = []
    for line in open('sudoku.txt'):
        if line[:4] == 'Grid':
            if g:
                # each time you encounter the "Grid" line, add the previous grid to the list
                grids.append(g)
            g = []
            continue
        # read in each 9 digit string and convert to a list of integers
        # add this list to the grid
        g.append([int(c) for c in line.rstrip()])

    # Add the last grid to the grid list
    grids.append(g)
    return grids

def notInRow(row, item):
    """Test for presence of number in row

    :param row: list of 9 ints
    :param item: int
    :return: boolean: True if not found, False otherwise
    """
    
    return not item in row

def notInCol(grid, column, item):
    """Test for presence of number in column of grid

    :param grid: list of 9 lists of 9 ints
    :param column: int
    :param item: int
    :return: boolean: True if item not found in grid column, False otherwise
    """
    
    return not item in [col[column] for col in grid]

def notInSquare(grid, row, column, item):
    """Test for presence of number in the cell's square

    :param grid: list of 9 lists of 9 ints
    :param row: int
    :param column: int
    :param item: 
    :return: boolean: True if item not found in square, False otherwise
    """

    # set x and y to the upper left cell of square
    x = column/lengthOfSquare*lengthOfSquare
    y = row/lengthOfSquare*lengthOfSquare
    return not item in [member for sublist in [r[x:x+lengthOfSquare] for r in grid[y:y+lengthOfSquare]] for member in sublist]

def nextCell(row, column):
    """Advance row and column to the next cell

    :param row: int
    :param column: int
    :return: 2 element tuple of int
    """
    column = (column + 1) % rowsPerGrid
    if column == 0:
        row = row + 1
    return (row, column)

def solve(grid, coordinates):
    """Main solver. Go through grid starting at coordinates provided, row by row. Add elements not already in row
    which are also not in column and not in the 3x3 square of the current cell. Recursively called, backtracking
    on failures, until all elements have been placed in all rows, or failure.

    :param grid: list of 9 lists of 9 ints
    :param coordinates: tuple of 2 ints
    :return: boolean: True if the grid was solved, False otherwise
    """
    row, startCol = coordinates # starting row and column for solution
    if row == rowsPerGrid:
        return True     # All rows in this grid are complete

    # lists of values already handled and to be handled
    placed = [c for c in grid[row] if c > 0]
    toPlace = [c for c in range(1,columnsPerRow+1) if not c in placed]

    if not toPlace:
        return solve(grid, (row+1, 0))    # nothing in this row remains to be handled - move to the next row

    # basic approach is to place values in empty cells row by row, using columns and squares as constraints
    for col in range(startCol, columnsPerRow):
        if grid[row][col] == 0:
            for i in toPlace:
                # Verify candidate doesn't conflict with existing values
                if notInRow(grid[row], i) and notInCol(grid, col, i) and notInSquare(grid, row, col, i):
                    # Set candidate
                    grid[row][col] = i

                    # Check next cell
                    if solve(grid, nextCell(row, col)):
                        return True

                    # Backtrack - candidate not viable - try next item in toPlace.
                    # Set to 0 in case further backtracking occurs
                    grid[row][col] = 0

            if toPlace:     # all possible values for this cell have been exhausted - Fail
                return False

    if not toPlace:     # all columns have been evaluated, and candidates remain - Fail
        return False
    return True

def main():
    """Read in grid list from sudoku.txt. Try to solve each grid. Convert first three cells of first row
    into a 3 digit number which is added to the total. Print the total after all grids in the grid list
    have been processed.
    """

    grids = readGrids()
    total = 0
    count = 1
    for g in grids:
        if not solve(g, (0, 0)):
            print 'Grid ' + str(count) + ' could not be solved'
        # Problem calls for treating the first three cells of first row as a three digit number,
        # and keeping a running total of all such values
        total = total + g[0][0]*100+g[0][1]*10+g[0][2]
        count = count+1
    print 'Pseudo-checksum of all 100 grids:', total

if __name__ == "__main__":
    main()
