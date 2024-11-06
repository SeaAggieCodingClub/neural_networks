from Position import *
from Character import *
import copy
import random
import math
import pygame

# Tiles in which there is an intersection
decision_tiles = {
    1:[5],
    3:[26],
    6:[1, 5, 8, 14, 20, 23],
    9:[5, 14, 17, 20, 23],
    12:[5, 11, 23, 29],
    15:[5, 11, 23, 29],
    18:[5, 14, 17, 20, 23],
    21:[1, 5, 8, 14, 20, 23],
    24:[26],
    27:[5]
}

# Decision tiles where there is an extra movement restriction
special_tiles = {
    12:[11, 23],
    15:[11, 23]
}

# Tunnels on either side for the characters to traverse, x pos
warp_tunnels = {
    'right':-2,
    'left':27
}

# Positions where each ghost starts
starting_positions = {
    #  r
    # bpo
    # 
    # 'r':Position(13.50, 11),
    # 'p':Position(13.50, 14),
    # 'b':Position(14.75, 14),
    # 'o':Position(12.25, 14)
    'r':Position(1, 1),
    'p':Position(10, 1),
    'b':Position(16, 1),
    'o':Position(25, 1)
}

# directions where each ghost starts
starting_directions = {
    'r':'a',
    'p':'s',
    'b':'w',
    'o':'w'
}

# Targets for each ghost in scatter mode
scatter_targets = {
    'r':Position(0, 0),
    'p':Position(27, 0),
    'b':Position(0, 29),
    'o':Position(27, 29)
}

# Phases: Chase ('c'), Scatter ('s'), Frightened ('f')
# Ghosts: Red ('r'), Pink ('p'), Blue ('b'), Orange ('o')
# Directions: 'w', 'a', 's', 'd'

images = {
    "body":{
        'r':"Pacman/images/ghost_red.png",
        'p':"Pacman/images/ghost_pink.png",
        'b':"Pacman/images/ghost_blue.png",
        'o':"Pacman/images/ghost_orange.png"
        #"pacman":"Pacman/images/pacman.png"
    },
    "eyes":"Pacman/images/ghost_eyes.png",
    "scared":"Pacman/images/ghost_scared.png"
}

# Convert image urls to pygame objects
for k, image in images["body"].items(): # Body images
    img = pygame.image.load(image) # Load the image
    images["body"][k] = pygame.transform.scale(img, (35, 35)) # Scale the image and reference it back to the key
# for k, image in images.items(): # Other images
#     img = pygame.image.load(image) # Load the image
#     images[k] = pygame.transform.scale(img, (35, 35)) # Scale the image and reference it back to the key

class Ghost(Character):
    image_eyes = None
    target = None
    scatter_target = None
    was_on_decision_tile = False
    is_active = True
    is_dead = False
    
    # For pink
    blush_timer = 0
    is_scared = False
    
    # For red
    in_chase = False
    
    def __init__(self, id, speed, image_eyes):
        self.id = id
        self.pos = starting_positions[id]
        self.dir = starting_directions[id]
        self.speed = self.base_speed = speed
        self.image_eyes = image_eyes
        self.target = Position(0, 0)
        self.scatter_target = scatter_targets[id]
    
    # If the current position matches a decision tile, only run once per decision tile
    def is_on_decision_tile(self, decision_tiles):
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
    
    # If the current position is on a special tile
    def is_on_special(self, special_tiles):
        return any(
            x == round(self.pos.x) and round(self.pos.y) in y_list
            for x, y_list in special_tiles.items()
        )
    
    def is_in_house(self):
        # Boundaries of the house:
        # x: 10-17
        # y: 12-16
        
        pos = self.pos.tile()
        return 10 <= pos.x <= 17 and 13 <= pos.y <= 16
    
    def is_at_entrance(self):
        pos = self.pos.tile()
        return 13 <= pos.x <= 14 and 11 <= pos.y <= 12
    
    # Returns the distance from the specified position to the target
    def target_distance(self, pos):
        return math.sqrt((self.target.x - pos.x) ** 2 + (self.target.y - pos.y) ** 2)
    
    # Returns (as Position, direction) the possible tile choices that neighbor the decision tile specified
    def get_choices(self, grid, special):
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
    
    # Gets the optimal direction to turn while on a decision tile
    def get_turn(self, grid, phase, special): #   [([x, y], 'a')]
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
        #print(choices, min[1])
        
        
        return min[1] # Return the direction
    
    def turn(self, direction): # Should not turn completely around
        if self.dir != direction:
            self.pos = self.pos.tile() # Center the position
        self.dir = direction
    
    def turn_around(self):
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
    
    def start(self):
        # Begin to exit the house
        self.is_active = True
        
        # Blue turns right, orange turns left
        if self.id == 'b': 
            self.dir = 'd'
        elif self.id == 'o':
            self.dir = 'a'
    
    def kill(self):
        # Die and turn into eyes
        self.is_dead = True
        self.image = None
        self.target = Position(13.5, 14)
        # self.speed *= 10 # Tiles per second
    
    def revive(self):
        self.is_dead = False
        self.image = None # CHANGE TO NORMAL GHOST IMAGE
        self.move(1) # Move a bit further into the house for effect
        self.turn('w')
        # self.speed = self.base_speed # Return to normal speed
    
