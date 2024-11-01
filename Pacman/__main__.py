import pygame
import time
import os
import random
import Ghosts_Pacman as Ghosts

pygame.init()



# Get the screen resolution
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Calculate position for the window to be centered at the top-right
window_width, window_height = 640, 480
top_right_x = screen_width - window_width - 175
top_right_y = 0

# Set environment variable for window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{top_right_x},{top_right_y}"

# Do not change this so they will be consistent between games and able to keep room for the Neural Network window
width = 800
height = 650

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption('Snake')

# Images
background = pygame.image.load("Pacman/images/background.png")
dot_ = pygame.image.load("Pacman/images/dot.png")
#wall = pygame.image.load("Pacman/images/wall.png")
images = {
    'r':"Pacman/images/ghost_red.png",
    'p':"Pacman/images/ghost_pink.png",
    'b':"Pacman/images/ghost_blue.png",
    'o':"Pacman/images/ghost_orange.png",
    "pacman":"Pacman/images/pacman.png"
}

# Convert image urls to pygame objects
for k, image in images.items():
    img = pygame.image.load(image) # Load the image
    images[k] = pygame.transform.scale(img, (35, 35)) # Scale the image and reference it back to the key

# Set clock speed
clock = pygame.time.Clock()

# Color definitions
black = (10, 10, 10)  # Changed to white color for clarity
blue = (32,36,221)

# Menu variables
outside_border = pygame.Rect(10, 15, 200, height - 30)
inside_border = pygame.Rect(15, 20, 190, height - 40)





#grid = {(x, y): 'dot_' for x in range(28) for y in range(36)}


