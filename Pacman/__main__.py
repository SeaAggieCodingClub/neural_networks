import pygame
import time
import random


pygame.init()

# Do not change this so they will be consistant between games and able to keep room for the Nueral Network window
width = 800
height = 650


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

# Set clock speed
clock = pygame.time.Clock()

#other functions here