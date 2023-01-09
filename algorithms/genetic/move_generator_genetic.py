import monte_carlo_opt

class GeneticMoveGenerator:
    def __init__(self, agent):
        self.agent = agent

    def get_move(self, board):
        move = monte_carlo_opt.monte_carlo_algo(board, lambda input: self.agent.neural_network(input.reshape(1, 8, 8, 12)))
        return str(move)