grid = {
    (0.0, 0): '', (0, 1): '', (0, 2): '', (0.0, 3): '', (0, 4): 'wall', (0, 5): 'wall', (0.0, 6): 'wall', (0, 7): 'wall', (0.0, 8): 'wall', (0, 9): 'wall', (0.0, 10): 'wall', (0.0, 11): 'wall', (0, 12): 'wall', (0.0, 13): 'wall', (0, 14): '____', (0, 15): '____',  (0, 16): '____', (0, 17): 'wall', (0.0, 18): '____', (0.000, 19): 'wall', (0, 20): '____',  (0, 21): '____', (0, 22): '____', (0.000, 23): 'wall', (0, 24): 'wall', (0, 25): 'wall', (0, 26): 'wall', (0.000, 27): 'wall', (0, 28): 'wall', (0, 29): 'wall', (0, 30): 'wall', (0, 31): 'wall', (0.0000, 32): 'wall', (0, 33): 'wall', (0, 34): 'wall', 
    (1.0, 0): '', (1, 1): '', (1, 2): '', (1.0, 3): '', (1, 4): 'wall', (1, 5): 'dot_', (1.0, 6): 'dot_', (1, 7): 'dot_', (1.0, 8): 'dot_', (1, 9): 'dot_', (1.0, 10): 'dot_', (1.0, 11): 'dot_', (1, 12): 'dot_', (1.0, 13): 'wall', (1, 14): '____', (1, 15): '____',  (1, 16): '____', (1, 17): 'wall', (1.0, 18): '____', (1.000, 19): 'wall', (1, 20): '____',  (1, 21): '____', (1, 22): '____', (1.000, 23): 'wall', (1, 24): 'dot_', (1, 25): 'dot_', (1, 26): 'dot_', (1.000, 27): 'dot_', (1, 28): 'wall', (1, 29): 'wall', (1, 30): 'dot_', (1, 31): 'dot_', (1.0000, 32): 'dot_', (1, 33): 'dot_', (1, 34): 'wall', 
    (2.0, 0): '', (2, 1): '', (2, 2): '', (2.0, 3): '', (2, 4): 'wall', (2, 5): 'dot_', (2.0, 6): 'wall', (2, 7): 'wall', (2.0, 8): 'wall', (2, 9): 'dot_', (2.0, 10): 'wall', (2.0, 11): 'wall', (2, 12): 'dot_', (2.0, 13): 'wall', (2, 14): '____', (2, 15): '____',  (2, 16): '____', (2, 17): 'wall', (2.0, 18): '____', (2.000, 19): 'wall', (2, 20): '____',  (2, 21): '____', (2, 22): '____', (2.000, 23): 'wall', (2, 24): 'dot_', (2, 25): 'wall', (2, 26): 'wall', (2.000, 27): 'dot_', (2, 28): 'wall', (2, 29): 'wall', (2, 30): 'dot_', (2, 31): 'wall', (2.0000, 32): 'wall', (2, 33): 'dot_', (2, 34): 'wall', 
    (3.0, 0): '', (3, 1): '', (3, 2): '', (3.0, 3): '', (3, 4): 'wall', (3, 5): 'dot_', (3.0, 6): 'wall', (3, 7): 'wall', (3.0, 8): 'wall', (3, 9): 'dot_', (3.0, 10): 'wall', (3.0, 11): 'wall', (3, 12): 'dot_', (3.0, 13): 'wall', (3, 14): '____', (3, 15): '____',  (3, 16): '____', (3, 17): 'wall', (3.0, 18): '___', (3.000, 19): 'wall',  (3, 20): '____',  (3, 21): '____', (3, 22): '____', (3.000, 23): 'wall', (3, 24): 'dot_', (3, 25): 'wall', (3, 26): 'wall', (3.000, 27): 'dot_', (3, 28): 'dot_', (3, 29): 'dot_', (3, 30): 'dot_', (3, 31): 'wall', (3.0000, 32): 'wall', (3, 33): 'dot_', (3, 34): 'wall', 
    (4.0, 0): '', (4, 1): '', (4, 2): '', (4.0, 3): '', (4, 4): 'wall', (4, 5): 'dot_', (4.0, 6): 'wall', (4, 7): 'wall', (4.0, 8): 'wall', (4, 9): 'dot_', (4.0, 10): 'wall', (4.0, 11): 'wall', (4, 12): 'dot_', (4.0, 13): 'wall', (4, 14): '____', (4, 15): '____',  (4, 16): '____', (4, 17): 'wall', (4.0, 18): '____', (4.000, 19): 'wall', (4, 20): '____',  (4, 21): '____', (4, 22): '____', (4.000, 23): 'wall', (4, 24): 'dot_', (4, 25): 'wall', (4, 26): 'wall', (4.000, 27): 'wall', (4, 28): 'wall', (4, 29): 'wall', (4, 30): 'dot_', (4, 31): 'wall', (4.0000, 32): 'wall', (4, 33): 'dot_', (4, 34): 'wall', 
    (5.0, 0): '', (5, 1): '', (5, 2): '', (5.0, 3): '', (5, 4): 'wall', (5, 5): 'dot_', (5.0, 6): 'wall', (5, 7): 'wall', (5.0, 8): 'wall', (5, 9): 'dot_', (5.0, 10): 'wall', (5.0, 11): 'wall', (5, 12): 'dot_', (5.0, 13): 'wall', (5, 14): 'wall', (5, 15): 'wall',  (5.0, 16): 'wall', (5, 17): 'wall', (5.0, 18): '____', (5.0, 19): 'wall', (5, 20): 'wall',  (5, 21): 'wall', (5, 22): 'wall', (5.000, 23): 'wall', (5, 24): 'dot_', (5, 25): 'wall', (5, 26): 'wall', (5.000, 27): 'wall', (5, 28): 'wall', (5, 29): 'wall', (5, 30): 'dot_', (5, 31): 'wall', (5.0000, 32): 'wall', (5, 33): 'dot_', (5, 34): 'wall', 
    (6.0, 0): '', (6, 1): '', (6, 2): '', (6.0, 3): '', (6, 4): 'wall', (6, 5): 'dot_', (6.0, 6): 'dot_', (6, 7): 'dot_', (6.0, 8): 'dot_', (6, 9): 'dot_', (6.0, 10): 'dot_', (6.0, 11): 'dot_', (6, 12): 'dot_', (6.0, 13): 'dot_', (6, 14): 'dot_', (6, 15): 'dot_',  (6.0, 16): 'dot_', (6, 17): 'dot_', (6.0, 18): 'dot_', (6.0, 19): 'dot_', (6, 20): 'dot_',  (6, 21): 'dot_', (6, 22): 'dot_', (6.000, 23): 'dot_', (6, 24): 'dot_', (6, 25): 'dot_', (6, 26): 'dot_', (6.000, 27): 'dot_', (6, 28): 'dot_', (6, 29): 'dot_', (6, 30): 'dot_', (6, 31): 'wall', (6.0000, 32): 'wall', (6, 33): 'dot_', (6, 34): 'wall', 
    (7.0, 0): '', (7, 1): '', (7, 2): '', (7.0, 3): '', (7, 4): 'wall', (7, 5): 'dot_', (7.0, 6): 'wall', (7, 7): 'wall', (7.0, 8): 'wall', (7, 9): 'dot_', (7.0, 10): 'wall', (7.0, 11): 'wall', (7, 12): 'wall', (7.0, 13): 'wall', (7, 14): 'wall', (7, 15): 'wall',  (7.0, 16): 'wall', (7, 17): 'wall', (7.0, 18): '____', (7.0, 19): 'wall', (7, 20): 'wall',  (7, 21): 'wall', (7, 22): 'wall', (7.000, 23): 'wall', (7, 24): 'dot_', (7, 25): 'wall', (7, 26): 'wall', (7.000, 27): 'dot_', (7, 28): 'wall', (7, 29): 'wall', (7, 30): 'wall', (7, 31): 'wall', (7.0000, 32): 'wall', (7, 33): 'dot_', (7, 34): 'wall',
    (8.0, 0): '', (8, 1): '', (8, 2): '', (8.0, 3): '', (8, 4): 'wall', (8, 5): 'dot_', (8.0, 6): 'wall', (8, 7): 'wall', (8.0, 8): 'wall', (8, 9): 'dot_', (8.0, 10): 'wall', (8.0, 11): 'wall', (8, 12): 'wall', (8.0, 13): 'wall', (8, 14): 'wall', (8, 15): 'wall',  (8.0, 16): 'wall', (8, 17): 'wall', (8.0, 18): '____', (8.0, 19): 'wall', (8, 20): 'wall',  (8, 21): 'wall', (8, 22): 'wall', (8.000, 23): 'wall', (8, 24): 'dot_', (8, 25): 'wall', (8, 26): 'wall', (8.000, 27): 'dot_', (8, 28): 'wall', (8, 29): 'wall', (8, 30): 'wall', (8, 31): 'wall', (8.0000, 32): 'wall', (8, 33): 'dot_', (8, 34): 'wall', 
    (9.0, 0): '', (9, 1): '', (9, 2): '', (9.0, 3): '', (9, 4): 'wall', (9, 5): 'dot_', (9.0, 6): 'wall', (9, 7): 'wall', (9.0, 8): 'wall', (9, 9): 'dot_', (9.0, 10): 'dot_', (9.0, 11): 'dot_', (9, 12): 'dot_', (9.0, 13): 'wall', (9, 14): 'wall', (9, 15): '____',  (9.0, 16): '____', (9, 17): '____', (9.0, 18): '____', (9.0, 19): '____', (9, 20): '____',  (9, 21): '____', (9, 22): '____', (9.000, 23): '____', (9, 24): 'dot_', (9, 25): 'wall', (9, 26): 'wall', (9.000, 27): 'dot_', (9, 28): 'dot_', (9, 29): 'dot_', (9, 30): 'dot_', (9, 31): 'wall', (9.0000, 32): 'wall', (9, 33): 'dot_', (9, 34): 'wall', 
    (10, 0): '', (10, 1): '', (10, 2): '', (10, 3): '', (10, 4): 'wall', (10, 5): 'dot_', (10, 6): 'wall', (10, 7): 'wall', (10, 8): 'wall', (10, 9): 'dot_', (10, 10): 'wall', (10, 11): 'wall', (10, 12): 'dot_', (10, 13): 'wall', (10, 14): 'wall', (10, 15): '____', (10, 16): 'wall', (10, 17): 'wall', (10, 18): 'wall', (10, 19): 'wall', (10, 20): 'wall', (10, 21): '____', (10, 22): 'wall', (10, 23): 'wall', (10, 24): 'dot_', (10, 25): 'wall', (10, 26): 'wall', (10, 27): 'dot_', (10, 28): 'wall', (10, 29): 'wall', (10, 30): 'dot_', (10, 31): 'wall', (10, 32): 'wall', (10, 33): 'dot_', (10, 34): 'wall', 
    (11, 0): '', (11, 1): '', (11, 2): '', (11, 3): '', (11, 4): 'wall', (11, 5): 'dot_', (11, 6): 'wall', (11, 7): 'wall', (11, 8): 'wall', (11, 9): 'dot_', (11, 10): 'wall', (11, 11): 'wall', (11, 12): 'dot_', (11, 13): 'wall', (11, 14): 'wall', (11, 15): '____', (11, 16): 'wall', (11, 17): '____', (11, 18): '____', (11, 19): '____', (11, 20): 'wall', (11, 21): '____', (11, 22): 'wall', (11, 23): 'wall', (11, 24): 'dot_', (11, 25): 'wall', (11, 26): 'wall', (11, 27): 'dot_', (11, 28): 'wall', (11, 29): 'wall', (11, 30): 'dot_', (11, 31): 'wall', (11, 32): 'wall', (11, 33): 'dot_', (11, 34): 'wall', 
    (12, 0): '', (12, 1): '', (12, 2): '', (12, 3): '', (12, 4): 'wall', (12, 5): 'dot_', (12, 6): 'dot_', (12, 7): 'dot_', (12, 8): 'dot_', (12, 9): 'dot_', (12, 10): 'wall', (12, 11): 'wall', (12, 12): 'dot_', (12, 13): '____', (12, 14): '____', (12, 15): '____', (12, 16): 'wall', (12, 17): '____', (12, 18): '____', (12, 19): '____', (12, 20): 'wall', (12, 21): '____', (12, 22): 'wall', (12, 23): 'wall', (12, 24): 'dot_', (12, 25): 'dot_', (12, 26): 'dot_', (12, 27): 'dot_', (12, 28): 'wall', (12, 29): 'wall', (12, 30): 'dot_', (12, 31): 'dot_', (12, 32): 'dot_', (12, 33): 'dot_', (12, 34): 'wall', 
    (13, 0): '', (13, 1): '', (13, 2): '', (13, 3): '', (13, 4): 'wall', (13, 5): 'wall', (13, 6): 'wall', (13, 7): 'wall', (13, 8): 'wall', (13, 9): 'dot_', (13, 10): 'wall', (13, 11): 'wall', (13, 12): 'wall', (13, 13): 'wall', (13, 14): 'wall', (13, 15): '____', (13, 16): 'wall', (13, 17): '____', (13, 18): '____', (13, 19): '____', (13, 20): 'wall', (13, 21): '____', (13, 22): 'wall', (13, 23): 'wall', (13, 24): 'wall', (13, 25): 'wall', (13, 26): 'wall', (13, 27): 'dot_', (13, 28): 'wall', (13, 29): 'wall', (13, 30): 'wall', (13, 31): 'wall', (13, 32): 'wall', (13, 33): 'dot_', (13, 34): 'wall', 
    (14, 0): '', (14, 1): '', (14, 2): '', (14, 3): '', (14, 4): 'wall', (14, 5): 'wall', (14, 6): 'wall', (14, 7): 'wall', (14, 8): 'wall', (14, 9): 'dot_', (14, 10): 'wall', (14, 11): 'wall', (14, 12): 'wall', (14, 13): 'wall', (14, 14): 'wall', (14, 15): '____', (14, 16): 'wall', (14, 17): '____', (14, 18): '____', (14, 19): '____', (14, 20): 'wall', (14, 21): '____', (14, 22): 'wall', (14, 23): 'wall', (14, 24): 'wall', (14, 25): 'wall', (14, 26): 'wall', (14, 27): 'dot_', (14, 28): 'wall', (14, 29): 'wall', (14, 30): 'wall', (14, 31): 'wall', (14, 32): 'wall', (14, 33): 'dot_', (14, 34): 'wall', 
    (15, 0): '', (15, 1): '', (15, 2): '', (15, 3): '', (15, 4): 'wall', (15, 5): 'dot_', (15, 6): 'dot_', (15, 7): 'dot_', (15, 8): 'dot_', (15, 9): 'dot_', (15, 10): 'wall', (15, 11): 'wall', (15, 12): 'dot_', (15, 13): '____', (15, 14): '____', (15, 15): '____', (15, 16): 'wall', (15, 17): '____', (15, 18): '____', (15, 19): '____', (15, 20): 'wall', (15, 21): '____', (15, 22): 'wall', (15, 23): 'wall', (15, 24): 'dot_', (15, 25): 'dot_', (15, 26): 'dot_', (15, 27): 'dot_', (15, 28): 'wall', (15, 29): 'wall', (15, 30): 'dot_', (15, 31): 'dot_', (15, 32): 'dot_', (15, 33): 'dot_', (15, 34): 'wall', 
    (16, 0): '', (16, 1): '', (16, 2): '', (16, 3): '', (16, 4): 'wall', (16, 5): 'dot_', (16, 6): 'wall', (16, 7): 'wall', (16, 8): 'wall', (16, 9): 'dot_', (16, 10): 'wall', (16, 11): 'wall', (16, 12): 'dot_', (16, 13): 'wall', (16, 14): 'wall', (16, 15): '____', (16, 16): 'wall', (16, 17): '____', (16, 18): '____', (16, 19): '____', (16, 20): 'wall', (16, 21): '____', (16, 22): 'wall', (16, 23): 'wall', (16, 24): 'dot_', (16, 25): 'wall', (16, 26): 'wall', (16, 27): 'dot_', (16, 28): 'wall', (16, 29): 'wall', (16, 30): 'dot_', (16, 31): 'wall', (16, 32): 'wall', (16, 33): 'dot_', (16, 34): 'wall', 
    (17, 0): '', (17, 1): '', (17, 2): '', (17, 3): '', (17, 4): 'wall', (17, 5): 'dot_', (17, 6): 'wall', (17, 7): 'wall', (17, 8): 'wall', (17, 9): 'dot_', (17, 10): 'wall', (17, 11): 'wall', (17, 12): 'dot_', (17, 13): 'wall', (17, 14): 'wall', (17, 15): '____', (17, 16): 'wall', (17, 17): 'wall', (17, 18): 'wall', (17, 19): 'wall', (17, 20): 'wall', (17, 21): '____', (17, 22): 'wall', (17, 23): 'wall', (17, 24): 'dot_', (17, 25): 'wall', (17, 26): 'wall', (17, 27): 'dot_', (17, 28): 'wall', (17, 29): 'wall', (17, 30): 'dot_', (17, 31): 'wall', (17, 32): 'wall', (17, 33): 'dot_', (17, 34): 'wall',
    (18, 0): '', (18, 1): '', (18, 2): '', (18, 3): '', (18, 4): 'wall', (18, 5): 'dot_', (18, 6): 'wall', (18, 7): 'wall', (18, 8): 'wall', (18, 9): 'dot_', (18, 10): 'dot_', (18, 11): 'dot_', (18, 12): 'dot_', (18, 13): 'wall', (18, 14): 'wall', (18, 15): '____', (18, 16): '____', (18, 17): '____', (18, 18): '____', (18, 19): '____', (18, 20): '____', (18, 21): '____', (18, 22): '____', (18, 23): '____', (18, 24): 'dot_', (18, 25): 'wall', (18, 26): 'wall', (18, 27): 'dot_', (18, 28): 'dot_', (18, 29): 'dot_', (18, 30): 'dot_', (18, 31): 'wall', (18, 32): 'wall', (18, 33): 'dot_', (18, 34): 'wall', 
    (19, 0): '', (19, 1): '', (19, 2): '', (19, 3): '', (19, 4): 'wall', (19, 5): 'dot_', (19, 6): 'wall', (19, 7): 'wall', (19, 8): 'wall', (19, 9): 'dot_', (19, 10): 'wall', (19, 11): 'wall', (19, 12): 'wall', (19, 13): 'wall', (19, 14): 'wall', (19, 15): 'wall', (19, 16): 'wall', (19, 17): 'wall', (19, 18): '____', (19, 19): 'wall', (19, 20): 'wall', (19, 21): 'wall', (19, 22): 'wall', (19, 23): 'wall', (19, 24): 'dot_', (19, 25): 'wall', (19, 26): 'wall', (19, 27): 'dot_', (19, 28): 'wall', (19, 29): 'wall', (19, 30): 'wall', (19, 31): 'wall', (19, 32): 'wall', (19, 33): 'dot_', (19, 34): 'wall',
    (20, 0): '', (20, 1): '', (20, 2): '', (20, 3): '', (20, 4): 'wall', (20, 5): 'dot_', (20, 6): 'wall', (20, 7): 'wall', (20, 8): 'wall', (20, 9): 'dot_', (20, 10): 'wall', (20, 11): 'wall', (20, 12): 'wall', (20, 13): 'wall', (20, 14): 'wall', (20, 15): 'wall', (20, 16): 'wall', (20, 17): 'wall', (20, 18): '____', (20, 19): 'wall', (20, 20): 'wall', (20, 21): 'wall', (20, 22): 'wall', (20, 23): 'wall', (20, 24): 'dot_', (20, 25): 'wall', (20, 26): 'wall', (20, 27): 'dot_', (20, 28): 'wall', (20, 29): 'wall', (20, 30): 'wall', (20, 31): 'wall', (20, 32): 'wall', (20, 33): 'dot_', (20, 34): 'wall', 
    (21, 0): '', (21, 1): '', (21, 2): '', (21, 3): '', (21, 4): 'wall', (21, 5): 'dot_', (21, 6): 'dot_', (21, 7): 'dot_', (21, 8): 'dot_', (21, 9): 'dot_', (21, 10): 'dot_', (21, 11): 'dot_', (21, 12): 'dot_', (21, 13): 'dot_', (21, 14): 'dot_', (21, 15): 'dot_', (21, 16): 'dot_', (21, 17): 'dot_', (21, 18): 'dot_', (21, 19): 'dot_', (21, 20): 'dot_', (21, 21): 'dot_', (21, 22): 'dot_', (21, 23): 'dot_', (21, 24): 'dot_', (21, 25): 'dot_', (21, 26): 'dot_', (21, 27): 'dot_', (21, 28): 'dot_', (21, 29): 'dot_', (21, 30): 'dot_', (21, 31): 'wall', (21, 32): 'wall', (21, 33): 'dot_', (21, 34): 'wall', 
    (22, 0): '', (22, 1): '', (22, 2): '', (22, 3): '', (22, 4): 'wall', (22, 5): 'dot_', (22, 6): 'wall', (22, 7): 'wall', (22, 8): 'wall', (22, 9): 'dot_', (22, 10): 'wall', (22, 11): 'wall', (22, 12): 'dot_', (22, 13): 'wall', (22, 14): 'wall', (22, 15): 'wall', (22, 16): 'wall', (22, 17): 'wall', (22, 18): '____', (22, 19): 'wall', (22, 20): 'wall', (22, 21): 'wall', (22, 22): 'wall', (22, 23): 'wall', (22, 24): 'dot_', (22, 25): 'wall', (22, 26): 'wall', (22, 27): 'wall', (22, 28): 'wall', (22, 29): 'wall', (22, 30): 'dot_', (22, 31): 'wall', (22, 32): 'wall', (22, 33): 'dot_', (22, 34): 'wall', 
    (23, 0): '', (23, 1): '', (23, 2): '', (23, 3): '', (23, 4): 'wall', (23, 5): 'dot_', (23, 6): 'wall', (23, 7): 'wall', (23, 8): 'wall', (23, 9): 'dot_', (23, 10): 'wall', (23, 11): 'wall', (23, 12): 'dot_', (23, 13): 'wall', (23, 14): '____', (23, 15): '____', (23, 16): '____', (23, 17): 'wall', (23, 18): '____', (23, 19): 'wall', (23, 20): '____', (23, 21): '____', (23, 22): '____', (23, 23): 'wall', (23, 24): 'dot_', (23, 25): 'wall', (23, 26): 'wall', (23, 27): 'wall', (23, 28): 'wall', (23, 29): 'wall', (23, 30): 'dot_', (23, 31): 'wall', (23, 32): 'wall', (23, 33): 'dot_', (23, 34): 'wall', 
    (24, 0): '', (24, 1): '', (24, 2): '', (24, 3): '', (24, 4): 'wall', (24, 5): 'dot_', (24, 6): 'wall', (24, 7): 'wall', (24, 8): 'wall', (24, 9): 'dot_', (24, 10): 'wall', (24, 11): 'wall', (24, 12): 'dot_', (24, 13): 'wall', (24, 14): '____', (24, 15): '____', (24, 16): '____', (24, 17): 'wall', (24, 18): '____', (24, 19): 'wall', (24, 20): '____', (24, 21): '____', (24, 22): '____', (24, 23): 'wall', (24, 24): 'dot_', (24, 25): 'wall', (24, 26): 'wall', (24, 27): 'dot_', (24, 28): 'dot_', (24, 29): 'dot_', (24, 30): 'dot_', (24, 31): 'wall', (24, 32): 'wall', (24, 33): 'dot_', (24, 34): 'wall', 
    (25, 0): '', (25, 1): '', (25, 2): '', (25, 3): '', (25, 4): 'wall', (25, 5): 'dot_', (25, 6): 'wall', (25, 7): 'wall', (25, 8): 'wall', (25, 9): 'dot_', (25, 10): 'wall', (25, 11): 'wall', (25, 12): 'dot_', (25, 13): 'wall', (25, 14): '____', (25, 15): '____', (25, 16): '____', (25, 17): 'wall', (25, 18): '____', (25, 19): 'wall', (25, 20): '____', (25, 21): '____', (25, 22): '____', (25, 23): 'wall', (25, 24): 'dot_', (25, 25): 'wall', (25, 26): 'wall', (25, 27): 'dot_', (25, 28): 'wall', (25, 29): 'wall', (25, 30): 'dot_', (25, 31): 'wall', (25, 32): 'wall', (25, 33): 'dot_', (25, 34): 'wall', 
    (26, 0): '', (26, 1): '', (26, 2): '', (26, 3): '', (26, 4): 'wall', (26, 5): 'dot_', (26, 6): 'dot_', (26, 7): 'dot_', (26, 8): 'dot_', (26, 9): 'dot_', (26, 10): 'dot_', (26, 11): 'dot_', (26, 12): 'dot_', (26, 13): 'wall', (26, 14): '____', (26, 15): '____', (26, 16): '____', (26, 17): 'wall', (26, 18): '____', (26, 19): 'wall', (26, 20): '____', (26, 21): '____', (26, 22): '____', (26, 23): 'wall', (26, 24): 'dot_', (26, 25): 'dot_', (26, 26): 'dot_', (26, 27): 'dot_', (26, 28): 'wall', (26, 29): 'wall', (26, 30): 'dot_', (26, 31): 'dot_', (26, 32): 'dot_', (26, 33): 'dot_', (26, 34): 'wall', 
    (27, 0): '', (27, 1): '', (27, 2): '', (27, 3): '', (27, 4): 'wall', (27, 5): 'wall', (27, 6): 'wall', (27, 7): 'wall', (27, 8): 'wall', (27, 9): 'wall', (27, 10): 'wall', (27, 11): 'wall', (27, 12): 'wall', (27, 13): 'wall', (27, 14): '____', (27, 15): '____', (27, 16): '____', (27, 17): 'wall', (27, 18): '____', (27, 19): 'wall', (27, 20): '____', (27, 21): '____', (27, 22): '____', (27, 23): 'wall', (27, 24): 'wall', (27, 25): 'wall', (27, 26): 'wall', (27, 27): 'wall', (27, 28): 'wall', (27, 29): 'wall', (27, 30): 'wall', (27, 31): 'wall', (27, 32): 'wall', (27, 33): 'wall', (27, 34): 'wall', 
}







