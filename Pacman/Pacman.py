from Character import *
from Position import *
import copy
import Sound
import pygame
class Pacman(Character):
    lives = 3
    pause = False # Each dot Pac-Man eats causes him to stop moving for one frame or 1/60th of a second
    current_sprite = "move"
    current_sprite_index = 0
    sprite_buffer = 0
    def __init__(self, speed):
        self.speed = self.base_speed = speed
        self.pos = Position(13.5, 23)
        self.dir = 'a'
    
        # Adds moving sprites to dictionary
        self.sprites["move"] = []
        for i in range (1, 4):
            temp = pygame.image.load("Pacman/images/pacman/pacman_move_" + str(i) + ".png")
            temp = pygame.transform.scale(temp, (45, 45))
            self.sprites["move"].append(temp)
           

        self.image = self.sprites["move"][0]


        #self.rect.topleft = (self.pos.x * 16, self.pos.y * 16)
        #self.image.scale((45, 45))

        
        
    def kill(self):
        self.is_dead = True
        self.lives -= 1
        Sound.play_death_sound()
    
    def reset_position(self):
        self.pos = Position(13.5, 23)
    
    def update_pacman(self, grid):
        self.check_warp_tunnels()
        if self.pause:
            self.pause = False
        elif self.check_wall(self.dir, grid): # Check if pos is a wall   
            self.pos = self.pos.tile() # Center the position
        else:
            self.move(self.speed)
            self.change_animation(self.current_sprite)
            
    def change_animation(self, current):
        if self.sprite_buffer == 2:
            self.sprite_buffer = 0
        else:
            self.sprite_buffer += 1
            return
        
        if current == "move":
            if len(self.sprites["move"]) - 1 == self.current_sprite_index:
                self.current_sprite_index = 0
            else:
                self.current_sprite_index += 1
    
    def rotate_sprite(self):
        self.image = self.sprites[self.current_sprite][self.current_sprite_index]
        if self.dir == 'w':
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.dir == 's':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.dir == 'd':
            self.image = pygame.transform.rotate(self.image, 0)
        elif self.dir == 'a':
            self.image = pygame.transform.rotate(self.image, 180)
            
    # Changes the direction of pacman from the keyboard input, if move is invalid returns the next move 
    def control_pacman(self, next_move, grid):
        # Direction controls
        # next_move = next_move_list[0] # Store as tuple for pass by reference
        pos = self.pos.tile()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or next_move == 'w':
            if self.check_wall('w', grid):
                next_move = 'w' # Set a buffer for the next move
            else:
                self.dir = 'w'
                next_move = None
                self.pos.x = pos.x
        if keys[pygame.K_a] or next_move == 'a':
            if self.check_wall('a', grid):
                next_move = 'a' # Set a buffer for the next move
            else:
                self.dir = 'a'
                next_move = None
                self.pos.y = pos.y
        if keys[pygame.K_s] or next_move == 's':
            if self.check_wall('s', grid):
                next_move = 's' # Set a buffer for the next move
            else:
                self.dir = 's'
                next_move = None
                self.pos.x = pos.x
        if keys[pygame.K_d] or next_move == 'd':
            if self.check_wall('d', grid):
                next_move = 'd' # Set a buffer for the next move
            else:
                self.dir = 'd'
                next_move = None
                self.pos.y = pos.y

        return next_move