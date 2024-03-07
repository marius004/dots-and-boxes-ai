import copy

class Box: 
    def __init__(self, x, y) -> None:
        self.coordinates = [
            (x, y),
            (x + 1, y),
            (x, y + 1),
            (x + 1, y + 1)
        ]
        self.lines = [
            (self.coordinates[0], self.coordinates[1]),
            (self.coordinates[0], self.coordinates[2]),
            (self.coordinates[1], self.coordinates[3]),
            (self.coordinates[2], self.coordinates[3])
        ]
        self.completed = [False] * len(self.lines) 
        self.owner = None
    
    def lines(self):
        return copy.deepcopy(self.lines)
    
    def complete(self): 
        return self.complete
    
    def owner(self): 
        return self.owner
        
    def connect(self, line, player):
        if line in self.lines: 
            index = self.lines.index(line)
            if not self.completed[index]: 
                self.completed[index] = True
                if all(self.completed):
                    self.owner = player
                return True
        return False