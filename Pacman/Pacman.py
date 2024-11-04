from Character import *
from Position import *

warp_tunnels = {
    'right':0,
    'left':27
}

class Pacman(Character):
    def __init__(self, speed):
        self.speed = speed
def move(self, grid):
        target_y = self.pos.y
        target_x = self.pos.x
        match self.dir:
            case 'w':
                target_y -= self.speed
            case 'a':
                target_x += self.speed
            case 's':
                target_y += self.speed
            case 'd':
                target_x -= self.speed
        if target_x < warp_tunnels['right']:
            self.pos.x = warp_tunnels['left']
            return
             
        elif target_x > warp_tunnels['left']:
            self.pos.x = warp_tunnels['right']
            return
            
        elif grid[round(target_x),round(target_y)] == 'wall':    
            pass
        else:
            self.pos.y = target_y
            self.pos.x = target_x