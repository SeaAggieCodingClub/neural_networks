import pygame

pygame.init()

# Create a display surface
width = 800
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
# delete above later

snake_speed = 20

green = (0, 255, 0)

def movement_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])
"""Wait for the screen"""
