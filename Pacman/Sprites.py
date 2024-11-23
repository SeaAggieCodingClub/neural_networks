import pygame
import numpy as np

TILE_WIDTH = 30
TILE_HEIGHT = 30

class Spritesheet(object):
    def __init__(self):
        # Get the sprites sheet
        self.sheet = pygame.image.load("Pacman/images/sprites_sheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        
        # Get the size of the sprite on the sheet
        width = int(self.sheet.get_width() / 16 * TILE_WIDTH)
        height = int(self.sheet.get_height() / 16 * TILE_HEIGHT)
        
        # Scale the image
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def get_image(self, loc, width, height):
        '''
        Returns 
        '''
        x, y = loc
        x *= TILE_WIDTH
        y *= TILE_HEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()       
    
    def getStartImage(self):
        return self.get_image(8, 0)
    
    def get_image(self, x, y):
        return Spritesheet.get_image(self, x, y, 2*TILE_WIDTH, 2*TILE_HEIGHT)

class GhostSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
        # self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        # self.entity = entity
        # self.entity.image = self.get_start_image()
        
    # def get_start_image(self):
    #     return self.get_image(self.x[self.entity.name], 4)

    def get_image(self, loc):
        return Spritesheet.get_image(self, loc, TILE_WIDTH, TILE_HEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self):
        Spritesheet.__init__(self)
    
    # def getStartImage(self):
    #     return self.getImage(16, 8)
    
    def get_image(self, loc):
        return Spritesheet.get_image(self, loc, TILE_WIDTH, TILE_HEIGHT)

class Entity(object):
    def __init__(self, node):
        self.image = None
    
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                screen.blit(self.image, self.position.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)


