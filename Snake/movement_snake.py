import pygame

pygame.init()

cell_number = 40
cell_size = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

snake_speed = 20
snake_head = pygame.image.load('Snake/snake head.png').convert()
white = pygame.color.Color('#FFFFFF')

snake_x = 20
snake_y = 20
finished = False

while not finished:
    screen.fill(white)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake_y -= 1
    if keys[pygame.K_DOWN]:
            snake_y += 1
    if keys[pygame.K_LEFT]:
            snake_x -= 1
    if keys[pygame.K_RIGHT]:
         snake_x += 1
    screen.blit(snake_head, (snake_x,snake_y))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            finished = True
pygame.quit()
