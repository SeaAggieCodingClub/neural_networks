from Character import *
from Position import *
from Sprites import *
import Sound
import numpy as np

class Pacman(Character):
    lives = 3
    extra_lives = 0
    score = 0
    pause = False # Each dot Pac-Man eats causes him to stop moving for one frame or 1/60th of a second
    
    current_sprite = "move"
    current_sprite_index = 0
    current_sprite_buffer = 0
    sprite_buffer_max = 2
    
    def __init__(self, speed):
        self.speed = self.base_speed = self.normal_speed = speed
        self.pos = Position(13.5, 23)
        self.dir = 'a'
        self.fill_sprites()
    
    def fill_sprites(self):
        '''
        Fill the sprites dictionary
        
        Desired Structure:
        sprites = {
            "move":[X, X, X],
            "death":[X, X, ... , X]]
        }
        '''
        
        # Add moving sprites to dictionary
        sprites = PacmanSprites()
        self.sprites["move"] = []
        for index in range(3):
            img = sprites.get_image("move", index)
            self.sprites["move"].append(img)
        
        # Add death sprites to dictionary
        self.sprites["death"] = []
        for index in range(11):
            img = sprites.get_image("death", index)
            self.sprites["death"].append(img)
        
        self.image = self.sprites["move"][0]
    
    def kill(self, do_render):
        '''Decrease number of lives and activate the death animation'''
        
        self.is_dead = True
        self.lives -= 1
        
        self.current_sprite = "death"
        self.current_sprite_index = 0
        self.current_sprite_buffer = 0
        self.sprite_buffer_max = 0
        
        if do_render:
            Sound.play_death_sound()
    
    def respawn(self):
        '''Reset the position and sprites'''
        
        self.is_dead = False
        
        self.current_sprite = "move"
        self.current_sprite_index = 0
        self.current_sprite_buffer = 0
        self.sprite_buffer_max = 2
        
        self.reset_position()
        self.dir = 'a'
        
    def reset_position(self):
        self.pos = Position(13.5, 23)
    
    def update_pacman(self, grid):
        '''Moves, checks walls, checks warp tunnels, and updates animation for every frame'''
        
        self.check_warp_tunnels()
        if self.pause:
            self.pause = False
        elif self.check_wall(self.dir, grid): # Check if pos is a wall   
            self.pos = self.pos.tile() # Center the position
        else:
            self.move(self.speed)
            self.change_animation()
        
    def change_animation(self):
        '''Changes the sprite every frame'''
        
        if self.current_sprite_buffer == self.sprite_buffer_max:
            self.current_sprite_buffer = 0
        else:
            self.current_sprite_buffer += 1
            return
        
        if self.current_sprite == "move":
            if len(self.sprites["move"]) - 1 == self.current_sprite_index:
                self.current_sprite_index = 0
            else:
                self.current_sprite_index += 1
                
        elif self.current_sprite == "death":
            if len(self.sprites["death"]) - 1 == self.current_sprite_index:
                self.image = None
                return
            else:
                self.current_sprite_index += 1
                
        self.image = self.sprites[self.current_sprite][self.current_sprite_index]
    
    def rotate_sprite(self):
        '''Updates the rotation based on the direction facing, and justifies position'''
        
        curve_steps = 2 # Number of steps to take to center pacman after a turn
        pos = self.pos.tile()
        self.image = self.sprites[self.current_sprite][self.current_sprite_index]
        if self.dir == 'w':
            self.image = pygame.transform.rotate(self.image, 0)
            self.pos.x += (pos.x - self.pos.x) / curve_steps # Curve turns
        elif self.dir == 'a':
            self.image = pygame.transform.rotate(self.image, 90)
            self.pos.y += (pos.y - self.pos.y) / curve_steps # Curve turns
        elif self.dir == 's':
            self.image = pygame.transform.rotate(self.image, 180)
            self.pos.x += (pos.x - self.pos.x) / curve_steps # Curve turns
        elif self.dir == 'd':
            self.image = pygame.transform.rotate(self.image, 270)
            self.pos.y += (pos.y - self.pos.y) / curve_steps # Curve turns
    
    def get_choices(self, grid):
        '''Returns a list of valid moves, for tiles that are not walls'''
        
        choices = []
        pos = self.pos.tile()
        if not (1 <= pos.x <= 26 and 0 <= pos.y <= 30): # If grid indices are out of range
            return np.array([0, 1, 0, 1]) # Return as warp tunnel choices
        
        positions = [ # The positions of the 4 adjoining tiles in the current tile
            Position(pos.x, pos.y - 1), 
            Position(pos.x + 1, pos.y), 
            Position(pos.x, pos.y + 1), 
            Position(pos.x - 1, pos.y)
        ]
        
        for position in positions:
            choices += [0] if grid[position.x, position.y] == 'wall' else [1] # Check valid moves
        
        return np.array(choices)
    
    def has_reversed(self, action, prev_action):
        # action = self.dir
        reversed = False
        match prev_action:
            case 'w':
                reversed = action == 's'
            case 'a':
                reversed = action == 'd'
            case 's':
                reversed = action == 'w'
            case 'd':
                reversed = action == 'a'
        return reversed
    
    # def is_on_decision_tile(self, decision_tiles): # NOT USING
    #     '''
    #     Returns whether on a decision tile
    #     '''
        
    #     # Check for decision tiles
    #     pos = self.pos.tile()
    #     return any(
    #         pos.x == x and pos.y in y_list for x, y_list in decision_tiles.items()
    #     )
    
    # def dist_nearest_decision_tile(self, decision_tiles):
    #     '''
    #     Finds the closest decision tile, returns its position and distance
    #     '''
    #     min = 100
    #     for x, y_list in decision_tiles.items():
    #         for y in y_list:
    #             decision_tile_pos = Position(x, y)
    #             dist = self.pos.distance(decision_tile_pos)
    #             if dist < min:
    #                 min = dist
    #                 return decision_tile_pos, min
    #     return min(dists),  # Closest decision tile
    
    def dist_nearest_pellets(self, grid, count):
        # CHANGE TO HAMMING DISTANCE
        dists = []
        for loc, val in grid.items(): # For each value
            if val in ['dot_', 'pdot']: # If pellet
                x, y = loc
                dists += [self.pos.distance(Position(x, y))]
        return np.array(sorted(dists)[:count]) # n closest pellets
    
    def dist_nearest_ghost(self, ghosts):
        dists = [self.pos.distance(ghost.pos) for ghost in ghosts]
        return min(dists) # Closest ghost
    
    def dist_fruit(self, fruit):
        return self.pos.distance(fruit.pos) if fruit.is_active else 0 # CHANGE TO HAMMING DISTANCE
    
    def control_pacman(self, game, action=None):
        '''Changes the direction of pacman from the keyboard input, if move is invalid returns the next move'''
        # Unpack game variables
        next_move = game.next_move
        grid = game.grid
        
        # Direction controls
        pos = self.pos.tile()
        if 0 <= pos.x <= 27:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or 'w' in [action, next_move]:
                if self.check_wall('w', grid):
                    next_move = 'w' # Set a buffer for the next move
                else:
                    self.dir = 'w'
                    next_move = None
            if keys[pygame.K_a] or 'a' in [action, next_move]:
                if self.check_wall('a', grid):
                    next_move = 'a' # Set a buffer for the next move
                else:
                    self.dir = 'a'
                    next_move = None
            if keys[pygame.K_s] or 's' in [action, next_move]:
                if self.check_wall('s', grid):
                    next_move = 's' # Set a buffer for the next move
                else:
                    self.dir = 's'
                    next_move = None
            if keys[pygame.K_d] or 'd' in [action, next_move]:
                if self.check_wall('d', grid):
                    next_move = 'd' # Set a buffer for the next move
                else:
                    self.dir = 'd'
                    next_move = None
        
        game.next_move = next_move
        return next_move