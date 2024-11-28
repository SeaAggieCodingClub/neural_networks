from Position import *
from Sprites import *
from Score import Score
from queue import Queue

ids = [ # Types of fruit
    'c', # Cherry
    's', # Strawberry
    'o', # Orange
    'a', # Apple
    'm', # Melon
    'g', # Galaxian
    'b', # Bell
    'k'  # Key
]

points = { # Points received after consumption
    'c':100,
    's':300,
    'o':500,
    'a':700,
    'm':1000,
    'g':2000,
    'b':3000,
    'k':5000
}

class Fruit:
    id = None
    pos = Position(13.50, 17)
    sprites = None
    image = None
    
    # Static
    active_seconds = 0
    active_timer = 10
    is_active = False
    q = Queue()
    
    def __init__(self, level):
        self.id = self.get_id(level)
        self.points = points[self.id]
        
        sprites = FruitSprites()
        self.image = sprites.get_image(self.id)
        
        Fruit.is_active = False
    
    def get_id(self, level):
        '''Returns the fruit id based on the current level'''
        
        if level == 1:
            return ids[0] # Cherry
        if level == 2:
            return ids[1] # Strawberry
        if level <= 12:
            return ids[(level + 1) // 2] # All the others in 2's
        return ids[-1] # Only Keys after level 18
    
    def eat(self):
        '''Despawns fruit and places in the bottom queue, then adds to the score'''
        
        self.despawn()
        q = Fruit.q
        
        q.put(self.image) # Add the fruit
        if q.qsize() > 7: # If the list is full
            q.get() # Drop the last fruit
        
        Score("Fruit", self.pos, self.id) # Display score
    
    def spawn(self):
        '''Show the fruit'''
        Fruit.is_active = True
    
    def despawn(self):
        '''Reset the fruit'''
        Fruit.is_active = False
        Fruit.active_seconds = 0
    
def update_fruit(fruit, pacman, pellets, fps, level):
    '''
    The fruit appears after 70 dots are eaten and again after 170 dots 
    are eaten unless the first fruit is still there. 
    They will disappear if they are not eaten after 9-10 seconds.
    '''
    
    if fruit is None:
        return None
    
    if Fruit.is_active:
        # Check to eat fruit
        if abs(pacman.pos.y - fruit.pos.y) < 0.5 and abs(fruit.pos.x - pacman.pos.x) < 0.5:
            fruit.eat()
        
        # Check to despawn fruit
        Fruit.active_seconds += 1 / fps # Update timer
        if Fruit.active_seconds > Fruit.active_timer:
            fruit.despawn()
    # Check to spawn fruit
    elif pellets in [70, 170]:
        fruit.spawn()
    return fruit