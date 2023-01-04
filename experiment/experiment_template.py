import chess
import elo
from stockfish import Stockfish
import time

# consts
STOCKFISH_ELO = 1000


def evaluate_elo(p, stockfish: Stockfish, game_count=20, move_limit=20):
    stockfish_elo = STOCKFISH_ELO
    p_elo = 1000
    time_per_move = dict([(str(i), []) for i in range(move_limit)])
    game_status = dict([(i, 0) for i in range(game_count)])
    elo_history = dict([(i, 0) for i in range(game_count)])

    # run game_count games:

    for game_number in range(game_count):
        board = chess.Board()
        stockfish.set_fen_position(board.board_fen())

        # run the current game until the move_limit is surpassed  or game ended:

        for _ in range(move_limit):
            if board.is_game_over:
                break

            # system under evaluation is white
            if game_number % 2 == 0:
                t = time.thread_time()
                # this is why we need the `get_move` method
                board.push_san(p.get_move(board))
                time_per_move[game_number].append(time.thread_time() - t)
                if board.is_game_over:
                    break
                stockfish.set_fen_position(board.fen())
                board.push_san(stockfish.get_best_move())

            # stockfish is white
            else:
                stockfish.set_fen_position(board.fen())
                board.push_san(stockfish.get_best_move())
                if board.is_game_over:
                    break
                t = time.thread_time()
                board.push_san(p.get_move(board))
                time_per_move[game_number].append(time.thread_time() - t)

        # check the status of the game:

        # it's a draw...
        if board.is_game_over and not board.is_checkmate:
            p_elo = elo.adjust_1vs1(p_elo, stockfish_elo, True)[0]
        # someone has won
        elif board.is_checkmate:
            result = board.outcome().result()
            white_win, black_win = result == "1-0", result == "0-1"
            # system has won
            if (white_win and game_number % 2 == 0) or (black_win and game_number % 2 != 0):
                p_elo = elo.adjust_1vs1(p_elo, stockfish_elo)[0]
                game_status[game_number] = 1
            # system has lost
            else:
                p_elo = elo.adjust_1vs1(stockfish_elo, p_elo)[1]
                game_status[game_number] = -1
        # game ongoing, evaluate position and declare the winner by score
        else:
            stockfish.set_fen_position(board.board_fen())
            # TODO: investigate this
            evaluation = stockfish.get_evaluation()["value"]
            # negative is advantage for black, positive for white, 0 for equality
            # duplicate code, cleanup required
            if evaluation == 0:
                p_elo = elo.adjust_1vs1(p_elo, stockfish_elo, True)[0]
            if (evaluation > 0 and game_number % 2 == 0) or (evaluation < 0 and game_number % 2 != 0):
                p_elo = elo.adjust_1vs1(p_elo, stockfish_elo)[0]
                game_status[game_number] = 1
            else:
                p_elo = elo.adjust_1vs1(stockfish_elo, p_elo)[1]
                game_status[game_number] = -1

        # update elo history:

        elo_history[game_number] = p_elo

    return (p_elo, elo_history, game_status, time_per_move)


if __name__ == "__main__":
    ...
