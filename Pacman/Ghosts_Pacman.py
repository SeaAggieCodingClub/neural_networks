from Position import *
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
    'left':29
}

# Positions where each ghost starts
starting_positions = {
    # 'r':Position(13.50, 12),
    # 'p':Position(12.25, 14),
    # 'b':Position(13.50, 14),
    # 'o':Position(14.75, 14)
    'r':Position(1, 1),
    'p':Position(10, 1),
    'b':Position(16, 1),
    'o':Position(26, 1)
}

# directions where each ghost starts
starting_directions = {
    'r':'a',
    'p':'a',
    'b':'w',
    'o':'d'
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

class Ghost:
    pos = None
    dir = None
    speed = .1 # Tiles per frame
    id = None
    target = None
    scatter_target = None
    is_in_house = True
    was_on_decision_tile = False
    
    def __init__(self, id):
        self.id = id
        self.pos = starting_positions[id]
        self.dir = starting_directions[id]
        self.target = Position(0, 0)
        self.scatter_target = scatter_targets[id]
    
    def turn(self, direction): # Should not turn completely around
        if self.dir != direction:
            self.pos = self.pos.tile() # Center the position
        self.dir = direction
    
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
    
    def set_target(self, x, y):
        self.target.x = x
        self.target.y = y
        
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
        if pos.x < 0 or pos.x > 27: # If grid indices are out of range
            return choices # Return as empty list
        for index, position in enumerate(positions):
            if (grid[position.x, position.y + 4] != 'wall' # If the tile is available
                and directions[index] != invalid_dir # If the position is not on the square the ghost just came from
                and not (directions[index] == 'w' and special)): # If the choice is to move w on a special tile, do not add
                choices += [(position, directions[index])] # Add the position and direction to the list of choices, store as tuple
                #print([(position.x, position.y), directions[index]])
        return choices
    
    # Gets the optimal direction to turn while on a decision tile
    def get_turn(self, grid, phase, special): #   [([], 'a')]
        choices = self.get_choices(grid, special) # Get the list of choices containing tile positions and directions from the decision tile
        
        if len(choices) == 1:
            return choices[0][1] # Return the direction of the first choice
        
        if phase == 'f': # If in frightened mode
            return choices[random.randint(0, 1)][1] # Return a random direction
        
        # Find the choice with the minimum distance to the target
        min = [1000, 'w'] # Set min to some arbitrarily large value and arbitrary direction
        for choice in choices: # For each choice
            #print("CH:",choice[0])
            distance = self.target_distance(choice[0])
            if distance < min[0]: # If distance is less than min value
                min = [distance, choice[1]] # Set to min
        
        return min[1] # Return the direction

# Adds a given magnitude to the position of the character depending on the direction. Character may be a ghost or pacman 
def move(character, speed):
    match character.dir:
        case 'w':
            character.pos.y -= speed
        case 'a':
            character.pos.x += speed
        case 's':
            character.pos.y += speed
        case 'd':
            character.pos.x -= speed

# Sets the target for each individual ghost based on their personality
def set_red_target(red, pacman):
    red.target = pacman.pos.tile() # Just pacman's tile position

def set_pink_target(pink, pacman):
    # Make a copy of pacman and set 4 tiles ahead
    copy_pacman = copy.deepcopy(pacman)
    move(copy_pacman, 4) # 4 tiles in the direction pacman is facing
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
def set_target(id, ghosts, pacman, phase):    
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
                ghost.speed = 0.1
        case 's': # Scatter
            for ghost in ghosts:
                ghost.speed = 0.1
        case 'f': # Frightened
            for ghost in ghosts:
                ghost.speed -= 0.05

# Updates everything about the ghosts' data
def update_ghosts(ghosts, pacman, grid, decision_tiles, phase):    
    # Run updates: decision tile check, wall check, movement
    for ghost in ghosts:
        # Update for decision tiles
        special = ghost.is_on_special(special_tiles)
        if ghost.is_on_decision_tile(decision_tiles): # If not in frightened mode, and on a decision tile
            # Update the target tile           
            if phase == 's': # If the phase is on scatter mode
                ghost.target = ghost.scatter_target # Set the target to its respective corner
            else: # If on chase, set the respective target
                set_target(ghost.id, ghosts, pacman, phase) # Update the target
            
            # Turn to the chosen direction
            dir = ghost.get_turn(grid, phase, special)
            ghost.turn(dir)
        
        
        # Check if there is a wall 1 tile ahead of the ghost
        copy_ghost = copy.deepcopy(ghost) # Make a copy
        move(copy_ghost, 0.5) # Move the copy 1 tile forward
        pos = copy_ghost.pos.tile() # Store the tile pos
        #if (pos.x, i for i in len(grid)) in grid:
        #print("POS: ", pos.x, pos.y, copy_ghost.dir)
        #print("TILE?: ", grid[pos.x, pos.y + 4])
            #continue
        if pos.x < warp_tunnels['right']: # If grid indices are out of range to the right
            ghost.pos.x = warp_tunnels['left'] # Teleport to other side
        elif pos.x > warp_tunnels['left']:  # If grid indices are out of range to the left
            ghost.pos.x = warp_tunnels['right'] # Teleport to other side
        elif pos.x >= 0 and pos.x <= 27 and grid[pos.x, pos.y + 4] == 'wall': # Check if grid indices are in range, and pos is a wall
            # Turn the ghost
            dir = ghost.get_turn(grid, phase, special)
            ghost.turn(dir)
        
        # Move according to its speed and direction
        move(ghost, ghost.speed)