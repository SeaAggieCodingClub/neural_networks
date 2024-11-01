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

clock = pygame.time.Clock()
direction_x = 0
direction_y = 0

while not finished:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction_x, direction_y = 0, -snake_speed
            elif event.key == pygame.K_UP:
                direction_x, direction_y = 0, -snake_speed
            elif event.key == pygame.K_UP:
                direction_x, direction_y = -snake_speed, 0
            elif event.key == pygame.K_UP:
                direction_x, direction_y = snake_speed, 0

    snake_x += direction_x
    snake_y += direction_y
    screen.blit(snake_head, (snake_x,snake_y))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    clock.tick(10)
pygame.quit()
