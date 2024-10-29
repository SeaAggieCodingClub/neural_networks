import pygame as py # make typing easier 
import time
import random
from sys import exit 




width = 800
height = 650

screen = py.display.set_mode((width, height))
py.display.set_caption('Snake')

# Set clock speed
clock = py.time.Clock()

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
    py.display.update
    clock.tick(60)
