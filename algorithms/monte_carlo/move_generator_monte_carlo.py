from monte_carlo_implementation import *
from chess import Board

class MoveGenerator:
    def __init__(self, agent):
        self.agent = agent

    def get_move(self, board: Board):
        root = node()
        root.state = board
        return mcts_pred(
            root, 
            board.is_game_over(), 
            (len(board.move_stack) % 2) ^ 1)