# Sets the target for each individual ghost based on their personality
def set_red_target(red, pacman):
    red.target = pacman.pos.tile() # Just pacman's tile position

def set_pink_target(pink, pacman):
    # Make a copy of pacman and set 4 tiles ahead
    copy_pacman = copy.deepcopy(pacman)
    copy_pacman.move(4) # 4 tiles in the direction pacman is facing
    pink.target = copy_pacman.pos.tile()

def set_blue_target(blue, red, pacman):
    # Tile positions
    pos_pacman = pacman.pos.tile()
    pos_red = red.pos.tile()
    
    # Change in position from red to pacman
    delta_x = pos_pacman.x - pos_red.x
    delta_y = pos_pacman.y - pos_red.y
    
    vector = Position(pos_red.x + delta_x * 2, pos_red.y + delta_y * 2) # Double the vector and add to red's position
    blue.target = vector # The final position of the vector

def set_orange_target(orange, pacman):
    orange.target = pacman.pos
    distance = orange.target_distance(orange.pos) # Get orange's distance to pacman
    orange.target = pacman.pos.tile() if distance > 8 else orange.scatter_target

# Sets the target of any ghost given its id
def set_targets(id, ghosts, pacman, phase):
    # Set individual targets for each
    match id:
        case 'r': # Red
            set_red_target(ghosts[0], pacman)
        case 'p': # Pink
            set_pink_target(ghosts[1], pacman)
        case 'b': # Blue
            set_blue_target(ghosts[2], ghosts[0], pacman)
        case 'o': # Orange
            set_orange_target(ghosts[3], pacman)

# Controlled by timer, switches 
def switch_phase(ghosts, phase, prev_phase):
    # Turn ghosts around if changing out of chase or scatter
    if prev_phase in ['c', 's']:
        for ghost in ghosts:
            ghost.turn_around()

    # CHANGE VALUES LATER
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
                ghost.speed = ghost.base_speed / 2

def update_personalities(ghosts, pacman, fps, pellets):
    # red ghost should speed up after x number of pellets gone, and permanently be in chase mode
    # RED
    red = ghosts[0]
    if pellets == 20:
        red.speed = red.base_speed * 1.05 # Increase speed by 5%
        red.in_chase = True
    elif pellets == 10:
        red.speed = red.base_speed * 1.10 # Increase speed by 10%
    
    # PINK
    pink = ghosts[1]
    if pink.blush_timer > 0:
        pink.blush_timer -= 1 # Decrement the timer by 1
    else: # When timer runs out
        pink.is_scared = False # No longer scared
        # copy_pacman = copy.deepcopy(pacman) # Make a copy
        # move(copy_pacman, pink.pos.distance(pacman.pos)) # Move the pacman copy forward the distance to pink (pacman may be facing a different direction)  
        # if pink.pos.tile().equals(copy_pacman.pos.tile()): # If the tile positions match
        if pink.pos.distance(pacman.pos) < 2: # If pink is within 2 tiles of pacman
            pink.blush_timer = fps # Pacman is "looking at her", set a blush timer for 1 second
            pink.is_scared = True # Pink is scared

