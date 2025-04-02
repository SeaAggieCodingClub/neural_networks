from Position import *
from Character import *
from Sprites import *
from Score import Score
import copy
import random
import math

decision_tiles = { # Tiles in which there is an intersection (X val : [Y vals])
    1:[5],
    3:[26],
    6:[1, 5, 8, 14, 20, 23],
    9:[5, 14, 17, 20, 23],
    12:[5, 11, 23, 29],
    15:[5, 11, 23, 29],
    18:[5, 14, 17, 20, 23],
    21:[1, 5, 8, 14, 20, 23],
    24:[26],
    26:[5]
}

special_tiles = { # Decision tiles where there is an extra movement restriction
    12:[11, 23],
    15:[11, 23]
}

starting_positions = { # Positions where each ghost starts
    # In the house:
    #   r
    # b p o
    
    'r':Position(13.50, 11),
    'p':Position(13.50, 14),
    'b':Position(15.33, 14),
    'o':Position(11.67, 14)
}

starting_directions = { # directions where each ghost starts
    'r':'a',
    'p':'s',
    'b':'w',
    'o':'w'
}

scatter_targets = { # Targets for each ghost in scatter mode
    'r':Position(0, 0),
    'p':Position(27, 0),
    'b':Position(0, 29),
    'o':Position(27, 29)
}

consec_points = [ # The points received after each ghost eaten in sequence
    0,
    200,
    400,
    800,
    1600,
    0,
    0,
    0,
    0
]

