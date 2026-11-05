"""Connect 4 - Milestone 2 (Board and rules slice).

Run `python main.py --help` for options. Game/save-resume and high-score features
(other team slices) plug into the menu in `menu()`.
"""

import argparse
import json

EMPTY = "-"
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # horizontal, vertical, two diagonals


class Board:
    """A Connect-N board: grid state plus the rules for dropping pieces and winning."""

    def __init__(self, rows=6, cols=7, connect_n=4):
        self.rows = rows
        self.cols = cols
        self.connect_n = connect_n
        self.grid = [[EMPTY] * cols for _ in range(rows)]

    def drop_piece(self, col, piece):
        """Drop `piece` into column `col` (0-based). Return the row used, or None if full/invalid."""
        if col < 0 or col >= self.cols:
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = piece
                return row
        return None

    def is_full(self):
        return all(cell != EMPTY for cell in self.grid[0])

    def count_direction(self, row, col, d_row, d_col, piece):
        """Recursively count consecutive `piece` cells starting at (row, col) going (d_row, d_col)."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return 0  # base case: off the board
        if self.grid[row][col] != piece:
            return 0  # base case: run ended
        return 1 + self.count_direction(row + d_row, col + d_col, d_row, d_col, piece)

    def check_winner(self, row, col):
        """True if the piece at (row, col) is part of a line of `connect_n` or more."""
        piece = self.grid[row][col]
        if piece == EMPTY:
            return False
        for d_row, d_col in DIRECTIONS:
            # count the piece itself once, then each side of it
            forward = self.count_direction(row + d_row, col + d_col, d_row, d_col, piece)
            backward = self.count_direction(row - d_row, col - d_col, -d_row, -d_col, piece)
            if 1 + forward + backward >= self.connect_n:
                return True
        return False

    def __str__(self):
        header = " ".join(str(c + 1) for c in range(self.cols))
        return header + "\n" + "\n".join(" ".join(row) for row in self.grid)

    def to_dict(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "connect_n": self.connect_n,
            "grid": self.grid,
        }

    @classmethod
    def from_dict(cls, data):
        board = cls(data["rows"], data["cols"], data["connect_n"])
        board.grid = [list(row) for row in data["grid"]]
        return board

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path):
        """Load a board from JSON. Return None if the file is missing or invalid."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return cls.from_dict(json.load(f))
        except (OSError, ValueError, KeyError, TypeError):
            return None


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Connect 4 (configurable board size).")
    parser.add_argument("--rows", type=int, default=6, help="board rows (default 6)")
    parser.add_argument("--cols", type=int, default=7, help="board columns (default 7)")
    parser.add_argument("--connect", type=int, default=4,
                        help="pieces in a row needed to win (default 4)")
    parser.add_argument("--board-file", default="board.json",
                        help="file used by 'Save/Load board' (default board.json)")
    args = parser.parse_args(argv)
    if args.rows < 2 or args.cols < 2:
        parser.error("--rows and --cols must be at least 2")
    if args.connect < 2 or args.connect > max(args.rows, args.cols):
        parser.error("--connect must be between 2 and max(rows, cols)")
    return args


def ask_column(board, player):
    """Prompt until a valid column (1-N) is entered. Returns 0-based column, or None for 'q'/'s'."""
    while True:
        text = input(f"Player {player}, column (1-{board.cols}), 's' save, 'q' menu: ").strip().lower()
        if text in ("q", "s"):
            return text
        if text.isdigit() and 1 <= int(text) <= board.cols:
            return int(text) - 1
        print(f"Enter a number from 1 to {board.cols}.")


def play(board, board_file, player="X"):
    """Run one game loop on `board`. Returns when the game ends or the player leaves."""
    while True:
        print()
        print(board)
        choice = ask_column(board, player)
        if choice == "q":
            return
        if choice == "s":
            board.save(board_file)
            print(f"Board saved to {board_file}.")
            continue
        row = board.drop_piece(choice, player)
        if row is None:
            print("That column is full.")
            continue
        if board.check_winner(row, choice):
            print()
            print(board)
            print(f"Player {player} wins!")
            return
        if board.is_full():
            print()
            print(board)
            print("It's a draw.")
            return
        player = "O" if player == "X" else "X"


def menu(args):
    while True:
        print("\n=== CONNECT 4 ===")
        print("1. New game")
        print("2. Load board from file")
        print("3. Quit")
        choice = input("> ").strip()
        if choice == "1":
            play(Board(args.rows, args.cols, args.connect), args.board_file)
        elif choice == "2":
            board = Board.load(args.board_file)
            if board is None:
                print(f"No valid board in {args.board_file}.")
            else:
                play(board, args.board_file)
        elif choice == "3":
            return
        else:
            print("Choose 1, 2 or 3.")


def main():
    menu(parse_args())


if __name__ == "__main__":
    main()