# Moves the ghost out of the starting house
def move_exit_house(ghost):
    if ghost.pos.tile().x == 13.5: # If the ghost reaches the x position of the exit gate
        ghost.dir = 'w' # Turn upward
    ghost.move(ghost.speed) # Move regularly

# Moves the ghost according to its regular path
# Moves the ghost back to the starting house (After death)
def move_return_to_house(ghost, grid, phase): # UPDATE LATER         
    if ghost.is_at_entrance():
        # Move ghost into house
        ghost.pos.x = 13.5 # Move center to the entrance
        ghost.dir = 's' # Turn downward
    else:
        # Check if there is a wall 1 tile ahead of the ghost
        copy_ghost = copy.deepcopy(ghost) # Make a copy
        copy_ghost.move(0.5) # Move the copy 1 tile forward
        pos = copy_ghost.pos.tile() # Store the tile pos
        
        if 0 <= pos.x <= 27: # Check if grid indices are in range
            if grid[pos.x, pos.y] == 'wall' or ghost.is_on_decision_tile(decision_tiles): # Check if pos is a wall or decision tile
                # Turn the ghost
                dir = ghost.get_turn(grid, phase, False)
                ghost.turn(dir)
        else: # Ghost is in warp tunnel
            # Turn around
            ghost.turn_around()
    ghost.move(.5) # Move at higher speed


# Run normal updates: decision tile check, wall check, movement
def move_normal(ghosts, ghost, pacman, grid, phase):
    # Update for decision tiles
    special = ghost.is_on_special(special_tiles)
    if ghost.is_on_decision_tile(decision_tiles): # If not in frightened mode, and on a decision tile
        # Update the target tile
        if phase == 's' and not ghost.in_chase: # If the phase is on scatter mode, and red is not in chase mode
            ghost.target = ghost.scatter_target # Set the target to its respective corner
        else: # If on chase, set the respective target
            set_targets(ghost.id, ghosts, pacman, phase) # Update the target
        
        # Turn to the chosen direction
        dir = ghost.get_turn(grid, phase, special)
        ghost.turn(dir)
    else: # Update for wall
        # Check if there is a wall 1 tile ahead of the ghost
        copy_ghost = copy.deepcopy(ghost) # Make a copy
        copy_ghost.move(0.5) # Move the copy 1 tile forward
        pos = copy_ghost.pos.tile() # Store the tile pos
        
        # Check for position in warp tunnels, then check for walls
        ghost.check_warp_tunnels(warp_tunnels)
        if 0 <= pos.x <= 27: # Check if grid indices are in range
            if grid[pos.x, pos.y] == 'wall': # Check if pos is a wall
                # Turn the ghost
                dir = ghost.get_turn(grid, phase, special)
                ghost.turn(dir)
    
    # Move according to its speed and direction
    ghost.move(ghost.speed)

# Updates everything about the ghosts' data
def update_ghosts(ghosts, pacman, grid, phase, fps, seconds, phase_rotation, pellets): 
    # Specifics for each ghost
    update_personalities(ghosts, pacman, fps, pellets)
    
    for ghost in ghosts:
        # Check for death
        if ghost.pos.tile().equals(pacman.pos.tile()):# and phase == 'f': # If pacman is on the ghost and they are blue
            ghost.kill()
        
        if ghost.is_active:
            if ghost.is_in_house(): # If the ghost is waiting to exit the house
                if ghost.is_dead:
                    ghost.revive()
                move_exit_house(ghost)
            elif ghost.is_dead: # If the ghost has died, return to house
                move_return_to_house(ghost, grid, phase)
            else: # Normal movement
                move_normal(ghosts, ghost, pacman, grid, phase)