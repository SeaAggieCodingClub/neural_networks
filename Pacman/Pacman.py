from Character import *
from Position import *
import copy

class Pacman(Character):
    lives = 3
    
    def __init__(self, speed):
        self.speed = speed
        self.pos = Position(13.5, 23)
        self.dir = 'a'
    
    def kill(self):
        self.is_dead = True
        self.lives -= 1
        
def update_pacman(pacman, grid):
    pacman.check_warp_tunnels()
    if pacman.check_wall(pacman.dir, grid): # Check if pos is a wall   
        pacman.pos = pacman.pos.tile() # Center the position
    else:
        pacman.move(pacman.speed)