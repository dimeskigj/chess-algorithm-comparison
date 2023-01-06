from alpha_beta_pruning import minimax

class MoveGenerator:
    def __init__(self, agent):
        self.agent = agent

    def get_move(self, board):
        move = ""
        return move