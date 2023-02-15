class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []

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
                    if self.board[row][col][1] == "P":
                        moves.append(self.get_pawn_moves)
                    elif self.board[row][col][1] == "R":
                        moves.append(self.get_rook_moves)
                    elif self.board[row][col][1] == "N":
                        moves.append(self.get_knight_moves)
                    elif self.board[row][col][1] == "B":
                        moves.append(self.get_bishop_moves)
                    elif self.board[row][col][1] == "K":
                        moves.append(self.get_king_moves)
                    elif self.board[row][col][1] == "Q":
                        moves.append(self.get_queen_moves)

    # move handler - the methods take position and return the list of possible moves for a given type of piece
    def get_pawn_moves(self, r, c):
        pass

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


    def get_chess_notation(self):
        start = self.cols_to_files[self.start_col] + self.rows_to_ranks[self.start_row]
        end = self.cols_to_files[self.end_col] + self.rows_to_ranks[self.end_row]
        return start + end
