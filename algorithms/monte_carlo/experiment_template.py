import chess
import elo
from stockfish import Stockfish
import time
from tqdm import tqdm
import json

from move_generator_monte_carlo import MoveGenerator as MonteCarloMoveGenerator

# consts
STOCKFISH_ELO = 400
WIN_EVAL = 9999
LOSE_EVAL = -9999


def evaluate_elo(p, stockfish: Stockfish, game_count=20, move_limit=20):
    stockfish_elo = STOCKFISH_ELO
    p_elo = 400
    time_per_move = dict([(i, []) for i in range(game_count)])
    game_status = []
    elo_history = []
    eval_history = []

    # run game_count games:

    for game_number in range(game_count):
        board = chess.Board()
        stockfish.set_fen_position(board.board_fen())

        # run the current game until the move_limit is surpassed  or game ended:

        for _ in tqdm(range(move_limit), desc=f"Playing moves for game {game_number + 1}.", ascii=False, ncols=75):
            if board.is_game_over():
                break

            # system under evaluation is white
            if game_number % 2 == 0:
                t = time.thread_time()
                # this is why we need the `get_move` method
                board.push_san(p.get_move(board))
                time_per_move[game_number].append(time.thread_time() - t)
                if board.is_game_over():
                    break
                stockfish.set_fen_position(board.fen())
                board.push_san(stockfish.get_best_move())

            # stockfish is white
            else:
                stockfish.set_fen_position(board.fen())
                board.push_san(stockfish.get_best_move())
                if board.is_game_over():
                    break
                t = time.thread_time()
                board.push_san(p.get_move(board))
                time_per_move[game_number].append(time.thread_time() - t)

        # check the status of the game:

        # it's a draw...
        if board.is_game_over() and not board.is_checkmate():
            eval_history.append(0)
            p_elo = elo.rate_1vs1(p_elo, stockfish_elo, True)[0]
        # someone has won
        elif board.is_checkmate():
            result = board.outcome().result()
            white_win, black_win = result == "1-0", result == "0-1"
            # system has won
            if (white_win and game_number % 2 == 0) or (black_win and game_number % 2 != 0):
                p_elo = elo.rate_1vs1(p_elo, stockfish_elo)[0]
                game_status.append(1)
                eval_history.append(WIN_EVAL)
            # system has lost
            else:
                p_elo = elo.rate_1vs1(stockfish_elo, p_elo)[1]
                game_status.append(-1)
                eval_history.append(LOSE_EVAL)
        # game ongoing, evaluate position and declare the winner by score
        else:
            # TODO: investigate this
            stockfish.set_fen_position(board.board_fen())
            evaluation = stockfish.get_evaluation()["value"]
            eval_history.append(
                evaluation * (-1 if game_number % 2 != 0 else 1))
            # negative is advantage for black, positive for white, 0 for equality
            # duplicate code, cleanup required
            if evaluation == 0:
                p_elo = elo.rate_1vs1(p_elo, stockfish_elo, True)[0]
            if (evaluation > 0 and game_number % 2 == 0) or (evaluation < 0 and game_number % 2 != 0):
                p_elo = elo.rate_1vs1(p_elo, stockfish_elo)[0]
                game_status.append(1)
            else:
                p_elo = elo.rate_1vs1(stockfish_elo, p_elo)[1]
                game_status.append(-1)

        # update elo history:

        elo_history.append(p_elo)

    return {
        "system elo": p_elo,
        "elo history": elo_history,
        "game evaluation history": eval_history,
        "game status history": game_status,
        "time per move": time_per_move}


if __name__ == "__main__":
    p = MonteCarloMoveGenerator()
    sf = Stockfish(r"algorithms\stockfish-11-win\Windows\stockfish_20011801_x64.exe")
    sf.set_elo_rating(STOCKFISH_ELO)
    sf.set_skill_level(0)
    res = evaluate_elo(p, sf, 10, 30)
    print(res)
    with open("monte_carlo_30its.json", "w") as f:
        json.dump(res, f)
