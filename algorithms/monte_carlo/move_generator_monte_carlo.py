from monte_carlo_implementation import *
from chess import Board


class MoveGenerator:
    def get_move(self, board: Board):
        root = node()
        root.state = chess.Board(board.fen())
        return mcts_pred(
            root,
            board.is_game_over(),
            (len(board.move_stack) % 2) ^ 1)
