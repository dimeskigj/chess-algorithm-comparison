'''
 *    author:  Ishaan Gupta
 *    created: 8.11.2020 15:04:06       
'''
import chess
import chess.pgn
import chess.engine

scores = {'p':-1,'n':-3,'b':-3,'r':-5,'q':-9,'k':-10**5,'P':1,'N':3,'B':3,'R':5,'Q':9,'K':10**5}

def evaluate(fen):
    global scores
    sc = 0
    for i in fen:
        if(i not in scores):
            continue
        sc+=scores[i]
    return sc
def minimax(tmp_board,all_moves,white,over,depth,alpha=-10**5-5,beta=10**5+5):
    fen = tmp_board.fen()
#     print(fen)
    if(over or depth==0):
        if(over):
            if(tmp_board.result()[0]=='1'):
                return (tmp_board,10**5+1,'')
            elif(tmp_board.result()[-1]=='1'):
                return (tmp_board,-10**5-1,'')
            else:
                return (tmp_board,0,'')
        if(white):
            mx = -10**5
            move = ''
            for i in all_moves:
                tmp_board.push_san(i)
                #white
                all_moves = [tmp_board.san(i) for i in list(tmp_board.legal_moves)]
                val = evaluate(tmp_board.fen().split()[0])
                
                if(mx<val):
                    mx = val
                    move = i
                alpha = max(alpha,mx)
                if(beta<=alpha):
                    tmp_board = chess.Board(fen)
                    break
                tmp_board = chess.Board(fen)
            return (tmp_board,mx,move)
        else:
            mn = 10**5
            move = ''
            for i in all_moves:
                tmp_board.push_san(i)
                all_moves = [tmp_board.san(i) for i in list(tmp_board.legal_moves)]
                val = evaluate(tmp_board.fen().split()[0])
                
                if(mn>val):
                    mn = val
                    move = i
                beta = min(beta,mn)
                if(beta<=alpha):
                    tmp_board = chess.Board(fen)
                    break
                tmp_board = chess.Board(fen)
            return (tmp_board,mn,move)
            
    if(white):
        mx = -10**6
        move = ''
        for i in all_moves:
            tmp_board.push_san(i)
            
            tmp_all_moves = [tmp_board.san(i) for i in list(tmp_board.legal_moves)]
            val = minimax(tmp_board,tmp_all_moves,0,tmp_board.is_game_over(),depth-1,alpha,beta)
            if(mx<val[1]):
                mx = val[1]
                move = i
            tmp_board = chess.Board(fen)
            alpha = max(alpha,mx)
            if(beta<=alpha):
                tmp_board = chess.Board(fen)
                break
            tmp_board = chess.Board(fen)
        return (tmp_board,mx,move)
    else:
        mn = 10**6
        move = ''
        for i in all_moves:
            tmp_board.push_san(i)
            tmp_all_moves = [tmp_board.san(i) for i in list(tmp_board.legal_moves)]
            val = minimax(tmp_board,tmp_all_moves,1,tmp_board.is_game_over(),depth-1,alpha,beta)
            if(mn>val[1]):
                mn = val[1]
                move = i
            tmp_board = chess.Board(fen)
            beta = min(beta,mn)
            if(beta<=alpha):
                tmp_board = chess.Board(fen)
                break
            tmp_board = chess.Board(fen)
        return (tmp_board,mn,move)
