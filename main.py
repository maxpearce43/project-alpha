"""Entry point for the group project.

`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward. Replace the placeholder below with your own core loop.
"""


board = [
    ["-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-"]
]


def display_board(board):
    print("1 2 3 4 5 6 7")

    for row in board:
        print(" ".join(row))


def drop_piece(board, column, piece):
    for row in range(5, -1, -1):
        if board[row][column] == "-":
            board[row][column] = piece
            return True

    return False


def check_winner(board, piece):

    # Horizontal
    for row in range(6):
        for col in range(4):
            if (board[row][col] == piece and
                board[row][col + 1] == piece and
                board[row][col + 2] == piece and
                board[row][col + 3] == piece):
                return True

    # Vertical
    for row in range(3):
        for col in range(7):
            if (board[row][col] == piece and
                board[row + 1][col] == piece and
                board[row + 2][col] == piece and
                board[row + 3][col] == piece):
                return True

    # Diagonal down-right
    for row in range(3):
        for col in range(4):
            if (board[row][col] == piece and
                board[row + 1][col + 1] == piece and
                board[row + 2][col + 2] == piece and
                board[row + 3][col + 3] == piece):
                return True

    # Diagonal up-right
    for row in range(3, 6):
        for col in range(4):
            if (board[row][col] == piece and
                board[row - 1][col + 1] == piece and
                board[row - 2][col + 2] == piece and
                board[row - 3][col + 3] == piece):
                return True

    return False


current_player = "X"

print("CONNECT 4")

while True:

    display_board(board)

    column = int(input(f"Player {current_player}, choose a column (1-7): "))

    if column < 1 or column > 7:
        print("Invalid column. Choose between 1 and 7.")
        continue

    column = column - 1

    move_worked = drop_piece(board, column, current_player)

    if move_worked == False:
        print("That column is full.")
        continue

    if check_winner(board, current_player):
        display_board(board)
        print(f"Player {current_player} wins!")
        break

    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"