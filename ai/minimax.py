from core.board import Board
from core.constants import *
from math import inf
import copy

class MiniMax: 
    def minimax(self, board: Board, depth: int, max_min: bool):
        best = (-inf, None) if max_min else (inf, None)
        
        allowed_moves = board.allowed_moves()
        if depth == 0 or len(allowed_moves) == 0: 
            return (self.evaluate(board), None)
        
        for move in allowed_moves: 
            board_copy = copy.deepcopy(board)
            board_copy.move(move)
            
            # player filled a box => gets another move 
            if board_copy.player_turn() == board.player_turn():
                next_move = self.minimax(board_copy, depth - 1, max_min)
            else: 
                next_move = self.minimax(board_copy, depth - 1, not max_min)
            
            if (max_min and next_move[0] > best[0]) \
                or (not max_min and next_move[0] < best[0]):
                best = (next_move[0], move)
                
        return best        
    
    def evaluate(self, board: Board):
        return board.player_score(AI_PLAYER) - board.player_score(HUMAN_PLAYER)         