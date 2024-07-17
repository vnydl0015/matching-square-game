from collections import defaultdict

DIR_UP = "u"
DIR_DOWN = "d"
DIR_LEFT = "l"
DIR_RIGHT = "r"
BLANK_PIECE = "Z"

###############################################################################
def pretty_print(board):
    '''Takes in a board (a list of lists) and prints the pretty pattern,
    containing row and column indexes and the pieces within the input list'''

    # Finding greatest length of sub-lists in case they vary
    greatest_row_length = max(map(len, board))
    # Creating first two lines using greatest length
    column_index = "   "
    hyphen_line = "   "
    for i in range(greatest_row_length):
        # Adding column index
        column_index += f"{i:<3}"
        hyphen_line += "-" * 3
    print(column_index)
    print(hyphen_line)

    # Creating the rest of the board
    for j in range(len(board)):
        # Adding each row index
        row_line = f"{j:2d}|"
        # Adding each board value according to their row's length
        for k in range(len(board[j])):
            row_line += f"{board[j][k]:<3}"
        print(row_line)
    print()

###############################################################################
def validate_input(board, position, direction):
    """
    Returns True or returns False.
    Validates and returns True if all 6 criteria are met.
        Parameters:
            board: A list of lists
            position (int): 2 integer values (x, y)
            direction (str): One of "u", "d", "l", "r"
        Returns:
            True if all 6 criteria are met.
            False otherwise.
    """
    valid = True
    # Ensuring input arguments are not empty
    if not board or not position or not direction:
        return not valid

    # Validating at least 2 rows (and all have same length) and 2 columns
    if len(board) < 2 or min(map(len, board)) < 2 or \
            len(set(map(len, board))) != 1:
        return not valid

    # Validating if position is within board
    x, y = position
    if not 0 <= x < len(board) or not 0 <= y < len(board[0]):
        return not valid

    # Validating all board values as uppercase
    for i in range(len(board)):
        uppercase_validation_list = list(map(str.isupper, board[i]))
        if False in uppercase_validation_list:
            return not valid

    # Validating if direction is permitted
    if direction.lower().strip() not in (DIR_UP, DIR_DOWN, DIR_LEFT,
                                         DIR_RIGHT):
        return not valid

    # Creating dictionary to count each colour
    colour_count = defaultdict(int)
    for row in range(len(board)):
        for piece in board[row]:
            # "Z" are not recorded
            if piece != BLANK_PIECE:
                colour_count[piece] += 1
                # Ensuring input pieces are not all "Z"
    if len(colour_count) == 0:
        return not valid
    # Validating the number of same coloured-pieces as a multiple of 4
    for piece in colour_count:
        if colour_count[piece] % 4 != 0:
            return not valid

    return valid

###############################################################################
def legal_move(board, position, direction):
    """
    Returns True or returns False.
    Validates and swaps the positions of the involved pieces 1 and 2. Then
    calls for another check_adjacent() function to validate if one of the 2
    pieces ends up adjacent to the same colour.
        Parameters:
            board: A list of lists
            position (int): 2 integer values (x, y)
            direction (str): One of "u", "d", "l", "r"
        Returns:
            True if either one of the check_adjacent() is returned True.
            False otherwise.
    """
    x, y = position
    p1_pos = {'x': x, 'y': y}  # Stores piece 1's position

    # Ensuring both pieces are within board after moved
    if direction == DIR_UP and 0 <= x - 1 < len(board) - 1:
        p2_pos = {'x': x - 1, 'y': y}  # Stores piece 2's position
    elif direction == DIR_DOWN and 0 < x + 1 < len(board):
        p2_pos = {'x': x + 1, 'y': y}
    elif direction == DIR_LEFT and 0 <= y - 1 < len(board[0]) - 1:
        p2_pos = {'x': x, 'y': y - 1}
    elif direction == DIR_RIGHT and 0 < y + 1 < len(board[0]):
        p2_pos = {'x': x, 'y': y + 1}
    else:
        return False

    # Checking if either piece 1 or piece 2 is BLANK_PIECE
    if board[p1_pos['x']][p1_pos['y']] == BLANK_PIECE or \
            board[p2_pos['x']][p2_pos['y']] == BLANK_PIECE:
        return False

        # Swapping positions of piece 1 and piece 2
    board[p1_pos['x']][p1_pos['y']], board[p2_pos['x']][p2_pos['y']] = \
        board[p2_pos['x']][p2_pos['y']], board[p1_pos['x']][p1_pos['y']]

    # Calling for check_adjacent()
    return check_adjacent(board, p1_pos) or check_adjacent(board, p2_pos)


