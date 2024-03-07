from core.box import Box
import copy

class Board: 
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.boxes = [[Box(i, j) for j in range(rows)] for i in range(cols)]
        
        self.possible_moves  = self.calc_possible_moves(self.rows, self.cols)
        self.performed_moves = set()
        self.scores = {}
        
    def allowed_moves(self):
        return copy.deepcopy(self.possible_moves)
    
    def player_score(self, player): 
        return self.scores.get(player, 0)
        
    def calc_possible_moves(self, rows, cols):
        moves = []
        
        for col in range(0, cols+1):
            for row in range(0, rows):
                moves.append(((row, col), (row + 1, col)))
                if col < cols:
                    moves.append(((row, col), (row, col + 1)))
            if col < cols:
                moves.append(((rows, col), (rows, col + 1)))
        
        return moves
    
    def move(self, coordinates, player): 
        if coordinates in self.possible_moves: 
            self.possible_moves.remove(coordinates)
            self.performed_moves.add(coordinates)
            self.connect(coordinates, player)
            return True

        return False
    
    def connect(self, coordinates, player): 
        for i in range(self.rows):
            for j in range(self.cols): 
                if coordinates in self.boxes[i][j].lines(): 
                    self.boxes[i][j].connect(coordinates, player)
                    if self.boxes[i][j].complete():
                        self.scores[player] = self.scores.get(player, 0) + 1
    