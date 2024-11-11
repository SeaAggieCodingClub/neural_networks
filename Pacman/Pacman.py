from Character import *
from Position import *
import copy

class Pacman(Character):
    lives = 3
    pause = False # Each dot Pac-Man eats causes him to stop moving for one frame or 1/60th of a second
    
    def __init__(self, speed):
        self.speed = self.base_speed = speed
        self.pos = Position(13.5, 23)
        self.dir = 'a'
    
    def kill(self):
        self.is_dead = True
        self.lives -= 1
    
    def reset_position(self):
        self.pos = Position(13.5, 23)
        
def update_pacman(pacman, grid):
    pacman.check_warp_tunnels()
    if pacman.pause:
        pacman.pause = False
    elif pacman.check_wall(pacman.dir, grid): # Check if pos is a wall   
        pacman.pos = pacman.pos.tile() # Center the position
    else:
        pacman.move(pacman.speed)