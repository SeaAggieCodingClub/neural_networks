from Position import *
import copy
import pygame
# Tunnels on either side for the characters to traverse, x pos
warp_tunnels = {
    'right':-1,
    'left':28
}

# Parent class over Pacman and Ghosts
class Character(pygame.sprite.Sprite):
    images = None
    id = None
    pos = None
    dir = None
    speed = None
    base_speed = None
    is_active = True
    is_dead = False
    
    # Adds a given magnitude to the position of the character depending on the direction
    def move(self, speed):
        match self.dir:
            case 'w':
                self.pos.y -= speed
            case 'a':
                self.pos.x += speed
            case 's':
                self.pos.y += speed
            case 'd':
                self.pos.x -= speed
    
    # "Move Predict" Returns a predicted position if the character moved
    def movep(self, speed, dir):
        x = self.pos.x
        y = self.pos.y
        
        match dir:
            case 'w':
                y -= speed
            case 'a':
                x += speed
            case 's':
                y += speed
            case 'd':
                x -= speed
        return Position(x, y)
    
    def check_warp_tunnels(self):
        pos = self.pos
        if pos.x < warp_tunnels['right']: # If grid indices are out of range to the right
                self.pos.x = warp_tunnels['left'] # Teleport to other side
        elif pos.x > warp_tunnels['left']:  # If grid indices are out of range to the left
            self.pos.x = warp_tunnels['right'] # Teleport to other side`
    
    # Returns True if there is a wall ahead of the character
    def check_wall(self, dir, grid):
        copy_self = copy.deepcopy(self) # Make a copy
        copy_self.dir = dir
        copy_self.move(0.6) # Move the copy 1 tile forward
        pos = copy_self.pos.tile() # Store the tile pos
        
        if 0 <= pos.x <= 27: # Check if grid indices are in range
            if grid[pos.x, pos.y] == 'wall': # Check if pos is a wall
                return True
        return False