def check_escape():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()


def menu():
    screen.fill((0, 0, 0))  # Clear the screen with a black background
    
    pygame.draw.rect(screen, blue, outside_border, border_radius=15)
    pygame.draw.rect(screen, black, inside_border, border_radius=15)
    screen.blit(background,(250, 5))
    


def find_cordinates(x,y):
    px = (18*x) + 250
    py = (18*y)+ -20
    return px,py


def run_graph(level):
    for key in level:
        x,y = key
        
        if key == (x,y):
            px,py = find_cordinates(key[0],key[1])
            if level[(x,y)] == 'dot_':
                screen.blit(dot_,(px,py))
            # if level[(x,y)] == 'wall':
            #     screen.blit(wall,(px,py))

def display(image, pos):
    # Offset values from the edge of the screen
    offset_x = 55
    offset_y = 60
    
    # Set x, y values. Converting from tile size to pixels, and centering the position of the image 
    image_pos_x = 800 - (pos.x * 18 + offset_x) - image.get_width() / 2
    image_pos_y = pos.y * 18 + offset_y - image.get_height() / 2
    screen.blit(image, (image_pos_x, image_pos_y)) # Display to screen

def __main__():
    # Begin
    pacman = Ghosts.Ghost('o') # CHANGE FROM GHOST CLASS TO PACMAN CLASS
    ghosts = [
        Ghosts.Ghost('r'),
        Ghosts.Ghost('p'),
        Ghosts.Ghost('b'),
        Ghosts.Ghost('o')
    ]
    
    dir = ''
    phase = 'c'
    for ghost in ghosts:
        ghost.target = pacman.pos # Update target
    
    # Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw menu and check for escape
        menu()
        check_escape()
        run_graph(grid)
        
        # Update ghost data
        Ghosts.update_ghosts(ghosts, pacman, grid, Ghosts.decision_tiles, phase)
        
        # Update display
        for ghost in ghosts:
            display(images[ghost.id], ghost.pos)
        display(images["pacman"], pacman.pos)
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)  # Adjust as necessary for smoothness
        
        # Direction controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dir = 'w'
        elif keys[pygame.K_a]:
            dir = 'a'
        elif keys[pygame.K_s]:
            dir = 's'
        elif keys[pygame.K_d]:
            dir = 'd'
        else:
            continue
        
        # Update pacman direction
        pacman.dir = dir
        Ghosts.move(pacman, .3)

    pygame.quit()


__main__()