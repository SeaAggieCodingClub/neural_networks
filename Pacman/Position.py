import math

class Position:
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def tile(self):
        '''Converts the floating position to the coordinates of the center of the tile'''
        
        x = round(self.x)
        y = round(self.y)
        return Position(x, y)
    
    def add(self, pos):
        '''Adds this position with another given position'''
        
        x = self.pos.x + pos.x
        y = self.pos.x + pos.x
        return Position(x, y)
    
    def distance(self, pos):
        '''Returns the pythagorean distance to the given position'''
        
        return math.sqrt((self.x - pos.x) ** 2 + (self.y - pos.y) ** 2)
    
    def equals(self, pos):
        '''Returns whether this position equals the given position'''
        
        return self.x == pos.x and self.y == pos.y
    
    def to_tuple(self):
        return (self.x, self.y)
    
    def to_string(self):
        '''Prints the position as x, y values'''
        
        return f"{self.x}, {self.y}"