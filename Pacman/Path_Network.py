import sys
from Position import Position
import numpy as np

grid = {
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
    (27, 0): 'wall', (27, 1): 'wall', (27, 2): 'wall', (27, 3): 'wall', (27, 4): 'wall', (27, 5): 'wall', (27, 6): 'wall', (27, 7): 'wall', (27, 8): 'wall', (27, 9): 'wall', (27, 10): '____', (27, 11): '____', (27, 12): '____', (27, 13): 'wall', (27, 14): '____', (27, 15): 'wall', (27, 16): '____', (27, 17): '____', (27, 18): '____', (27, 19): 'wall', (27, 20): 'wall', (27, 21): 'wall', (27, 22): 'wall', (27, 23): 'wall', (27, 24): 'wall', (27, 25): 'wall', (27, 26): 'wall', (27, 27): 'wall', (27, 28): 'wall', (27, 29): 'wall', (27 , 30): 'wall',
}

class Node(Position):    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nexts = {}
    
    def connect(self, nodes, grid, decision_tiles):
        '''Connect nodes by searching the nearest cardinal x, y values'''
        x, y = self.tile().to_tuple()
        
        for dir in [1, -1]:
            # Shifting x values
            new_pos = Position(x + dir, y)
            if 1 <= new_pos.x <= 26 and grid[new_pos.to_tuple()] != 'wall': # If valid relative to position
                y_list = []
                x_val = x
                
                # Search x values
                while 1 <= x_val <= 27:
                    x_val += dir # Update variables
                    
                    if x_val in decision_tiles and y in decision_tiles[x_val]: # Check for nodes with the same y value
                        y_list = nodes[x_val]
                        break
                
                # Store node
                if y in [node.y for node in y_list]:
                    next = [n for n in y_list if n.y == y][0] # Lookup node with position
                    self.nexts[next] = self.manhattan(next) # Add to nexts
            
            # Shifting y values
            new_pos = Position(x, y + dir)
            if x in decision_tiles and 0 <= new_pos.y <= 30 and grid[new_pos.to_tuple()] != 'wall': # If valid relative to position
                y_list = decision_tiles[x] # Y values containing the node
                y_val = y
                
                while 0 <= y_val <= 30: # If not found
                    y_val += dir # Move to the nearest node
                    if y_val in y_list: # If found a node
                        y_index = y_list.index(y_val) # Find the index
                        break
                
                next = nodes[x][y_index] # Lookup node with position
                self.nexts[next] = self.manhattan(next) # Add to nexts
    
    def nearest_n(self, nodes, number=1):
        distances = [self.manhattan(node) for node in nodes] # Get euclidean distances between all point
        nearest_nodes = {}
        for _ in range(number):
            nearest_index = np.argmin(distances) # Find the nearest in the list
            nearest_nodes[nodes[nearest_index]] = distances[nearest_index] # Store nearest
            # print(distances[nearest_index], nodes[nearest_index].to_tuple(), [node.to_tuple() for node in nearest_nodes])
            # print(distances)
            distances[nearest_index] = 500 # Remove distance from selection by setting to large number
        self.nexts.update(nearest_nodes) # One-way connect to the nearest 2 nodes
        return nearest_nodes
    
    '''def nearest_to_target(self, target):
        min = 500
        nearest = None
        
        sorted(self.nexts, key=lambda n: n.manhattan(target))
        
        for next in self.nexts: # Get euclidean distances between all point
            distance = target.manhattan(next)
            if distance < min:
                min = distance
                nearest = next
        return nearest'''

