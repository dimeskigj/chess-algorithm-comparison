from alpha_beta_pruning import *
from chess import Board


class MoveGenerator:
    def get_move(self, board: Board):
        result = minimax(
            chess.Board(board.fen()),
            [board.san(i) for i in list(board.legal_moves)],
            (len(board.move_stack) % 2) ^ 1,
            board.is_game_over(),
            3)  # depth should probs be increased when we're doing real testing
        return result[2]