###############################################################################
def check_adjacent(board, pos):
    """
    Returns True or returns False.
    Validate and return True if either one of moved pieces ends up adjacent to
    the same colour.
        Parameters:
            board: A modified list of lists, received from legal_move()
            pos (dict): A dictionary that stores the position
        Returns:
            True if either one of moved pieces ends up adjacent to same colour.
            False otherwise.
    """
    # Identifying involved piece as "piece"
    piece = board[pos['x']][pos['y']]

    illegal = False
    # Validating if adjacent piece has same colour as "piece"
    if pos['x'] != 0 and piece == board[pos['x'] - 1][pos['y']] or \
            pos['y'] != 0 and piece == board[pos['x']][pos['y'] - 1] or \
            pos['x'] != len(board) - 1 and piece == board[pos['x'] + 1][pos['y']] or \
            pos['y'] != len(board[0]) - 1 and piece == board[pos['x']][pos['y'] + 1]:
        return not illegal

    return illegal

###############################################################################
def make_move(board, position, direction):
    """
    Returns a board.
    Validates and swaps the positions of the involved pieces 1 and 2. Then call
    for check_square() function to check square for both pieces (the piece with
    with a lesser row/column index will be checked first).
        Parameters:
            board: A list of lists
            position (int): 2 integer values (x, y)
            direction (str): One of "u", "d", "l", "r"
        Returns:
            Final board after all blanks are filled using fill_blank().
            Original board if the involved piece is "Z".
            Moved board after the legal moved, but no square is formed.
    """
    x, y = position
    # Creating "p1_pos" and "p2_pos" to store piece 1 and piece 2 positions
    p1_pos = {'x': x, 'y': y}
    if direction == DIR_UP:
        p2_pos = {'x': x - 1, 'y': y}
    elif direction == DIR_DOWN:
        p2_pos = {'x': x + 1, 'y': y}
    elif direction == DIR_LEFT:
        p2_pos = {'x': x, 'y': y - 1}
    elif direction == DIR_RIGHT:
        p2_pos = {'x': x, 'y': y + 1}

    # Return orignal board if either piece 1 or piece 2 is BLANK_PIECE
    if board[p1_pos['x']][p1_pos['y']] == BLANK_PIECE or \
            board[p2_pos['x']][p2_pos['y']] == BLANK_PIECE:
        return board

    # Swapping positions of piece 1 and piece 2
    board[p1_pos['x']][p1_pos['y']], board[p2_pos['x']][p2_pos['y']] = \
        board[p2_pos['x']][p2_pos['y']], board[p1_pos['x']][p1_pos['y']]

    # "store_board" stores a new board or None (if no square formed)
    store_board = []
    # Ordering pieces' positions, then call for check_square()
    if p1_pos['x'] < p2_pos['x'] or p1_pos['x'] == p2_pos['x'] and \
            p1_pos['y'] < p2_pos['y']:
        store_board.extend([check_square(board, p1_pos),
                            check_square(board, p2_pos)])
    else:
        store_board.extend([check_square(board, p2_pos),
                            check_square(board, p1_pos)])

    # Returning moved board after legal move but NO square formed
    if store_board.count(None) > 1:
        return board

    for final_board in list(filter(lambda x: x is not None, store_board)):
        # Returning final board after all blanks filled using fill_blank()
        return fill_blank(final_board)


