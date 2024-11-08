import math

class Position:
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Converts the floating position to the coordinates of the center of the tile 
    def tile(self):
        x = round(self.x)
        y = round(self.y)
        return Position(x, y)
    
    # Adds this position with another given position
    def add(self, pos):
        x = self.pos.x + pos.x
        y = self.pos.x + pos.x
        return Position(x, y)
    
    def distance(self, pos):
        return math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2 )
    
    def equals(self, pos):
        return self.x == pos.x and self.y == pos.y
    
    def to_string(self):
        return f"{self.x}, {self.y}"