Matching games are a popular class of games, with titles like Bejeweled and
Candy Crush receiving great success over recent years. In this assignment we
will create our own basic matching game. Our game consists of a number of coloured
pieces on a two-dimensional board. Each piece can be represented as a string
containing a single upper-case character between 'A' and 'Y'. The character 'Z'
is used to indicate a blank position on the board. The board can be represented
in Python by a list of lists. For example, the board below could be represented as:
board = [['B', 'G', 'B', 'Y'], ['G', 'B', 'Y', 'Y'], ['G', 'G', 'Y', 'Z'],
['B', 'Z', 'Z', 'Z']]

Note that board[0][0] therefore corresponds to the position in the top-left corner
of the board. A 4 x 4 board is shown, but our game will allow for boards of sizes
up to 99 x 99. A move is made by selecting a piece and specifying a direction
in which it should be moved (up, down, left or right).

The piece can be selected by specifying its position on the board. To do so, we
use a tuple (row, column) where row and column are the index values of the row and
column on the board that contain the piece. To specify the direction we use a
single lower case character as follows:

'u': Up
'd': Down
'l': Left
'r': Right

Four pieces of the same colour may be eliminated from the board by moving them into
a 2 x 2 square. For example, in the scenario above the green triangle at (0, 1)
could be moved downwards to (1, 1). This move would eliminate all four
green triangles from the board.
