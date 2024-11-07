from Character import *
from Position import *
import copy

warp_tunnels = {
    'right':0,
    'left':27
}

class Pacman(Character):
    def __init__(self, speed):
        self.speed = speed
        self.pos = Position(13.5, 23)
        
def update_pacman(pacman, grid):
    target = pacman.pos
    
    pacman.check_warp_tunnels(warp_tunnels)
    if pacman.check_wall(pacman.dir, grid): # Check if pos is a wall   
        pacman.pos = pacman.pos.tile() # Center the position
    else:
        pacman.move(pacman.speed)
        # match self.dir:
        #     case 'w':
        #         target.y -= self.speed
        #     case 'a':
        #         target.x += self.speed
        #     case 's':
        #         target.y += self.speed
        #     case 'd':
        #         target.x -= self.speed
        
        # self.pos = target