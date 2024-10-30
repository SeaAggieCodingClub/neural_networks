import pygame

pygame.init()


snake_speed = 20
snake_head = pygame.image.load('Snake/snake head.png').convert()
green = (0, 255, 0)
snake_x = 20
snake_y = 20
finished = False
while not finished:
    keys = pygame.key.get_pressed
    if keys[pygame.K_up]:
        snake_y -= 1


#def movement_snake(snake_block, snake_list):
#    for x in snake_list:
#        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])