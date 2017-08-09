import pprint
pp = pprint.PrettyPrinter(indent=4)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Set some global variables // Since solution_test doesn't include parameters
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    diagonal_units_a = [[rows[i]+cols[i] for i in range(0, len(rows))]]
    diagonal_units_b = [[rows[(len(rows)-1-i)]+cols[i] for i in range(0, len(rows))]]
    unitlist = row_units + column_units + square_units + diagonal_units_a + diagonal_units_b
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

    # Find all instances of naked twins
    #print('-----')
    #print(values)
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    #print(potential_twins)

    # Loop through potential twins
    for box in potential_twins:
        confirmed_twin = None
        #print(values[box])
        for peer in peers[box]:
            if(len(values[peer])==2):
                #print(box + ':' + values[box] + '-->' + peer + ':' + values[peer])
                if values[box] == values[peer]:
                    #print('found a twin')
                    confirmed_twin = peer
                    break
        if confirmed_twin:
            #print('confirmed twin:' + box + ':' + confirmed_twin)
            box_vals = [c for c in values[box]]
            for unit in unitlist:
                if box in unit and confirmed_twin in unit:
                    for u in unit:
                        #print('u:' + u + ':' + values[u])
                        if u != box and u != confirmed_twin:
                            u_vals = [c for c in values[u]]
                            for val in u_vals:
                                if val in box_vals:
                                    values[u] = values[u].replace(val, '')
                        #print('-->' + values[u])
    #print(values)
    # Eliminate the naked twins as possibilities for their peers

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid, boxes):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'

    boxes = cross(rows, cols)

    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, peers):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values, unitlist):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            #print(dplaces)
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values, peers, unitlist):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    #solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values, peers)
        values = only_choice(values, unitlist)
        # Reduce the puzzle with naked twins strategy
        values = naked_twins(values)
        #pp.pprint(temp)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values, boxes, peers, unitlist):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, peers, unitlist)

    # Where did this come from??
    if values is False:
        return False ## Failed earlier
    # Check if all values found
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku, boxes, peers, unitlist)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Set some global variables
    rows = 'ABCDEFGHI'
    cols = '123456789'

    boxes = cross(rows, cols)

    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    #print(cross(rows,cols))
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    #print(square_units)

    # Define diaganal units for peers
    diagonal_units_a = [[rows[i]+cols[i] for i in range(0, len(rows))]]
    diagonal_units_b = [[rows[(len(rows)-1-i)]+cols[i] for i in range(0, len(rows))]]
    #print(diagonal_units_a)
    #print(diagonal_units_b)
    unitlist = row_units + column_units + square_units + diagonal_units_a + diagonal_units_b
    #print(unitlist)
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    #print(units)
    #print("--")
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
    #pp.pprint(peers)

    # Convert Grid to Dictionary
    puzzle = grid_values(grid, boxes)
    #pp.pprint(puzzle)

    # Reduce the puzzle
    puzzle = reduce_puzzle(puzzle, peers, unitlist)
    #pp.pprint(puzzle)

    # Search
    puzzle = search(puzzle, boxes, peers, unitlist)

    # Return puzzle
    return puzzle



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
