class GameState:
    def __init__(self):

        # The representation of the board
        # -- means that the square is empty, b means black, w means white
        # The uppercase letters symbolise different types of pieces
        # e.g. "wB" symbolises a white bishop
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "bP", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                               "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    # gets all possible moves considering checks
    def get_legal_moves(self):
        return self.get_all_moves()

    # gets all possible moves without considering checks
    # traverses the whole board looking for squares with pieces of a particular color on them
    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if ((self.board[row][col][0] == "w" and self.white_to_move) or
                        (self.board[row][col][0] == "b" and not self.white_to_move)):
                    piece = self.board[row][col][1]
                    if piece == "P":  # only for testing the dictionary as the other functions are yet to be implemented
                        moves.extend(self.move_functions["P"](row, col))

        return moves

    # move handler - the methods take position and return the list of possible moves for a given type of piece
    def get_pawn_moves(self, r, c):
        moves = []
        # find white's moves
        if self.white_to_move:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                # if it's white and on row 6 it means that the pawn hasn't been moved yet,
                # so we check if the square 2 rows further is empty
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            # now, let's check if the pawn can attack
            # left attack
            if c != 0 and self.board[r-1][c-1] != "--":
                move = Move((r, c), (r-1, c-1), self.board)
                if move.piece_captured[0] == "b":
                    moves.append(move)
            if c != 7 and self.board[r-1][c+1] != "--":
                move = Move((r, c), (r-1, c+1), self.board)
                if move.piece_captured[0] == "b":
                    moves.append(move)
        # find black's moves
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                # if it's white and on row 6 it means that the pawn hasn't been moved yet,
                # so we check if the square 2 rows further is empty
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # now, let's check if the pawn can attack
            # left attack - from white's perspective
            if c != 0 and self.board[r + 1][c - 1] != "--":
                move = Move((r, c), (r + 1, c - 1), self.board)
                if move.piece_captured[0] == "w":
                    moves.append(move)
            # right attack - from white's perspective
            if c != 7 and self.board[r + 1][c + 1] != "--":
                move = Move((r, c), (r + 1, c + 1), self.board)
                if move.piece_captured[0] == "w":
                    moves.append(move)
        return moves

    def get_rook_moves(self, r, c):
        pass

    def get_knight_moves(self, r, c):
        pass

    def get_bishop_moves(self, r, c):
        pass

    def get_king_moves(self, r, c):
        pass

    def get_queen_moves(self, r, c):
        pass


class Move:
    # Chess notation - convert our row/col to rank/file and back
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start, end, board):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # creating a unique moveID - allow us to compare 2 moves easily
        # if the ids are the same - the moves have the same start and end
        # they are effectively the same move - given the state of the board
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return other.moveID == self.moveID

    def get_chess_notation(self):
        start = self.cols_to_files[self.start_col] + self.rows_to_ranks[self.start_row]
        end = self.cols_to_files[self.end_col] + self.rows_to_ranks[self.end_row]
        return start + end
