from core.constants import *
from core.box import Box
import copy

class Board:
    def __init__(self, rows: int, cols: int, human_starts: bool) -> None:
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(i, j) for j in range(rows)] for i in range(cols)]
        
        self.human_player = human_starts
        self.scoredPoints = False
        
        self.possible_moves  = self.calc_possible_moves(self.rows, self.cols)
        self.performed_moves = set()
        self.scores = {}
       
    def all_boxes(self):
        return [copy.deepcopy(box) for row in self.boxes for box in row]
        
    def completed_boxes(self): 
        return [copy.deepcopy(box) for row in self.boxes for box in row if box.is_complete()]
    
    def is_gameover(self):
        return len(self.possible_moves) == 0
        
    def allowed_moves(self):
        return copy.deepcopy(self.possible_moves)
    
    def player_score(self, player): 
        return self.scores.get(player, 0)
    
    def player_turn(self): 
        return HUMAN_PLAYER if self.human_player else AI_PLAYER
        
    def calc_possible_moves(self, rows, cols):
        moves = []
        
        for row in range(0, rows):
            for col in range(0, cols):
                if row + 1 < rows:
                    moves.append(((row, col), (row + 1, col)))
                if col + 1 < cols:
                    moves.append(((row, col), (row, col + 1)))
        
        return list(sorted(moves))
    
    def move(self, coordinates): 
        if coordinates in self.possible_moves: 
            self.possible_moves.remove(coordinates)
            self.performed_moves.add(coordinates)
            self.connect(coordinates, HUMAN_PLAYER if self.human_player else AI_PLAYER)
            self.human_player = (not self.human_player) if not self.scoredPoints else self.human_player
            self.scoredPoints = False
            return True

        return False
    
    def connect(self, coordinates, player):
        self.scoredPoints = False
        for i in range(self.rows):
            for j in range(self.cols): 
                if coordinates in self.boxes[i][j].all_lines(): 
                    self.boxes[i][j].connect(coordinates, player)
                    if self.boxes[i][j].is_complete():
                        self.scores[player] = self.scores.get(player, 0) + 1
                        self.scoredPoints = True