###############################################################################
def check_square(board, pos):
    """
    Returns None or returns a new board.
    Checks for any square(s) formed. If there is a square, then replaces the
    pieces with "Z" before calling fill_blank(). If no, then returns None.
        Parameters:
            board: A modified list of lists, received from make_move() or
                   fill_blank()
            pos (dict): A dictionary that stores the position
        Returns:
            New board as received from the fill_blank().
            None if no square is detected.
    """
    # Identifying involved piece as "piece"
    piece = board[pos['x']][pos['y']]

    if piece != BLANK_PIECE:
        # Checking for x=0 and y=0 offset
        if pos['x'] != 0 and pos['y'] != 0:
            # Find and eliminate square in top left corner
            if piece == board[pos['x'] - 1][pos['y']] and \
                    piece == board[pos['x'] - 1][pos['y'] - 1] and \
                    piece == board[pos['x']][pos['y'] - 1]:
                board[pos['x'] - 1][pos['y']] = BLANK_PIECE
                board[pos['x'] - 1][pos['y'] - 1] = BLANK_PIECE
                board[pos['x']][pos['y'] - 1] = BLANK_PIECE
                board[pos['x']][pos['y']] = BLANK_PIECE
                return fill_blank(board)

        # Checking for x=0 and y=len(board[0])-1 offset
        if pos['x'] != 0 and pos['y'] != len(board[0]) - 1:
            # Find and eliminate square in top right corner
            if piece == board[pos['x'] - 1][pos['y']] and \
                    piece == board[pos['x'] - 1][pos['y'] + 1] and \
                    piece == board[pos['x']][pos['y'] + 1]:
                board[pos['x'] - 1][pos['y']] = BLANK_PIECE
                board[pos['x'] - 1][pos['y'] + 1] = BLANK_PIECE
                board[pos['x']][pos['y'] + 1] = BLANK_PIECE
                board[pos['x']][pos['y']] = BLANK_PIECE
                return fill_blank(board)

        # Checking for x=len(board)-1 and y=0 offset
        if pos['x'] != len(board) - 1 and pos['y'] != 0:
            # Find and eliminate square in bottom left corner
            if piece == board[pos['x'] + 1][pos['y']] and \
                    piece == board[pos['x'] + 1][pos['y'] - 1] and \
                    piece == board[pos['x']][pos['y'] - 1]:
                board[pos['x'] + 1][pos['y']] = BLANK_PIECE
                board[pos['x'] + 1][pos['y'] - 1] = BLANK_PIECE
                board[pos['x']][pos['y'] - 1] = BLANK_PIECE
                board[pos['x']][pos['y']] = BLANK_PIECE
                return fill_blank(board)

        # Checking for x=len(board)-1 and y=len(board[0])-1 offset
        if pos['x'] != len(board) - 1 and pos['y'] != len(board[0]) - 1:
            # Find and eliminate square in bottom right corner
            if piece == board[pos['x'] + 1][pos['y']] and \
                    piece == board[pos['x'] + 1][pos['y'] + 1] and \
                    piece == board[pos['x']][pos['y'] + 1]:
                board[pos['x'] + 1][pos['y']] = BLANK_PIECE
                board[pos['x'] + 1][pos['y'] + 1] = BLANK_PIECE
                board[pos['x']][pos['y'] + 1] = BLANK_PIECE
                board[pos['x']][pos['y']] = BLANK_PIECE
                return fill_blank(board)
    return None


###############################################################################
def fill_blank(board):
    """
    Returns a new board.
    Checks for "Z" in the board that has its square eliminated. Then fills in
    the blanks vertically before horizontally. Lastly, calls for check_square()
    for any more squares formed.
        Parameters:
            board: A modified list of lists, received from check_square() or
                   make_move()
        Returns:
            New board with either filled or semi-filled blanks.
    """
    # Move pieces vertically (from higher to lower column index) to fill blanks
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == BLANK_PIECE:
                # Ensuring pieces are within board after moved
                if i + 1 >= len(board):
                    pass
                else:
                    if board[i + 1][j] == BLANK_PIECE and i + 2 < len(board):
                        board[i][j], board[i + 2][j] = \
                            board[i + 2][j], board[i][j]
                    else:
                        board[i][j], board[i + 1][j] = \
                            board[i + 1][j], board[i][j]

    # Move pieces horizontally (from higher to lower row index) to fill blanks
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == BLANK_PIECE:
                # Ensuring pieces are within board after moved
                if j + 1 >= len(board[i]):
                    pass
                else:
                    if board[i][j + 1] == BLANK_PIECE and \
                            j + 2 < len(board[i]):
                        board[i][j], board[i][j + 2] = \
                            board[i][j + 2], board[i][j]
                    else:
                        board[i][j], board[i][j + 1] = \
                            board[i][j + 1], board[i][j]

    # Calling check_square() to eliminate by-product square(s)
    for i in range(len(board)):
        for j in range(len(board[i])):
            check_square(board, {"x": i, "y": j})

    # Returning filled or semi-filled board
    return board

###############################################################################

