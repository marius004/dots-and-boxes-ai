from core.board import Board
from core.constants import *
from math import inf
import copy

class AlphaBeta:
    def alpha_beta(self, board: Board, depth: int, alpha: int, beta: int, maximizing: bool):
        best = (-inf, None) if maximizing else (inf, None)

        allowed_moves = board.allowed_moves()
        if depth == 0 or len(allowed_moves) == 0:
            return (self.evaluate(board), None)

        if maximizing:
            for move in allowed_moves:
                board_copy = copy.deepcopy(board)
                board_copy.move(move)

                # current player filled a box => gets another move
                if board_copy.player_turn() == board.player_turn():
                    next_move = self.alpha_beta(board_copy, depth - 1, alpha, beta, maximizing)
                else:
                    next_move = self.alpha_beta(board_copy, depth - 1, alpha, beta, not maximizing)

                if next_move[0] > best[0]:
                    best = (next_move[0], move)
                    
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break 
        else:
            for move in allowed_moves:
                board_copy = copy.deepcopy(board)
                board_copy.move(move)

                # current player filled a box => gets another move
                if board_copy.player_turn() == board.player_turn():
                    next_move = self.alpha_beta(board_copy, depth - 1, alpha, beta, not maximizing)
                else:
                    next_move = self.alpha_beta(board_copy, depth - 1, alpha, beta, maximizing)

                if next_move[0] < best[0]:
                    best = (next_move[0], move)
                beta = min(beta, best[0])
                if beta <= alpha:
                    break 

        return best
    
    def evaluate(self, board: Board):
        return board.player_score(AI_PLAYER) - board.player_score(HUMAN_PLAYER)
