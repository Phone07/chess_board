class ChessBoard:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Create an 8x8 chess board with pieces in their initial positions
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p"] * 8,
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            ["P"] * 8,
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

    def display(self):
        print("  a b c d e f g h")
        print("  ----------------")
        for i, row in enumerate(self.board):
            print(8 - i, "|", " ".join(row), "|", 8 - i)
        print("  ----------------")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        # Translate positions to indices
        start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord("a")
        end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord("a")

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        # Validate if the start position contains a piece
        if piece == " ":
            print("No piece at the starting position!")
            return False

        # Check if the move is valid for the given piece
        if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
            print(f"Invalid move for {piece.upper()}!")
            return False

        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = " "
        return True

    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        # Calculate move differences
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Define movement rules for each piece
        if piece == "P":  # White pawn
            # Forward move (no capture)
            if col_diff == 0:
                # Single step forward
                if row_diff == -1 and self.board[end_row][end_col] == " ":
                    return True
                # Double step forward from the starting position
                if row_diff == -2 and start_row == 6 and self.board[end_row][end_col] == " " and \
                        self.board[start_row - 1][start_col] == " ":
                    return True
            # Diagonal capture
            if abs(col_diff) == 1 and row_diff == -1 and self.board[end_row][end_col].islower():
                return True

        elif piece == "p":  # Black pawn
            # Forward move (no capture)
            if col_diff == 0:
                # Single step forward
                if row_diff == 1 and self.board[end_row][end_col] == " ":
                    return True
                # Double step forward from the starting position
                if row_diff == 2 and start_row == 1 and self.board[end_row][end_col] == " " and \
                        self.board[start_row + 1][start_col] == " ":
                    return True
            # Diagonal capture
            if abs(col_diff) == 1 and row_diff == 1 and self.board[end_row][end_col].isupper():
                return True

        # Rules for other pieces remain unchanged...
        elif piece == "r":  # Rook
            return self.is_straight_move(start_row, start_col, end_row, end_col)
        elif piece == "n":  # Knight
            return (abs(row_diff), abs(col_diff)) in [(2, 1), (1, 2)]
        elif piece == "b":  # Bishop
            return self.is_diagonal_move(start_row, start_col, end_row, end_col)
        elif piece == "q":  # Queen
            return (
                    self.is_straight_move(start_row, start_col, end_row, end_col)
                    or self.is_diagonal_move(start_row, start_col, end_row, end_col)
            )
        elif piece == "k":  # King
            return max(abs(row_diff), abs(col_diff)) == 1

        return False

    def is_straight_move(self, start_row, start_col, end_row, end_col):
        # Check for straight-line movement
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            for c in range(start_col + step, end_col, step):
                if self.board[start_row][c] != " ":
                    return False
            return True
        elif start_col == end_col:  # Vertical move
            step = 1 if end_row > start_row else -1
            for r in range(start_row + step, end_row, step):
                if self.board[r][start_col] != " ":
                    return False
            return True
        return False

    def is_diagonal_move(self, start_row, start_col, end_row, end_col):
        # Check for diagonal movement
        row_diff = end_row - start_row
        col_diff = end_col - start_col
        if abs(row_diff) != abs(col_diff):
            return False
        step_row = 1 if row_diff > 0 else -1
        step_col = 1 if col_diff > 0 else -1
        for i in range(1, abs(row_diff)):
            if self.board[start_row + i * step_row][start_col + i * step_col] != " ":
                return False
        return True


def main():
    print("Welcome to Chess!")
    chess_board = ChessBoard()
    chess_board.display()

    while True:
        move = input("Enter your move (e.g., e2 e4, or 'exit' to quit): ").strip()
        if move.lower() == "exit":
            print("Exiting the game. Goodbye!")
            break

        try:
            start, end = move.split()
            if chess_board.move_piece(start, end):
                chess_board.display()
            else:
                print("Move failed. Try again.")
        except ValueError:
            print("Invalid input format. Use 'e2 e4' format.")

if __name__ == "__main__":
    main()