class Ghost(Character):
    target = None
    scatter_target = None
    was_on_decision_tile = False # For make sure decisions only happen once
    consec_eaten = 0 # Counting scores for multiple ghosts eaten in a row
    override_frightened = False # When returning to the house and being revived
    
    # Sprites
    sprites = None
    image = None
    image_index = 0
    flash = 0 # White scared
    scared_seconds = 0 # Timer
    
    # For pink
    blush_timer = 0
    is_scared = False
    
    # For red
    in_chase = False
    
    def __init__(self, id, speed):
        self.id = id
        self.pos = copy.deepcopy(starting_positions[id])
        self.dir = starting_directions[id]
        self.speed = self.base_speed = speed
        
        self.image_index = 0
        self.sprites = { # Contains pygame images of each type
            "move":{},
            "eyes":{},
            "blue":{}
        }
        
        Ghost.scared_seconds = 0
        self.target = Position(0, 0)
        self.scatter_target = scatter_targets[id]
        self.is_active = id == 'r' # Only start with red active
        self.override_frightened = False
        self.fill_sprites()
    
    def fill_sprites(self):
        '''
        Fill the sprites dictionary
        
        Desired Structure:
        sprites = {
            "move":{
                'w':[X, X],
                'a':[X, X],
                's':[X, X],
                'd':[X, X]
            },
            "eyes":{
                'w':X,
                'a':X,
                's':X,
                'd':X
            },
            "blue":[
                [X, X], # Not Flashing
                [X, X]  # Flashing
            ]
        }
        '''
        
        sprites = GhostSprites()
        for dir in ['w', 'a', 's', 'd']:
            # Add moving sprites to dictionary
            self.sprites["move"][dir] = []
            for index in range(2): # Only 2 animation types
                img = sprites.get_image("move", id=self.id, dir=dir, index=index)
                self.sprites["move"][dir].append(img)
            
            # Add eyes sprites to dictionary
            img = sprites.get_image("eyes", dir=dir)
            self.sprites["eyes"][dir] = img
        
        # Add blue sprites to dictionary
        self.sprites["blue"] = []
        for flash in range(2): # Only flashing on or off (1 or 0)
            self.sprites["blue"].append([])
            for index in range(2): # Only 2 animation types
                img = sprites.get_image("blue", flash=flash, index=index)
                self.sprites["blue"][flash].append(img)
        
        # Starting image
        self.image = self.sprites["move"][self.dir][0]
    
    def change_animation(self, phase, seconds):
        '''Changes the sprite every frame'''
        
        if self.is_dead:
            image = self.sprites["eyes"][self.dir]
        elif phase == 'f' and not self.override_frightened:
            image = self.sprites["blue"][Ghost.flash][self.image_index]
        else:
            image = self.sprites["move"][self.dir][self.image_index]
        
        # Change animation index
        wiggles_per_tick = 0.2
        tol = 0.03 # Within one tick
        if seconds % wiggles_per_tick < tol:
            self.image_index = (self.image_index + 1) % 2
        
        self.image = image
        return image
    
    def is_on_decision_tile(self, decision_tiles):
        '''
        Returns whether on a decision tile
        If the current position matches a decision tile, only run once per decision tile
        '''
        
        # Check for decision tiles
        found = False
        for x, y_list in decision_tiles.items(): # For each x key in the dictionary
            if x == round(self.pos.x) and round(self.pos.y) in y_list: # If x and y values are in the list
                found = True
                if self.was_on_decision_tile: # If already marked as on this decision tile
                    to_return = False # Do not return
                else:
                    self.was_on_decision_tile = True # Mark that it is on decision tile
                    to_return = True
                break
        if not found: # If not on a decision tile   
            self.was_on_decision_tile = False
            to_return = False
        return to_return
    
    def is_on_special(self, special_tiles):
        '''Returns whether the current position is on a special tile'''
        
        return any(
            x == round(self.pos.x) and round(self.pos.y) in y_list
            for x, y_list in special_tiles.items()
        )
    
    def is_in_house(self):
        '''
        Returns whether the ghost is in the house at the center of the board.
        Boundaries of the house:
        x: 10-17
        y: 12-16
        '''
        
        pos = self.pos.tile()
        return 10 <= pos.x <= 17 and 13 <= pos.y <= 16
    
    def is_at_entrance(self):
        '''Returns whether the ghost is at the entrance to the house'''
        
        pos = self.pos.tile()
        return 13 <= pos.x <= 14 and 11 <= pos.y <= 12
    
    def target_distance(self, pos):
        '''Returns the distance from the specified position to the target'''
        
        return math.sqrt((self.target.x - pos.x) ** 2 + (self.target.y - pos.y) ** 2)
    
    def get_choices(self, grid, special):
        '''Returns (as Position, direction) the possible tile choices that neighbor the decision tile specified'''
        
        choices = []
        pos = self.pos.tile()
        
        # Lists 
        directions = ['w', 'a', 's', 'd']
        positions = [ # The positions of the 4 adjoining tiles in the current tile
            Position(pos.x, pos.y - 1), 
            Position(pos.x + 1, pos.y), 
            Position(pos.x, pos.y + 1), 
            Position(pos.x - 1, pos.y)
        ]
        
        # Find the direction opposite of ghost direction to note the invalid choice
        match self.dir:
            case 'w':
                invalid_dir = 's'
            case 'a':
                invalid_dir = 'd'
            case 's':
                invalid_dir = 'w'
            case 'd':
                invalid_dir = 'a'
        
        # For each adjoint tile in the cardinal directions
        if not (0 <= pos.x <= 27 and 0 <= pos.y <= 30): # Check if grid indices are in range: # If grid indices are out of range
            return choices # Return as empty list
        for index, position in enumerate(positions):
            # if 0 <= position.x <= 27 and 0 <= position.y <= 30: # Check if grid indices are in range
            if (grid[position.x, position.y] != 'wall' # If the tile is available
                and directions[index] != invalid_dir # If the position is not on the square the ghost just came from
                and not (special and directions[index] == 'w')): # If the choice is to move w on a special tile, do not add
                choices += [(position, directions[index])] # Add the position and direction to the list of choices, store as tuple
                #print([(position.x, position.y), directions[index]])
        return choices
    
    def get_turn(self, grid, phase, special):
        '''
        Returns the optimal direction to turn while on a decision tile.
        Returns as: [([x, y], 'a')]
        '''
        
        choices = self.get_choices(grid, special) # Get the list of choices containing tile positions and directions from the decision tile
        
        if len(choices) == 1:
            return choices[0][1] # Return the direction of the first choice
        
        if ((phase == 'f' and not self.in_chase) or self.is_scared) and not self.is_dead: # If in frightened mode
            return choices[random.randint(0, len(choices) - 1)][1] # Return a random direction
        
        # Find the choice with the minimum distance to the target
        min = [1000, 'w'] # Set min to some arbitrarily large value and arbitrary direction
        for choice in choices: # For each choice
            distance = self.target_distance(choice[0])
            if distance < min[0]: # If distance is less than min value
                min = [distance, choice[1]] # Set to min
        
        return min[1] # Return the direction
    
    def turn(self, direction):
        '''Changes the direction of the ghost, but never turns completely around'''
        
        if self.dir != direction:
            self.pos = self.pos.tile() # Center the position
        self.dir = direction
    
    def turn_around(self):
        '''Switches the ghost to face the opposite direction during a phase switch'''
        
        # Find the direction opposite of ghost direction
        match self.dir:
            case 'w':
                self.dir = 's'
            case 'a':
                self.dir = 'd'
            case 's':
                self.dir = 'w'
            case 'd':
                self.dir = 'a' 
    
    def exit(self):
        '''Begin sequence to exit the house'''
        
        # Blue turns right, orange turns left
        self.is_active = True
        if self.id == 'b': 
            self.dir = 'd'
        elif self.id == 'o':
            self.dir = 'a'
    
    def kill(self):
        '''Sets attributes to return to the house after death'''
        
        # Die and turn into eyes
        self.is_dead = True
        self.image = None
        self.target = Position(13.5, 14)
    
    def revive(self, phase):
        '''When ghost reaches the house, reset back to normal'''
        
        self.is_dead = False
        self.move(1) # Move a bit further into the house for effect
        self.turn('w')
        self.override_frightened = phase == 'f'