class Path_Network():
    nodes = []
    
    def __init__(self, grid, run_from_config=False):
        # Structure of intersection points which will determine node positions
        self.decision_tiles = { # Tiles in which there is an intersection (X val : [Y vals])
            1: [1, 5, 8,             20, 23, 26, 29],
            3: [                         23, 26],
            6: [1, 5, 8,     14,     20, 23, 26],
            9: [   5, 8, 11, 14, 17, 20, 23, 26],
            12:[1, 5, 8, 11,         20, 23, 26, 29],
            15:[1, 5, 8, 11,         20, 23, 26, 29],
            18:[   5, 8, 11, 14, 17, 20, 23, 26],
            21:[1, 5, 8,     14,     20, 23, 26],
            24:[                         23, 26],
            26:[1, 5, 8,             20, 23, 26, 29]
        }
        
        # Populate nodes list
        nodes = {}
        for x, y_list in self.decision_tiles.items(): # For each x key in the dictionary
            nodes[x] = [] # Add new list
            for y in y_list: # For each y value
                nodes[x] += [Node(x, y)] # Retain list structure
        
        # Connect the nodes along warp tunnels
        self.warp1 = nodes[21][3] # 3 is the index of 14, the y position
        self.warp2 = nodes[6][3]
        self.warp1.nexts[self.warp2] = 13
        self.warp2.nexts[self.warp1] = 13
        
        # Flatten
        flattened_nodes = []
        for node_list in nodes.values():
            flattened_nodes += node_list
        
        # Save the nodes
        self.nodes = nodes
        self.flattened_nodes = flattened_nodes
        self.node_keys = {node.to_tuple(): i for i, node in enumerate(flattened_nodes)}
        self.grid = grid
        
        # Load from file if specified
        if run_from_config:
            self.matrix = np.load('neural_networks/Pacman/path_network.npy')
            return
        
        # Connect direct neighbors
        for node in flattened_nodes:
            node.connect(nodes, grid, self.decision_tiles)
            
            # if node.x in [1, 26] and node.y <= 8:
            #     print("Node:", node.to_tuple())
            #     if len(node.nexts) == 0:
            #         print('   ',  "None")
            #     for next in node.nexts:
            #         print('   ', next.to_tuple())
        
        # Initialize network matrix
        num_nodes = len(flattened_nodes)
        self.matrix = np.zeros((num_nodes, num_nodes))
        for node in flattened_nodes:
            for next, dist in node.nexts.items():
                self.matrix[self.node_keys[node.to_tuple()]][self.node_keys[next.to_tuple()]] = dist
        
        # Fully connect network 
        for node in flattened_nodes:
            self.traverse(node, [])
        
        # Save the matrix
        np.save('neural_networks/Pacman/path_network.npy', self.matrix)
        np.set_printoptions(threshold=np.inf)
        print(self.matrix)
    
    def update_matrix(self, origin, next, new_dist):
        '''Fills the matrix only if the distance is shorter'''
        if next == origin:
            return
        curr_dist = self.matrix[self.node_keys[origin.to_tuple()]][self.node_keys[next.to_tuple()]] # Get the current distance
        if (curr_dist == 0 or new_dist < curr_dist): # If the new distance is shorter
            self.matrix[self.node_keys[origin.to_tuple()]][self.node_keys[next.to_tuple()]] = new_dist # Update distance
    
    def traverse(self, node, prevs, prev=None, dist_origin=0, depth=0):
        '''Recursively runs through each node, keeping track of the distance
        between them and the origin, updating to keep the shortest distance'''
        
        # Update prevs
        prevs += [node] # Add node before current to prevs list
        
        # Check each neighbor
        for next, dist_next in node.nexts.items():            
            # Calculate new distance from the origin
            new_dist = dist_origin + dist_next
            
            # Check if it has previously been traversed; found already
            self.update_matrix(prevs[0], next, new_dist)
            
            # Check for previous nodes
            if next in prevs or next == prev: # Is in list of previous nodes
                continue
            
            # Traverse the next nodes
            self.traverse(next, prevs.copy(), node, new_dist, depth+1)
    
    def manhattan(self, current, target):
        '''Returns the shortest distance through the maze between two points'''
        
        # Convert Positions to Nodes
        c_x, c_y = current.to_tuple()
        t_x, t_y = target.to_tuple()
        current_node = Node(c_x, c_y)
        target_node = Node(t_x, t_y)
        
        # Connect nodes to network
        for node in [current_node, target_node]:
            node.connect(self.nodes, self.grid, self.decision_tiles)
            
            # Correct position for warp tunnels
            in_warp_tunnel = False
            if node.y == 14:
                if node.x < 5.9: # If position is in the warp tunnels
                    # Connect to warp tunnel nodes
                    node.nexts[self.warp2] = node.manhattan(self.warp2)
                    node.nexts[self.warp1] = node.manhattan(Position(self.warp1.x - 29, self.warp1.y))
                    in_warp_tunnel = True
                elif node.x > 21.1:
                    # Connect to warp tunnel nodes
                    node.nexts[self.warp2] = node.manhattan(Position(self.warp2.x + 29, self.warp2.y))
                    node.nexts[self.warp1] = node.manhattan(self.warp1)
                    in_warp_tunnel = True
            
            # # Check if node already exists in network
            if node.x in self.decision_tiles and node.y in self.decision_tiles[node.x]:
                node.nexts[node] = 0
        
        # print([(node.to_tuple(), dist) for node, dist in current_node.nexts.items()])
        
        dists = []
        for i in current_node.nexts:
            for j in target_node.nexts:
                if not in_warp_tunnel and i == j: # If they have a mutual neighbor
                    return current_node.manhattan(target_node) # Return manhattan distance
                
                dist_neighbors = self.matrix[self.node_keys[i.to_tuple()]][self.node_keys[j.to_tuple()]] # Get the distance from the matrix
                dists += [dist_neighbors + current_node.nexts[i] + target_node.nexts[j]]
        
        return int(min(dists) if len(dists) > 0 else 100)

# pacman = Node(21, 15)
# target = Node(14, 29)
# network = Path_Network(grid, 0)
# np.set_printoptions(threshold=np.inf)
# print(network.matrix)
# print('Done')
# print(network.manhattan(pacman, target))