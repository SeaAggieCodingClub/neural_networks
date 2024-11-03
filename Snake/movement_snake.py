import pygame

pygame.init()

cell_number = 40
cell_size = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

snake_speed = 20
snake_head = pygame.image.load('Snake/snake head.png').convert()
snake_head = pygame.transform.scale(snake_head, (20,20))  # Resize image to 20x20 pixels

white = pygame.color.Color('#FFFFFF')

snake_body = [(20, 20)]  # Initial position
direction = (1, 0)       # Initial direction (moving right)
snake_speed = 1
finished = False

clock = pygame.time.Clock()


while not finished:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):  # Prevent moving back on itself
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Update snake position
    new_head = (snake_body[0][0] + direction[0] * cell_size, snake_body[0][1] + direction[1] * cell_size)
    snake_body = [new_head] + snake_body[:-1]  # Add new head and remove last segment

    for segment in snake_body:
        screen.blit(snake_head, segment)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    clock.tick(10)
pygame.quit()