def scared_time(level):
    '''Returns the amount of time the ghosts are scared based on each level'''
    
    scared_time = [0, 6, 5, 4, 3, 2, 5, 2, 2, 1, 5, 2, 1, 1, 3, 1, 1, 0, 1, 0, 0, 0,]
    return 0 if level > 21 else scared_time[level]

def set_red_target(red, pacman):
    '''Sets the target for the red ghost'''
    
    red.target = pacman.pos.tile() # Just pacman's tile position

def set_pink_target(pink, pacman):
    '''Sets the target for the pink ghost'''
    
    pink.target = pacman.movep(4, pacman.dir).tile() # 4 tiles in the direction pacman is facing

def set_blue_target(blue, red, pacman):
    '''Sets the target for the blue ghost'''
    
    # Tile positions
    pos_pacman = pacman.pos.tile()
    pos_red = red.pos.tile()
    
    # Change in position from red to pacman
    delta_x = pos_pacman.x - pos_red.x
    delta_y = pos_pacman.y - pos_red.y
    
    vector = Position(pos_red.x + delta_x * 2, pos_red.y + delta_y * 2) # Double the vector and add to red's position
    blue.target = vector # The final position of the vector

def set_orange_target(orange, pacman):
    '''Sets the target for the orange ghost'''
    
    orange.target = pacman.pos
    distance = orange.target_distance(orange.pos) # Get orange's distance to pacman
    orange.target = pacman.pos.tile() if distance > 8 else orange.scatter_target

def set_targets(id, ghosts, pacman):
    '''Sets the target for each individual ghost based on their personality'''
    
    match id:
        case 'r': # Red
            set_red_target(ghosts[0], pacman)
        case 'p': # Pink
            set_pink_target(ghosts[1], pacman)
        case 'b': # Blue
            set_blue_target(ghosts[2], ghosts[0], pacman)
        case 'o': # Orange
            set_orange_target(ghosts[3], pacman)

def update_phase_attributes(ghosts, phase, prev_phase):
    '''Updates speeds and directions based on the current phase'''
    
    # Turn ghosts around if changing out of chase or scatter
    if prev_phase in ['c', 's']:
        for ghost in ghosts:
            ghost.turn_around()
    
    # Change speeds based on phase
    match phase:
        case 'c': # Chase
            for ghost in ghosts:
                ghost.speed = ghost.base_speed
        case 's': # Scatter
            for ghost in ghosts:
                ghost.speed = ghost.base_speed
        case 'f': # Frightened
            for ghost in ghosts:
                ghost.speed = ghost.base_speed * 0.70

def update_personalities(ghosts, pacman, fps, pellets):
    '''Updates attributes for each ghosts personality'''
    
    # RED (Cruise Elroy)
    red = ghosts[0]
    if pellets <= 100:
        red.speed = red.base_speed * 1.05 # Increase speed by 5%
        red.in_chase = True # Turn into Cruise Elroy
    if pellets <= 30:
        red.speed = red.base_speed * 1.10 # Increase speed by 10%
    
    # PINK (Gets shy around pacman)
    pink = ghosts[1]
    if pink.blush_timer > 0:
        pink.blush_timer -= 1 # Decrement the timer by 1
    else: # When timer runs out
        pink.is_scared = False # No longer scared
        if pink.pos.distance(pacman.pos) < 2: # If pink is within 2 tiles of pacman
            pink.blush_timer = fps # Pacman is "looking at her", set a blush timer for 1 second
            pink.is_scared = True # Pink is scared

def try_exit(ghosts, level, seconds, pellets):
    '''Check for the conditions for each ghost to leave the house'''
    
    pink = ghosts[1]
    blue = ghosts[2]
    orange = ghosts[3]
    
    # If the ghost satisfies its exit condition
    if not pink.is_active and level > 2 or int(seconds) == 8:
        pink.exit()
    elif (
        not blue.is_active
        and pink.is_active
        and not pink.is_in_house()
        and not pink.is_at_entrance()
        and (level > 2 or pellets <= 200)
    ):
        blue.exit()
    elif (
        not orange.is_active
        and blue.is_active
        and not blue.is_in_house()
        and not blue.is_at_entrance()
        and (level > 2 or pellets <= 160)
    ):
        orange.exit()

