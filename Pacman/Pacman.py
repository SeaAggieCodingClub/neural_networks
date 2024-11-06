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
        
def move(self, grid):
        target = self.pos
        
        # Check if there is a wall 1 tile ahead of pacman
        copy_self = copy.deepcopy(self) # Make a copy
        copy_self.move(0.6) # Move the copy 1 tile forward
        pos = copy_self.pos.tile() # Store the tile pos
        self.check_warp_tunnels(warp_tunnels)
        # if target_x < warp_tunnels['right']:
        #     self.pos.x = warp_tunnels['left']
        #     return
            
        # elif target_x > warp_tunnels['left']:
        #     self.pos.x = warp_tunnels['right']
        #     return
            
        if grid[pos.x, pos.y] == 'wall': # Check if pos is a wall   
            self.pos = self.pos.tile()
        else:
            match self.dir:
                case 'w':
                    target.y -= self.speed
                case 'a':
                    target.x += self.speed
                case 's':
                    target.y += self.speed
                case 'd':
                    target.x -= self.speed
            
            self.pos = target