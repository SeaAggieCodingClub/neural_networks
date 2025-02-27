import pygame
import copy
from Ghosts import Ghost
from Pacman import Pacman
from Fruit import Fruit, update_fruit
from Score import Score
from Position import *
import Ghosts
import Sound

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import gym
import numpy as np
import random
import datetime
import time
from collections import deque
from gym import spaces
# import tensorflow as tf
# from tensorflow.keras.layers import Input, Dense # type: ignore
# from tensorflow.keras.models import Sequential, load_model # type: ignore
# from tensorflow.keras.optimizers import Adam # type: ignore

class PacManGame(gym.Env):
    def __init__(self):
        super(PacManGame, self).__init__() # Create gym environment
        pygame.init()
        
        # --------------------PYGAME SETUP--------------------
        # Get the screen resolution
        self.screen_info = pygame.display.Info()
        self.screen_width, screen_height = self.screen_info.current_w, self.screen_info.current_h
        
        # Calculate position for the window to be centered at the top-right
        self.window_width, window_height = 640, 480
        self.top_right_x = self.screen_width - self.window_width - 175
        self.top_right_y = 0
        
        # Set environment variable for window position
        #os.environ['SDL_VIDEO_WINDOW_POS'] = f"{top_right_x},{top_right_y}"
        
        # Screen size
        self.width = 800
        self.height = 650
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pacman')
        
        # Menu variables
        self.outside_border = pygame.Rect(10, 15, 200, self.height - 30)
        self.inside_border = pygame.Rect(15, 20, 190, self.height - 40)
        
        # Images
        self.background = pygame.image.load("Pacman/images/background.png")
        self.dot_ = pygame.image.load("Pacman/images/dot.png")
        self.pdot = pygame.transform.scale(self.dot_, (40, 40))
        abyss = pygame.image.load("Pacman/images/black.png")
        self.abyss = pygame.transform.scale(abyss, (35, 35))
        
        # Color definitions
        self.black = (10, 10, 10)  # Changed to white color for clarity
        self.blue = (32,36,221)
        
        # Set clock speed
        self.clock = pygame.time.Clock()
        
        # --------------------NEURAL NETWORK SETUP--------------------
        self.state = {
            "pacman": None, # Position of pacman
            "ghosts": None, # Dict of Position of ghosts
            "pellets": None, # Numpy array of Position of pellets
            "fruit": None, # Bool of whether fruit exist
            "level": None, # Int of level
            "score": None, # Int of current score
            "lives": None, # Int of lives
            "phase": None, # Int of phase key
        }
        self.action_space = spaces.Discrete(4) # W, A, S, and D controls
        # Observation space??????
        
        '''{
                "r":
                "p":
                "b":
                "o":
            }'''
        
        # Duration for ghost phases
        self.phase_lengths = [{ # Level 1
                'c':[
                    20,
                    20,
                    20,
                    1e10 # Indefinitely
                ],
                's':[
                    7,
                    7,
                    5,
                    5
                ]
            },
            { # Levels 2-4
                'c':[
                    20,
                    20,
                    1033, # 17 minutes and 13 seconds
                    1e10 # Indefinitely
                ],
                's':[
                    7,
                    7,
                    5,
                    1/60
                ]
            },
            { # Levels 5+
                'c':[
                    20,
                    20,
                    1037, # 17 minutes and 17 seconds
                    1e10 # Indefinitely
                ],
                's':[
                    5,
                    5,
                    5,
                    1/60
                ]
            }
        ]
        
        # Starting grid layout
        self.grid = {
            (0 , 0): 'wall', (0 , 1): 'wall', (0 , 2): 'wall', (0 , 3): 'wall', (0 , 4): 'wall', (0 , 5): 'wall', (0 , 6): 'wall', (0 , 7): 'wall', (0 , 8): 'wall', (0 , 9): 'wall', (0 , 10): '____', (0 , 11): '____', (0 , 12): '____', (0 , 13): 'wall', (0 , 14): '____', (0 , 15): 'wall', (0 , 16): '____', (0 , 17): '____', (0 , 18): '____', (0 , 19): 'wall', (0 , 20): 'wall', (0 , 21): 'wall', (0 , 22): 'wall', (0 , 23): 'wall', (0 , 24): 'wall', (0 , 25): 'wall', (0 , 26): 'wall', (0 , 27): 'wall', (0 , 28): 'wall', (0 , 29): 'wall', (0 , 30): 'wall', 
            (1 , 0): 'wall', (1 , 1): 'dot_', (1 , 2): 'dot_', (1 , 3): 'pdot', (1 , 4): 'dot_', (1 , 5): 'dot_', (1 , 6): 'dot_', (1 , 7): 'dot_', (1 , 8): 'dot_', (1 , 9): 'wall', (1 , 10): '____', (1 , 11): '____', (1 , 12): '____', (1 , 13): 'wall', (1 , 14): '____', (1 , 15): 'wall', (1 , 16): '____', (1 , 17): '____', (1 , 18): '____', (1 , 19): 'wall', (1 , 20): 'dot_', (1 , 21): 'dot_', (1 , 22): 'dot_', (1 , 23): 'pdot', (1 , 24): 'wall', (1 , 25): 'wall', (1 , 26): 'dot_', (1 , 27): 'dot_', (1 , 28): 'dot_', (1 , 29): 'dot_', (1 , 30): 'wall', 
            (2 , 0): 'wall', (2 , 1): 'dot_', (2 , 2): 'wall', (2 , 3): 'wall', (2 , 4): 'wall', (2 , 5): 'dot_', (2 , 6): 'wall', (2 , 7): 'wall', (2 , 8): 'dot_', (2 , 9): 'wall', (2 , 10): '____', (2 , 11): '____', (2 , 12): '____', (2 , 13): 'wall', (2 , 14): '____', (2 , 15): 'wall', (2 , 16): '____', (2 , 17): '____', (2 , 18): '____', (2 , 19): 'wall', (2 , 20): 'dot_', (2 , 21): 'wall', (2 , 22): 'wall', (2 , 23): 'dot_', (2 , 24): 'wall', (2 , 25): 'wall', (2 , 26): 'dot_', (2 , 27): 'wall', (2 , 28): 'wall', (2 , 29): 'dot_', (2 , 30): 'wall', 
            (3 , 0): 'wall', (3 , 1): 'dot_', (3 , 2): 'wall', (3 , 3): 'wall', (3 , 4): 'wall', (3 , 5): 'dot_', (3 , 6): 'wall', (3 , 7): 'wall', (3 , 8): 'dot_', (3 , 9): 'wall', (3 , 10): '____', (3 , 11): '____', (3 , 12): '____', (3 , 13): 'wall', (3 , 14): '____', (3 , 15): 'wall', (3 , 16): '____', (3 , 17): '____', (3 , 18): '____', (3 , 19): 'wall', (3 , 20): 'dot_', (3 , 21): 'wall', (3 , 22): 'wall', (3 , 23): 'dot_', (3 , 24): 'dot_', (3 , 25): 'dot_', (3 , 26): 'dot_', (3 , 27): 'wall', (3 , 28): 'wall', (3 , 29): 'dot_', (3 , 30): 'wall', 
            (4 , 0): 'wall', (4 , 1): 'dot_', (4 , 2): 'wall', (4 , 3): 'wall', (4 , 4): 'wall', (4 , 5): 'dot_', (4 , 6): 'wall', (4 , 7): 'wall', (4 , 8): 'dot_', (4 , 9): 'wall', (4 , 10): '____', (4 , 11): '____', (4 , 12): '____', (4 , 13): 'wall', (4 , 14): '____', (4 , 15): 'wall', (4 , 16): '____', (4 , 17): '____', (4 , 18): '____', (4 , 19): 'wall', (4 , 20): 'dot_', (4 , 21): 'wall', (4 , 22): 'wall', (4 , 23): 'wall', (4 , 24): 'wall', (4 , 25): 'wall', (4 , 26): 'dot_', (4 , 27): 'wall', (4 , 28): 'wall', (4 , 29): 'dot_', (4 , 30): 'wall', 
            (5 , 0): 'wall', (5 , 1): 'dot_', (5 , 2): 'wall', (5 , 3): 'wall', (5 , 4): 'wall', (5 , 5): 'dot_', (5 , 6): 'wall', (5 , 7): 'wall', (5 , 8): 'dot_', (5 , 9): 'wall', (5 , 10): 'wall', (5 , 11): 'wall', (5 , 12): 'wall', (5 , 13): 'wall', (5 , 14): '____', (5 , 15): 'wall', (5 , 16): 'wall', (5 , 17): 'wall', (5 , 18): 'wall', (5 , 19): 'wall', (5 , 20): 'dot_', (5 , 21): 'wall', (5 , 22): 'wall', (5 , 23): 'wall', (5 , 24): 'wall', (5 , 25): 'wall', (5 , 26): 'dot_', (5 , 27): 'wall', (5 , 28): 'wall', (5 , 29): 'dot_', (5 , 30): 'wall', 
            (6 , 0): 'wall', (6 , 1): 'dot_', (6 , 2): 'dot_', (6 , 3): 'dot_', (6 , 4): 'dot_', (6 , 5): 'dot_', (6 , 6): 'dot_', (6 , 7): 'dot_', (6 , 8): 'dot_', (6 , 9): 'dot_', (6 , 10): 'dot_', (6 , 11): 'dot_', (6 , 12): 'dot_', (6 , 13): 'dot_', (6 , 14): 'dot_', (6 , 15): 'dot_', (6 , 16): 'dot_', (6 , 17): 'dot_', (6 , 18): 'dot_', (6 , 19): 'dot_', (6 , 20): 'dot_', (6 , 21): 'dot_', (6 , 22): 'dot_', (6 , 23): 'dot_', (6 , 24): 'dot_', (6 , 25): 'dot_', (6 , 26): 'dot_', (6 , 27): 'wall', (6 , 28): 'wall', (6 , 29): 'dot_', (6 , 30): 'wall', 
            (7 , 0): 'wall', (7 , 1): 'dot_', (7 , 2): 'wall', (7 , 3): 'wall', (7 , 4): 'wall', (7 , 5): 'dot_', (7 , 6): 'wall', (7 , 7): 'wall', (7 , 8): 'wall', (7 , 9): 'wall', (7 , 10): 'wall', (7 , 11): 'wall', (7 , 12): 'wall', (7 , 13): 'wall', (7 , 14): '____', (7 , 15): 'wall', (7 , 16): 'wall', (7 , 17): 'wall', (7 , 18): 'wall', (7 , 19): 'wall', (7 , 20): 'dot_', (7 , 21): 'wall', (7 , 22): 'wall', (7 , 23): 'dot_', (7 , 24): 'wall', (7 , 25): 'wall', (7 , 26): 'wall', (7 , 27): 'wall', (7 , 28): 'wall', (7 , 29): 'dot_', (7 , 30): 'wall', 
            (8 , 0): 'wall', (8 , 1): 'dot_', (8 , 2): 'wall', (8 , 3): 'wall', (8 , 4): 'wall', (8 , 5): 'dot_', (8 , 6): 'wall', (8 , 7): 'wall', (8 , 8): 'wall', (8 , 9): 'wall', (8 , 10): 'wall', (8 , 11): 'wall', (8 , 12): 'wall', (8 , 13): 'wall', (8 , 14): '____', (8 , 15): 'wall', (8 , 16): 'wall', (8 , 17): 'wall', (8 , 18): 'wall', (8 , 19): 'wall', (8 , 20): 'dot_', (8 , 21): 'wall', (8 , 22): 'wall', (8 , 23): 'dot_', (8 , 24): 'wall', (8 , 25): 'wall', (8 , 26): 'wall', (8 , 27): 'wall', (8 , 28): 'wall', (8 , 29): 'dot_', (8 , 30): 'wall', 
            (9 , 0): 'wall', (9 , 1): 'dot_', (9 , 2): 'wall', (9 , 3): 'wall', (9 , 4): 'wall', (9 , 5): 'dot_', (9 , 6): 'dot_', (9 , 7): 'dot_', (9 , 8): 'dot_', (9 , 9): 'wall', (9 , 10): 'wall', (9 , 11): '____', (9 , 12): '____', (9 , 13): '____', (9 , 14): '____', (9 , 15): '____', (9 , 16): '____', (9 , 17): '____', (9 , 18): '____', (9 , 19): '____', (9 , 20): 'dot_', (9 , 21): 'wall', (9 , 22): 'wall', (9 , 23): 'dot_', (9 , 24): 'dot_', (9 , 25): 'dot_', (9 , 26): 'dot_', (9 , 27): 'wall', (9 , 28): 'wall', (9 , 29): 'dot_', (9 , 30): 'wall', 
            (10, 0): 'wall', (10, 1): 'dot_', (10, 2): 'wall', (10, 3): 'wall', (10, 4): 'wall', (10, 5): 'dot_', (10, 6): 'wall', (10, 7): 'wall', (10, 8): 'dot_', (10, 9): 'wall', (10, 10): 'wall', (10, 11): '____', (10, 12): 'wall', (10, 13): 'wall', (10, 14): 'wall', (10, 15): 'wall', (10, 16): 'wall', (10, 17): '____', (10, 18): 'wall', (10, 19): 'wall', (10, 20): 'dot_', (10, 21): 'wall', (10, 22): 'wall', (10, 23): 'dot_', (10, 24): 'wall', (10, 25): 'wall', (10, 26): 'dot_', (10, 27): 'wall', (10, 28): 'wall', (10, 29): 'dot_', (10 , 30): 'wall', 
            (11, 0): 'wall', (11, 1): 'dot_', (11, 2): 'wall', (11, 3): 'wall', (11, 4): 'wall', (11, 5): 'dot_', (11, 6): 'wall', (11, 7): 'wall', (11, 8): 'dot_', (11, 9): 'wall', (11, 10): 'wall', (11, 11): '____', (11, 12): 'wall', (11, 13): '____', (11, 14): '____', (11, 15): '____', (11, 16): 'wall', (11, 17): '____', (11, 18): 'wall', (11, 19): 'wall', (11, 20): 'dot_', (11, 21): 'wall', (11, 22): 'wall', (11, 23): 'dot_', (11, 24): 'wall', (11, 25): 'wall', (11, 26): 'dot_', (11, 27): 'wall', (11, 28): 'wall', (11, 29): 'dot_', (11 , 30): 'wall', 
            (12, 0): 'wall', (12, 1): 'dot_', (12, 2): 'dot_', (12, 3): 'dot_', (12, 4): 'dot_', (12, 5): 'dot_', (12, 6): 'wall', (12, 7): 'wall', (12, 8): 'dot_', (12, 9): '____', (12, 10): '____', (12, 11): '____', (12, 12): 'wall', (12, 13): '____', (12, 14): '____', (12, 15): '____', (12, 16): 'wall', (12, 17): '____', (12, 18): 'wall', (12, 19): 'wall', (12, 20): 'dot_', (12, 21): 'dot_', (12, 22): 'dot_', (12, 23): 'dot_', (12, 24): 'wall', (12, 25): 'wall', (12, 26): 'dot_', (12, 27): 'dot_', (12, 28): 'dot_', (12, 29): 'dot_', (12 , 30): 'wall', 
            (13, 0): 'wall', (13, 1): 'wall', (13, 2): 'wall', (13, 3): 'wall', (13, 4): 'wall', (13, 5): 'dot_', (13, 6): 'wall', (13, 7): 'wall', (13, 8): 'wall', (13, 9): 'wall', (13, 10): 'wall', (13, 11): '____', (13, 12): 'wall', (13, 13): '____', (13, 14): '____', (13, 15): '____', (13, 16): 'wall', (13, 17): '____', (13, 18): 'wall', (13, 19): 'wall', (13, 20): 'wall', (13, 21): 'wall', (13, 22): 'wall', (13, 23): 'dot_', (13, 24): 'wall', (13, 25): 'wall', (13, 26): 'wall', (13, 27): 'wall', (13, 28): 'wall', (13, 29): 'dot_', (13 , 30): 'wall', 
            (14, 0): 'wall', (14, 1): 'wall', (14, 2): 'wall', (14, 3): 'wall', (14, 4): 'wall', (14, 5): 'dot_', (14, 6): 'wall', (14, 7): 'wall', (14, 8): 'wall', (14, 9): 'wall', (14, 10): 'wall', (14, 11): '____', (14, 12): 'wall', (14, 13): '____', (14, 14): '____', (14, 15): '____', (14, 16): 'wall', (14, 17): '____', (14, 18): 'wall', (14, 19): 'wall', (14, 20): 'wall', (14, 21): 'wall', (14, 22): 'wall', (14, 23): 'dot_', (14, 24): 'wall', (14, 25): 'wall', (14, 26): 'wall', (14, 27): 'wall', (14, 28): 'wall', (14, 29): 'dot_', (14 , 30): 'wall', 
            (15, 0): 'wall', (15, 1): 'dot_', (15, 2): 'dot_', (15, 3): 'dot_', (15, 4): 'dot_', (15, 5): 'dot_', (15, 6): 'wall', (15, 7): 'wall', (15, 8): 'dot_', (15, 9): '____', (15, 10): '____', (15, 11): '____', (15, 12): 'wall', (15, 13): '____', (15, 14): '____', (15, 15): '____', (15, 16): 'wall', (15, 17): '____', (15, 18): 'wall', (15, 19): 'wall', (15, 20): 'dot_', (15, 21): 'dot_', (15, 22): 'dot_', (15, 23): 'dot_', (15, 24): 'wall', (15, 25): 'wall', (15, 26): 'dot_', (15, 27): 'dot_', (15, 28): 'dot_', (15, 29): 'dot_', (15 , 30): 'wall', 
            (16, 0): 'wall', (16, 1): 'dot_', (16, 2): 'wall', (16, 3): 'wall', (16, 4): 'wall', (16, 5): 'dot_', (16, 6): 'wall', (16, 7): 'wall', (16, 8): 'dot_', (16, 9): 'wall', (16, 10): 'wall', (16, 11): '____', (16, 12): 'wall', (16, 13): '____', (16, 14): '____', (16, 15): '____', (16, 16): 'wall', (16, 17): '____', (16, 18): 'wall', (16, 19): 'wall', (16, 20): 'dot_', (16, 21): 'wall', (16, 22): 'wall', (16, 23): 'dot_', (16, 24): 'wall', (16, 25): 'wall', (16, 26): 'dot_', (16, 27): 'wall', (16, 28): 'wall', (16, 29): 'dot_', (16 , 30): 'wall', 
            (17, 0): 'wall', (17, 1): 'dot_', (17, 2): 'wall', (17, 3): 'wall', (17, 4): 'wall', (17, 5): 'dot_', (17, 6): 'wall', (17, 7): 'wall', (17, 8): 'dot_', (17, 9): 'wall', (17, 10): 'wall', (17, 11): '____', (17, 12): 'wall', (17, 13): 'wall', (17, 14): 'wall', (17, 15): 'wall', (17, 16): 'wall', (17, 17): '____', (17, 18): 'wall', (17, 19): 'wall', (17, 20): 'dot_', (17, 21): 'wall', (17, 22): 'wall', (17, 23): 'dot_', (17, 24): 'wall', (17, 25): 'wall', (17, 26): 'dot_', (17, 27): 'wall', (17, 28): 'wall', (17, 29): 'dot_', (17 , 30): 'wall', 
            (18, 0): 'wall', (18, 1): 'dot_', (18, 2): 'wall', (18, 3): 'wall', (18, 4): 'wall', (18, 5): 'dot_', (18, 6): 'dot_', (18, 7): 'dot_', (18, 8): 'dot_', (18, 9): 'wall', (18, 10): 'wall', (18, 11): '____', (18, 12): '____', (18, 13): '____', (18, 14): '____', (18, 15): '____', (18, 16): '____', (18, 17): '____', (18, 18): '____', (18, 19): '____', (18, 20): 'dot_', (18, 21): 'wall', (18, 22): 'wall', (18, 23): 'dot_', (18, 24): 'dot_', (18, 25): 'dot_', (18, 26): 'dot_', (18, 27): 'wall', (18, 28): 'wall', (18, 29): 'dot_', (18 , 30): 'wall', 
            (19, 0): 'wall', (19, 1): 'dot_', (19, 2): 'wall', (19, 3): 'wall', (19, 4): 'wall', (19, 5): 'dot_', (19, 6): 'wall', (19, 7): 'wall', (19, 8): 'wall', (19, 9): 'wall', (19, 10): 'wall', (19, 11): 'wall', (19, 12): 'wall', (19, 13): 'wall', (19, 14): '____', (19, 15): 'wall', (19, 16): 'wall', (19, 17): 'wall', (19, 18): 'wall', (19, 19): 'wall', (19, 20): 'dot_', (19, 21): 'wall', (19, 22): 'wall', (19, 23): 'dot_', (19, 24): 'wall', (19, 25): 'wall', (19, 26): 'wall', (19, 27): 'wall', (19, 28): 'wall', (19, 29): 'dot_', (19 , 30): 'wall', 
            (20, 0): 'wall', (20, 1): 'dot_', (20, 2): 'wall', (20, 3): 'wall', (20, 4): 'wall', (20, 5): 'dot_', (20, 6): 'wall', (20, 7): 'wall', (20, 8): 'wall', (20, 9): 'wall', (20, 10): 'wall', (20, 11): 'wall', (20, 12): 'wall', (20, 13): 'wall', (20, 14): '____', (20, 15): 'wall', (20, 16): 'wall', (20, 17): 'wall', (20, 18): 'wall', (20, 19): 'wall', (20, 20): 'dot_', (20, 21): 'wall', (20, 22): 'wall', (20, 23): 'dot_', (20, 24): 'wall', (20, 25): 'wall', (20, 26): 'wall', (20, 27): 'wall', (20, 28): 'wall', (20, 29): 'dot_', (20 , 30): 'wall', 
            (21, 0): 'wall', (21, 1): 'dot_', (21, 2): 'dot_', (21, 3): 'dot_', (21, 4): 'dot_', (21, 5): 'dot_', (21, 6): 'dot_', (21, 7): 'dot_', (21, 8): 'dot_', (21, 9): 'dot_', (21, 10): 'dot_', (21, 11): 'dot_', (21, 12): 'dot_', (21, 13): 'dot_', (21, 14): 'dot_', (21, 15): 'dot_', (21, 16): 'dot_', (21, 17): 'dot_', (21, 18): 'dot_', (21, 19): 'dot_', (21, 20): 'dot_', (21, 21): 'dot_', (21, 22): 'dot_', (21, 23): 'dot_', (21, 24): 'dot_', (21, 25): 'dot_', (21, 26): 'dot_', (21, 27): 'wall', (21, 28): 'wall', (21, 29): 'dot_', (21 , 30): 'wall', 
            (22, 0): 'wall', (22, 1): 'dot_', (22, 2): 'wall', (22, 3): 'wall', (22, 4): 'wall', (22, 5): 'dot_', (22, 6): 'wall', (22, 7): 'wall', (22, 8): 'dot_', (22, 9): 'wall', (22, 10): 'wall', (22, 11): 'wall', (22, 12): 'wall', (22, 13): 'wall', (22, 14): '____', (22, 15): 'wall', (22, 16): 'wall', (22, 17): 'wall', (22, 18): 'wall', (22, 19): 'wall', (22, 20): 'dot_', (22, 21): 'wall', (22, 22): 'wall', (22, 23): 'wall', (22, 24): 'wall', (22, 25): 'wall', (22, 26): 'dot_', (22, 27): 'wall', (22, 28): 'wall', (22, 29): 'dot_', (22 , 30): 'wall', 
            (23, 0): 'wall', (23, 1): 'dot_', (23, 2): 'wall', (23, 3): 'wall', (23, 4): 'wall', (23, 5): 'dot_', (23, 6): 'wall', (23, 7): 'wall', (23, 8): 'dot_', (23, 9): 'wall', (23, 10): '____', (23, 11): '____', (23, 12): '____', (23, 13): 'wall', (23, 14): '____', (23, 15): 'wall', (23, 16): '____', (23, 17): '____', (23, 18): '____', (23, 19): 'wall', (23, 20): 'dot_', (23, 21): 'wall', (23, 22): 'wall', (23, 23): 'wall', (23, 24): 'wall', (23, 25): 'wall', (23, 26): 'dot_', (23, 27): 'wall', (23, 28): 'wall', (23, 29): 'dot_', (23 , 30): 'wall', 
            (24, 0): 'wall', (24, 1): 'dot_', (24, 2): 'wall', (24, 3): 'wall', (24, 4): 'wall', (24, 5): 'dot_', (24, 6): 'wall', (24, 7): 'wall', (24, 8): 'dot_', (24, 9): 'wall', (24, 10): '____', (24, 11): '____', (24, 12): '____', (24, 13): 'wall', (24, 14): '____', (24, 15): 'wall', (24, 16): '____', (24, 17): '____', (24, 18): '____', (24, 19): 'wall', (24, 20): 'dot_', (24, 21): 'wall', (24, 22): 'wall', (24, 23): 'dot_', (24, 24): 'dot_', (24, 25): 'dot_', (24, 26): 'dot_', (24, 27): 'wall', (24, 28): 'wall', (24, 29): 'dot_', (24 , 30): 'wall', 
            (25, 0): 'wall', (25, 1): 'dot_', (25, 2): 'wall', (25, 3): 'wall', (25, 4): 'wall', (25, 5): 'dot_', (25, 6): 'wall', (25, 7): 'wall', (25, 8): 'dot_', (25, 9): 'wall', (25, 10): '____', (25, 11): '____', (25, 12): '____', (25, 13): 'wall', (25, 14): '____', (25, 15): 'wall', (25, 16): '____', (25, 17): '____', (25, 18): '____', (25, 19): 'wall', (25, 20): 'dot_', (25, 21): 'wall', (25, 22): 'wall', (25, 23): 'dot_', (25, 24): 'wall', (25, 25): 'wall', (25, 26): 'dot_', (25, 27): 'wall', (25, 28): 'wall', (25, 29): 'dot_', (25 , 30): 'wall', 
            (26, 0): 'wall', (26, 1): 'dot_', (26, 2): 'dot_', (26, 3): 'pdot', (26, 4): 'dot_', (26, 5): 'dot_', (26, 6): 'dot_', (26, 7): 'dot_', (26, 8): 'dot_', (26, 9): 'wall', (26, 10): '____', (26, 11): '____', (26, 12): '____', (26, 13): 'wall', (26, 14): '____', (26, 15): 'wall', (26, 16): '____', (26, 17): '____', (26, 18): '____', (26, 19): 'wall', (26, 20): 'dot_', (26, 21): 'dot_', (26, 22): 'dot_', (26, 23): 'pdot', (26, 24): 'wall', (26, 25): 'wall', (26, 26): 'dot_', (26, 27): 'dot_', (26, 28): 'dot_', (26, 29): 'dot_', (26 , 30): 'wall', 
            (27, 0): 'wall', (27, 1): 'wall', (27, 2): 'wall', (27, 3): 'wall', (27, 4): 'wall', (27, 5): 'wall', (27, 6): 'wall', (27, 7): 'wall', (27, 8): 'wall', (27, 9): 'wall', (27, 10): '____', (27, 11): '____', (27, 12): '____', (27, 13): 'wall', (27, 14): '____', (27, 15): 'wall', (27, 16): '____', (27, 17): '____', (27, 18): '____', (27, 19): 'wall', (27, 20): 'wall', (27, 21): 'wall', (27, 22): 'wall', (27, 23): 'wall', (27, 24): 'wall', (27, 25): 'wall', (27, 26): 'wall', (27, 27): 'wall', (27, 28): 'wall', (27, 29): 'wall', (27 , 30): 'wall'
        }
    
    def get_high_score(self):
        '''Reads the latest high score from high_scores.txt'''
        
        with open("Pacman/high_scores.txt", 'r') as hs:
            high_scores = hs.readlines() # Read all scores
            if len(high_scores) > 0:
                return int(high_scores[-1]) # Latest high score
    
    def update_high_score(self, score):
        '''Updates the high score to high_scores.txt and keeps track of all previous high scores'''
        with open("Pacman/high_scores.txt", 'a') as hs:
            if score > self.get_high_score(): # If latest score is larger
                hs.write('\r' + str(score)) # Replace score
    
    def check_escape(self, score):
        '''Check if the escape key has been pressed so the user can exit the game'''
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.update_high_score(score)
            pygame.quit()
            exit()
    
    def menu(self):
        '''Basic properties of the menu'''
        
        self.screen.fill((0, 0, 0))  # Clear the screen with a black background
        
        pygame.draw.rect(self.screen, self.blue, self.outside_border, border_radius=15)
        pygame.draw.rect(self.screen, self.black, self.inside_border, border_radius=15)
        self.screen.blit(self.background, (250, 5))
    
    def start_menu(self, speed_pacman, speed_ghosts, speed_ghosts_frightened):
        '''The main function for the menu'''
        
        # doesn't use any of the speeds yet, but it will once I add the sequence with the ghosts chasing/getting chased by pacman later
        return
        # Set up the screen for the start menu
        screen.fill(black)
        
        # Font for text
        font = pygame.font.Font("Pacman/fonts/emulogic-font/Emulogic-zrEw.ttf", 36)
        smaller_font = pygame.font.Font("Pacman/fonts/emulogic-font/Emulogic-zrEw.ttf", 24)
        
        # WE NEED TO FIX THE SPRITES 
        # Estimated positions, labels, colors, and images for every ghost
        ghost_details = [
            [(30, 100), "SHADOW - \"BLINKY\"", (255,0,0), ghosts[0].sprites["move"]],  # Red ghost at (50, 100)
            [(30, 150), "SPEEDY - \"PINKY\"", (255,184,255), ghosts[1].sprites["move"]],  # Pink ghost at (50, 150)
            [(30, 200), "BASHFUL - \"INKY\"", (0,255,255), ghosts[2].sprites["move"]],  # Blue ghost at (50, 200)
            [(30, 250), "POKEY - \"CLYDE\"", (255,184,82), ghosts[3].sprites["move"]]  # Orange ghost at (50, 250)
        ]
        
        # scale the ghost images
        for num in range(len(ghost_details)):
            ghost_details[num][3] = pygame.transform.scale(ghost_details[num][3], (40,40))
        
        for num in range(len(ghost_details)):
            x, y = ghost_details[num][0][0], ghost_details[num][0][1]
            label, color, image = ghost_details[num][1], ghost_details[num][2], ghost_details[num][3]
            text = font.render(label, True, color)
            
            screen.blit(image, (top_right_x-640 + x, y)) # place the image at the position for that ghost
            screen.blit(text, (top_right_x-640 + x + 90, y))  # position text to the right of the ghost
        
        # Estimated positions for the pellet point values
        point_details = [
            ((250, 450), "10 PTS", dot_),  # "10 PTS" at (300, 350)
            ((250, 500), "50 PTS", pdot)   # "50 PTS" at (300, 400)
        ]

        for num in range(len(point_details)):
            x, y = point_details[num][0][0], point_details[num][0][1]
            label, image = point_details[num][1], point_details[num][2]
            text = smaller_font.render(label, True, (255, 255, 255))
            screen.blit(image, (top_right_x-640 + x, y))
            screen.blit(text, (top_right_x-640 + x + 90, y))
        

        # Update the display
        pygame.display.flip()

        #pygame.time.wait(3000) # wait 3 secs as a placeholder for the ghost animation at the start
    
    def find_cordinates(self, x,y):
        '''Converts pixel coordinates to grid coordinates'''
        
        px = (18 * x) + 250
        py = (18 * y) - 20
        return (px, py)
    
    def run_graph(self, grid, seconds):
        '''Displays the level and pellets'''
        
        for key in grid:
            x, y = key
            
            if key == (x, y):
                px, py = self.find_cordinates(key[0], key[1] + 4) # Add 4 tiles for top offset
                blink_rate = 6 # Blinks per second for the power pellets
                
                if grid[(x, y)] == 'dot_':
                    self.screen.blit(self.dot_,(px, py))
                if grid[(x, y)] == 'pdot' and int(seconds * blink_rate) % 2 == 0:
                    self.screen.blit(self.pdot,(px - 12, py - 12))
    
    def display(self, image, pos):
        '''Displays an image central to its position and relative to the grid with screen offsets'''
        
        # Offset values from the edge of the screen
        offset_x = 55
        offset_y = 60
        
        # Set x, y values. Converting from tile size to pixels, and centering the position of the image 
        image_pos_x = 800 - (pos.x * 18 + offset_x) - image.get_width() / 2
        image_pos_y = pos.y * 18 + offset_y - image.get_height() / 2
        self.screen.blit(image, (image_pos_x, image_pos_y)) # Display to screen
    
    def display_characters(self, pygame, pacman, ghosts, phase, seconds, ghost_killed=None):
        '''Displays ghosts and pacman'''
        
        # Display ghosts
        for ghost in ghosts:
            if ghost_killed == ghost.id: # Do not display the killed ghost
                continue
            image = ghost.change_animation(phase, seconds)
            self.display(image, ghost.pos)
            
        # Display pacman
        if not pacman.is_dead:
            pacman.rotate_sprite()
        if pacman.image != None:    
            self.display(pacman.image, pacman.pos) # Display pacman
    
    def display_fruit(self, fruit):
        '''Displays the fruit'''
        
        if fruit is not None and Fruit.is_active:
            self.display(fruit.image, fruit.pos)
        for x in range(Fruit.q.qsize()):
            q = Fruit.q.queue
            self.display(q[x], Position(x * 2 + 0.3, 31.6))
    
    def display_level(self, pacman, grid, seconds):
        '''Displays the background and checks for escape'''
        self.menu()
        self.check_escape(pacman.score)
        self.run_graph(grid, seconds)
    
    def draw(self, pygame, pacman, ghosts, phase, seconds, fruit, ghost_killed=None):
        '''Displays all entities'''
        
        # Scores
        for score in Score.l:
            self.display(score.image, score.pos)
        
        # Lives
        life = Pacman(0)
        life.image = pygame.transform.rotate(life.sprites["move"][1], 90)
        for x in range(pacman.lives):
            self.display(life.image, Position(26.75 - (x * 2 + 0.3), 31.6))
        
        self.display_fruit(fruit)
        self.display_characters(pygame, pacman, ghosts, phase, seconds, ghost_killed)
        self.display(self.abyss, Position(-1.5, 14))
        self.display(self.abyss, Position(28.4, 14))
        
        # Update pygame
        pygame.display.flip()
    
    def get_pellets(self, grid):
        '''Returns the number of pellets on the board'''
        
        sum = 0
        for i in grid.values(): # For each value
            if i == 'dot_': # If pellet
                sum += 1 # Add to sum
        return sum
    
    def update_pellets(self, pacman, grid, phase):
        '''Updates the phases and sounds associated with eating pellets'''
        
        # Pacman Eating Dots
        pos = pacman.pos.tile() # Centered position
        if 0 <= pos.x <= 27: # Check if indices are in range
            grid_value = grid[27 - pos.x, pos.y]
            
            if grid_value in ['dot_', 'pdot']: # If position is on any dot
                grid[27 - pos.x, pos.y] = '____' # Change dot into empty tile
                pacman.pause = True
                Sound.play_waka(True) # Play sound
                pacman.score += 10
            if grid_value == 'pdot':
                phase = 'f' # Change phase to frightened mode
                Ghost.scared_seconds = 0
                pacman.score += 40
        
        return phase
    
    def phase_switch(self, phase, phase_rotation):
        '''Switches the ghost phase from chase to scatter and back again'''
        
        if phase == 's':
            phase = 'c'
        elif phase == 'c':
            phase = 's'
            phase_rotation += 1
        return phase, phase_rotation
    
    def update_phase(self, values, ghosts, pacman, grid, fps):
        '''Updates the ghosts attributes according to each phase'''
        
        (phase, phase_rotation, level, phase_seconds) = values # Store in tuple for a pass by reference
        
        prev_phase = phase # Hold variable
        phase = self.update_pellets(pacman, grid, phase) # Check pellets
        
        if phase == 'f':
            if phase != prev_phase: # If phase has changed
                Ghosts.update_phase_attributes(ghosts, phase, prev_phase) # Update ghosts
                Ghost.flash = False
            
            time = Ghosts.scared_time(level)
            if Ghost.scared_seconds < 0.1: # When eating a new power pellet
                for ghost in ghosts:
                    ghost.override_frightened = False
                    Ghost.flash = False
            flash_length = 0.33
            for fi in range(1, 10):
                if abs(Ghost.scared_seconds - (time - flash_length * 10 + fi * flash_length)) < 1 / fps / 2:
                    Ghost.flash = not Ghost.flash # Toggle flash
            
            
            Ghost.scared_seconds += 1 / fps # Increment timer
            if Ghost.scared_seconds > time:
                prev_phase = 'f'
                phase = 'c'
                Ghost.scared_seconds = 0
                Ghost.consec_eaten = 0
                Ghosts.update_phase_attributes(ghosts, phase, prev_phase) # Update ghosts
        elif phase_rotation <= 4: # Only for 4 rotations 
            # Phase timer
            phase_seconds += 1 / fps # Increment timer
            if level == 1 and phase_seconds > self.phase_lengths[0][phase][phase_rotation]:
                phase, phase_rotation = self.phase_switch(phase, phase_rotation)
            elif level < 4 and phase_seconds > self.phase_lengths[1][phase][phase_rotation]:
                    phase, phase_rotation = self.phase_switch(phase, phase_rotation)
            elif phase_seconds > self.phase_lengths[2][phase][phase_rotation]: # Level 5+
                    phase, phase_rotation = self.phase_switch(phase, phase_rotation)
            if phase != prev_phase: # If the phase has changed
                phase_seconds = 0 # Reset seconds
                Ghosts.update_phase_attributes(ghosts, phase, prev_phase) # Update ghosts
        
        return (phase, phase_rotation, level, phase_seconds)
    
    def run(self, grid_original):
        # Beginning variables for the whole game
        fps = 60 # Frames per second
        level = 1
        do_wait = False
        
        pacman = Pacman(12.0 / fps) # Tiles per second / Frames per second = Tiles per frame
        speed_pacman = pacman.base_speed * 0.80
        speed_ghosts = speed_pacman * 0.80 # frightened ghosts are two-thirds of their normal speed
        self.start_menu(speed_pacman, speed_ghosts, speed_ghosts*2/3) 
        
        # Loop across each level
        running = True
        while running:
            # Variables for each level
            grid = copy.deepcopy(grid_original)
            pacman.lives = 3
            pellets = 244
            print("Level", level)
            
            # Change speeds based on level
            if level == 1:
                pacman.speed = pacman.base_speed * 0.80
                ghosts_speed = pacman.speed * 0.80 # 80 % - Level 1
            elif 2 <= level <= 4:
                ghosts_speed = pacman.speed * .90 # 90 % - Levels 2-4
            elif level <= 21:
                pacman.speed = pacman.base_speed
                ghosts_speed = pacman.speed # 100% - Levels 5+
            else:
                pacman.speed = pacman.base_speed * 0.90 # levels 21+
            
            # Loop across each life
            prev_level = level
            while pacman.lives > 0 and prev_level == level: # Break when pacman either dies or advances a level         
                # Variables for each life
                phase = 's' # Begin in scatter mode
                next_move = None
                seconds = phase_seconds = phase_rotation = 0
                fruit = Fruit(level)
                Fruit.is_active = False
                Ghost.consec_eaten = 0
                ghosts = [
                    Ghost('r', ghosts_speed),
                    Ghost('p', ghosts_speed),
                    Ghost('b', ghosts_speed),
                    Ghost('o', ghosts_speed)
                ]
                
                # Wait to start level
                if do_wait:
                    while seconds < 1:
                        self.display_level(pacman, grid, seconds)
                        self.draw(pygame, pacman, ghosts, phase, seconds, fruit)
                        self.clock.tick(fps)
                        seconds += 1 / fps
                
                # Run
                seconds = 0
                prev_lives = pacman.lives
                while prev_lives == pacman.lives: # Break when pacman loses a life
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    self.display_level(pacman, grid, seconds)
                    self.clock.tick(fps) # Cap the frame rate
                    
                    # Update character data
                    next_move = pacman.control_pacman(next_move, grid) # Direction controls
                    pacman.update_pacman(grid)
                    ghost_killed = Ghosts.update_ghosts(ghosts, pacman, level, grid, phase, fps, seconds, pellets)
                    update_fruit(fruit, pacman, pellets, fps, level)
                    Score.update_scores(fps)
                    
                    # Pause for killed ghost
                    if ghost_killed is not None and do_wait:
                        killed_seconds = 0
                        while killed_seconds < 0.5:
                            self.display_level(pacman, grid, seconds)
                            pacman.change_animation()
                            self.draw(pygame, pacman, ghosts, phase, seconds, fruit, ghost_killed)
                            self.clock.tick(fps)
                            killed_seconds += 1 / fps
                    
                    # Update board
                    seconds += 1 / fps # Increment timer
                    phase_values = self.update_phase((phase, phase_rotation, level, phase_seconds), ghosts, pacman, grid, fps)
                    phase, phase_rotation, level, phase_seconds = phase_values
                    pellets = self.get_pellets(grid)
                    if pellets == 0:
                        level += 1 # Increment level
                        print("Level Complete!")
                        break
                    
                    # Extra life check
                    if pacman.score // 10000 > pacman.extra_lives: # Every 10,000 points is a life
                        if pacman.lives < 5:
                            pacman.lives += 1
                            prev_lives = pacman.lives
                        pacman.extra_lives += 1
                    
                    # Update display
                    self.draw(pygame, pacman, ghosts, phase, seconds, fruit)
                    print("Score:", pacman.score)
                
                # End of life
                if do_wait:
                    seconds = 0
                    while seconds < 2:
                        self.display_level(pacman, grid, seconds)
                        pacman.change_animation()
                        self.draw(pygame, pacman, ghosts, phase, seconds, fruit)
                        self.clock.tick(7)
                        seconds += 1 / 7
                
                pacman.respawn()
        
        self.update_high_score(pacman.score)
        pygame.quit()
    

# __main__(grid)
PacMan = PacManGame()
PacMan.run(PacMan.grid)