def move_exit_house(ghost):
    '''Moves the ghost out of the starting house'''
    
    if 13.4 < ghost.pos.x < 13.6: # If the ghost reaches the x position of the exit gate
        ghost.dir = 'w' # Turn upward
        ghost.pos.x = 13.5 # Center
    ghost.move(ghost.speed / 2)

def move_return_to_house(ghost, grid, phase):   
    '''Moves the ghost back to the starting house (After death)'''
        
    if ghost.is_at_entrance():
        # Move ghost into house
        ghost.pos.x = 13.5 # Move center to the entrance
        ghost.dir = 's' # Turn downward
    else:
        # Check if there is a wall 1 tile ahead of the ghost
        pos = ghost.movep(0.5, ghost.dir).tile() # Store the tile pos
        
        if 0 <= pos.x <= 27: # Check if grid indices are in range
            if grid[pos.x, pos.y] == 'wall' or ghost.is_on_decision_tile(decision_tiles): # Check if pos is a wall or decision tile
                # Turn the ghost
                dir = ghost.get_turn(grid, phase, False)
                ghost.turn(dir)
        else: # Ghost is in warp tunnel
            # Turn around
            ghost.turn_around()
    ghost.move(.3) # Move at higher speed

def move_normal(ghosts, ghost, pacman, grid, phase):
    '''Run normal updates: decision tile check, wall check, movement'''
    
    # Update for decision tiles
    special = ghost.id != 'r' and ghost.is_on_special(special_tiles)
    if ghost.is_on_decision_tile(decision_tiles): # If not in frightened mode, and on a decision tile
        # Update the target tile
        if phase == 's' and not ghost.in_chase: # If the phase is on scatter mode, and red is not in chase mode
            ghost.target = ghost.scatter_target # Set the target to its respective corner
        else: # If on chase, set the respective target
            set_targets(ghost.id, ghosts, pacman) # Update the target
        
        # Turn to the chosen direction
        dir = ghost.get_turn(grid, phase, special)
        ghost.turn(dir)
    else: # Update for wall
        # Check for position in warp tunnels, then check for walls
        ghost.check_warp_tunnels()
        if ghost.check_wall(ghost.dir, grid): # Check for a wall ahead
            dir = ghost.get_turn(grid, phase, special)
            ghost.turn(dir)
    
    # Move according to its speed and direction
    ghost.move(ghost.speed)

def update_ghosts(game): 
    '''Updates everything about the ghosts' data for every frame'''
    # Unpack game variables
    ghosts = game.ghosts
    pacman = game.pacman
    level = game.level
    grid = game.grid
    phase = game.phase
    fps = game.fps
    seconds = game.seconds
    pellets = game.pellets
    
    # Specifics for each ghost
    update_personalities(ghosts, pacman, fps, pellets)
    ghost_killed = None # If a ghost has been killed
    for ghost in ghosts:
        # Check for death
        pos = ghost.pos.tile()
        if (pos.equals(pacman.pos.tile()) or pos.equals(pacman.movep(0.5, pacman.dir).tile())) and not ghost.is_dead: # If pacman is on or near the ghost
            if phase == 'f' and not ghost.override_frightened: # If in frightened mode
                # Kill the ghost
                ghost.kill()
                ghost_killed = ghost.id
                Ghost.consec_eaten += 1
                pacman.score += consec_points[Ghost.consec_eaten] # Add to score
                Score("Ghost", ghost.pos.tile(), Ghost.consec_eaten - 1) # Display score
            else:
                # Kill pacman and move on to next life
                pacman.kill(game.do_render)
                return
        if ghost.is_active: 
            if ghost.is_in_house(): # If the ghost is waiting to exit the house
                if ghost.is_dead:
                    ghost.revive(phase)
                move_exit_house(ghost)
            elif ghost.is_dead: # If the ghost has died, return to house
                move_return_to_house(ghost, grid, phase)
            else: # Normal movement
                if ghost.is_at_entrance(): # Ghost just came out of the house
                    ghost.target = Position(14, 11) # ghost.dir = 'a'
                move_normal(ghosts, ghost, pacman, grid, phase)
        else: # Ghost is still bobbling inside the house
            ghost.move(ghost.base_speed * 0.6)
            pos = ghost.movep(1, ghost.dir).tile() # Store the tile pos
            if 0 <= pos.x <= 27 and grid[pos.x, pos.y] == 'wall': # Check if pos is a wall
                ghost.turn_around()
            try_exit(ghosts, level, seconds, pellets) # Check for the exit condition
    
    # Pack game variables
    game.phase = phase
    game.fps = fps
    game.seconds = seconds
    game.pellets = pellets
    
    return ghost_killed