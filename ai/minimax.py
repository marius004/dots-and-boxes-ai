from core.board import Board
from core.constants import *
from math import inf
import copy

class MiniMax: 
    def minimax(self, board: Board, depth: int, maximizing: bool):
        best = (-inf, None) if maximizing else (inf, None)
        
        allowed_moves = board.allowed_moves()
        if depth == 0 or len(allowed_moves) == 0: 
            return (self.evaluate(board), None)
        
        for move in allowed_moves: 
            board_copy = copy.deepcopy(board)
            board_copy.move(move)
            
            # current player filled a box => gets another move 
            if board_copy.player_turn() == board.player_turn():
                next_move = self.minimax(board_copy, depth - 1, maximizing)
            else: 
                next_move = self.minimax(board_copy, depth - 1, not maximizing)
            
            if (maximizing and next_move[0] > best[0]) \
                or (not maximizing and next_move[0] < best[0]):
                best = (next_move[0], move)
                
        return best        
    
    def evaluate(self, board: Board):
        return board.player_score(AI_PLAYER) - board.player_score(HUMAN_PLAYER)         