import pygame
import sys

pygame.init()

cell_number = 40
cell_size = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size


screen = pygame.display.set_mode((screen_width, screen_height))

snake_speed = 20
snake_head_image = pygame.image.load('Snake/snake head.png').convert()
snake_head_image = pygame.transform.scale(snake_head_image, (25,25))  # Resize image to 20x20 pixels more or less
snake_head = snake_head_image

white = pygame.color.Color('#FFFFFF')
black = pygame.color.Color('#000000')


snake_body = [(20, 20)]  # Initial position
direction = (1, 0)       # Initial direction (moving right)
finished = False

clock = pygame.time.Clock()

direction_of_snake ={ 
    (1,0):270,
    (0,1):180,
    (-1,0):90,
    (0,-1):0,
    }
'''
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, black)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Show the message for 2 seconds
    pygame.quit()
    sys.exit()
'''
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
    angle = direction_of_snake[direction]
    snake_head = pygame.transform.rotate(snake_head_image, angle)

    # Update snake position
    new_head = (snake_body[0][0] + direction[0] * cell_size, snake_body[0][1] + direction[1] * cell_size)
    if (new_head[0] < 0 or new_head[0] >= screen_width or
        new_head[1] < 0 or new_head[1] >= screen_height):
        #game_over()
        finished = True
    snake_body = [new_head] + snake_body[:-1]  # Add new head and remove last segment

    screen.blit(snake_head, snake_body[0])  # Draw rotated head
    for segment in snake_body[1:]:  # Draw the rest of the body without rotation
        screen.blit(snake_head_image, segment)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
