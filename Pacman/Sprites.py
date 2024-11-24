import pygame
import numpy as np

# Size of the sprites on sprites_sheet.png
TILE_WIDTH = 30
TILE_HEIGHT = 30

# Size of the images to display on the board
IMAGE_WIDTH = 35
IMAGE_HEIGHT = 35

class Spritesheet(object):
    def __init__(self):
        # Get the sprites sheet
        self.sheet = pygame.image.load("Pacman/images/sprites_sheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        
        # Get the size of the sprite on the sheet
        width = int(self.sheet.get_width() / 16 * TILE_WIDTH)
        height = int(self.sheet.get_height() / 16 * TILE_HEIGHT)
        
        # Scale the image
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def get_image(self, loc, width, height):
        '''
        Returns a subsection of sprites_sheet.png as a single sprite
        '''
        x, y = loc
        x *= TILE_WIDTH
        y *= TILE_HEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
        img = self.sheet.subsurface(self.sheet.get_clip())
        return pygame.transform.scale(img, (width, height))

class PacmanSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
    
    def get_move_loc(self, index):
        '''Returns the location of the moving sprite on sprites_sheet.png '''
        
        match index:
            case 0:
                return (2, 0)
            case 1:
                return (1, 2)
            case 2:
                return (0, 2)
    
    def get_death_loc(self, index):
        '''Returns the location of the death sprite on sprites_sheet.png '''
        
        if index > 10:
            return None
        
        x = 3
        y = 0
        
        return (x + index, y)
    
    def get_image(self, type, index):
        '''Returns a pygame image'''
        
        # Find location on the spritesheet
        if type == "move":
            loc = self.get_move_loc(index)
        else:
            loc = self.get_death_loc(index)
        
        return Spritesheet.get_image(self, loc, IMAGE_WIDTH, IMAGE_HEIGHT)

class GhostSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
    
    def get_move_loc(self, id, dir, index=0):
        '''Returns the location of the moving sprite on sprites_sheet.png '''
        
        x = {
            'w':4,
            'a':2,
            's':6,
            'd':0
        }
        
        y = {
            'r':4,
            'p':5,
            'b':6,
            'o':7
        }
        
        return (x[dir] + index, y[id])
    
    def get_eyes_loc(self, dir):
        '''Returns the location of the eyes sprite on sprites_sheet.png '''
        
        y = 5
        
        x = {
            'w':10,
            'a':9,
            's':11,
            'd':8
        }
        
        return (x[dir], y)
    
    def get_blue_loc(self, flash, index=0):
        '''Returns the location of the blue (scared) sprite on sprites_sheet.png'''
        
        x = 10 if flash else 8
        y = 4
        
        return (x + index, y)
    
    def get_image(self, type, id=None, dir=None, index=0, flash=0):
        '''Returns a pygame image'''
        
        # Find location on the spritesheet
        if type == "move":
            loc = self.get_move_loc(id, dir, index)
        elif type == "eyes":
            loc = self.get_eyes_loc(dir)
        else:
            loc = self.get_blue_loc(flash, index)
        
        return Spritesheet.get_image(self, loc, IMAGE_WIDTH, IMAGE_HEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
    
    def get_image(self, id):
        locs = {
            'c':(2, 3),
            's':(3, 3),
            'o':(4, 3),
            'a':(5, 3),
            'm':(6, 3),
            'g':(7, 3),
            'b':(8, 3),
            'k':(9, 3)
        }
        
        '''Returns a pygame image'''
        return Spritesheet.get_image(self, locs[id], IMAGE_WIDTH, IMAGE_HEIGHT)

class ScoreSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
    
    # def get_ghost_score_loc(self, index):
    #     '''Returns the location of the ghost score sprite on sprites_sheet.png '''
        
    #     return (index, 8)
    
    # def get_fruit_score_loc(self, index):
    #     '''Returns the location of the fruit score on sprites_sheet.png '''
        
    #     x = index if index < 4 else 4
    #     y = 9 if index < 4 else index + 4
        
    #     return (x, y)
    
    def get_image(self, type, index):
        '''Returns a pygame image'''
        
        if type == "Ghost":
            loc = (index, 8)
        else:
            locs = {
                'c':(0, 9),
                's':(1, 9),
                'o':(2, 9),
                'a':(3, 9),
                'm':(4, 9),
                'g':(4, 10),
                'b':(4, 11),
                'k':(4, 13),
            }
            loc = locs[index]
        
        return Spritesheet.get_image(self, loc, IMAGE_WIDTH, IMAGE_HEIGHT)

