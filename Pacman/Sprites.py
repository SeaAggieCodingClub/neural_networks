import pygame
import numpy as np

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

TILEWIDTH = 18
TILEHEIGHT = 18

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("sprites_sheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()       
    
    def getStartImage(self):
        return self.getImage(8, 0)
    
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

# class GhostSprites(Spritesheet):
#     def __init__(self, entity):
#         Spritesheet.__init__(self)
#         self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
#         self.entity = entity
#         self.entity.image = self.getStartImage()
        
#     def getStartImage(self):
#         return self.getImage(self.x[self.entity.name], 4)

#     def getImage(self, x, y):
#         return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
    
    def getStartImage(self):
        return self.getImage(16, 8)
    
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class Entity(object):
    def __init__(self, node):
        ...
        self.image = None
    
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                screen.blit(self.image, self.position.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)


