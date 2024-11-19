import pygame
import time
import sys
import random
from button import Button
from pygame.math import Vector2

class MAIN:
    def __init__(self):
        self.fruit = FRUIT()

    def update(self):
        self.draw_elements()
        self.check_collision()

    def draw_elements(self):
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.coords == snake_body[0]:
            self.fruit.randomize()
            # Add block to snake
    
class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        '''
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)  #fix later if needed
        '''
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size + cell_size / 4),
            int(self.pos.y * cell_size + cell_size / 4),
            cell_size // 2,
            cell_size // 2
        )
        screen.blit(apple, fruit_rect)

    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

pygame.init()

cell_number = 40
cell_size = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size

# Window resolution
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
apple = pygame.image.load("Snake/apple.png").convert_alpha()
main_font = pygame.font.SysFont("Arial", 26)
back_font = pygame.font.SysFont("Arial", 20)

main_game = MAIN()

# Button variables
button_surface = pygame.image.load("Snake/images/basic_button.png").convert()
button_surface = pygame.transform.scale(button_surface, (235, 55))
back_button_surface = pygame.image.load("Snake/images/basic_button.png").convert()
back_button_surface = pygame.transform.scale(back_button_surface, (100, 40))

snake_speed = 20 # speed of snake

#snake head and body
snake_head_image = pygame.image.load('Snake/images/snake head.png').convert_alpha()
snake_head_image = pygame.transform.scale(snake_head_image, (45,45))  # Resize image to 45x45 pixels more or less
snake_head = snake_head_image
snake_body_image = pygame.image.load('Snake/images/snake_body.png').convert_alpha()
snake_body_image = pygame.transform.scale(snake_body_image,(45,25)) # accurately same size as head
snake_body = snake_body_image
#snake position
snake_body = [(20, 20)]  # Initial position
direction = (1, 0)       # Initial direction (moving right)
finished = False
#direction
direction_of_snake ={ 
    (1,0):270,
    (0,1):180,
    (-1,0):90,
    (0,-1):0,
    }

# Main menu screen
def main_menu():
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        play_button = Button(button_surface, 400, 300, "Play", main_font, "white", "green")
        options_button = Button(button_surface, 400, 370, "Options", main_font, "white", "green")
        exit_button = Button(button_surface, 400, 440, "Exit", main_font, "white", "green")

        for button in [play_button, options_button, exit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if exit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

# Options screen
def options():
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        setting_button = Button(button_surface, 400, 300, "Example", main_font, "white", "green")
        back_button = Button(back_button_surface, 60, 30, "Back", back_font, "white", "green")

        for button in [setting_button, back_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setting_button.check_for_input(menu_mouse_pos):
                    print("Setting")
                if back_button.check_for_input(menu_mouse_pos):
                    main_menu()

        pygame.display.update()
        clock.tick(60)
def create_grid(cell_number):
    grid = {}
    for x in range(cell_number):
        for y in range(cell_number):
            grid[(x, y)] = "empty"
    return grid
grid = create_grid(cell_number)

def update_grid(grid, snake_body, apple_pos):
    # Reset the grid
    for key in grid:
        grid[key] = "empty"
    grid[(int(apple_pos.x), int(apple_pos.y))] = "apple"
    for i, segment in enumerate(snake_body):
        if i == 0:
            grid[(segment[0] // cell_size, segment[1] // cell_size)] = "snake_head"
        else:
            grid[(segment[0] // cell_size, segment[1] // cell_size)] = "snake_body"

def draw_grid(grid):
    for (x, y), value in grid.items():
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        if value == "apple":
            screen.blit(apple, rect)
        elif value == "snake_head":
            screen.blit(snake_head_image, rect)
        elif value == "snake_body":
            screen.blit(snake_body_image, rect)
        else:  # Draw grid lines for better visibility
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)



# Play screen
def play():
    global direction

    snake_body = [(100, 350)]  # Initial position
    snake_directions = [direction]
    direction = (1, 0)
    apple_pos = main_game.fruit.pos

    while True:
        #screen.fill((172, 206, 96)) #can be fixed later if messed up
        screen.fill((0,0,0))

        for event in pygame.event.get():
            # Checks if the window is closed then terminates the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks if escape key is pressed then opens the menu screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return #return to main menu
                elif event.key == pygame.K_UP and direction != (0, 1):  # Prevent moving back on itself
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
        '''           just in case if we need it
        angle = direction_of_snake[direction] 
        snake_head = pygame.transform.rotate(snake_head_image, angle)

        # Update snake position
        new_head = (snake_body[0][0] + direction[0] * cell_size, snake_body[0][1] + direction[1] * cell_size)
        if (new_head[0] < 0 or new_head[0] >= screen_width or
            new_head[1] < 0 or new_head[1] >= screen_height):
            break
        snake_body = [new_head] + snake_body[:-1]  # Add new head and remove last segment


        screen.blit(snake_head, snake_body[0])  # Draw rotated head
        for segment in snake_body[1:]:  # Draw the rest of the body without rotation
            screen.blit(snake_head_image, segment)
            pygame.draw.rect(screen, (0, 255, 0), (*segment, cell_size, cell_size))
        
        main_game.draw_elements() #can be fixed later if messed up
        '''
        new_head = (snake_body[0][0] + direction[0] * cell_size, snake_body[0][1] + direction[1] * cell_size)
        if (new_head[0] < 0 or new_head[0] >= screen_width or
            new_head[1] < 0 or new_head[1] >= screen_height):
            break

        #check for collisions
        if (new_head[0] // cell_size, new_head[1] // cell_size) in [
            (segment[0] // cell_size, segment[1] // cell_size) for segment in snake_body[1:]]:
            break

        # Check for apple collision
        if new_head[0] // cell_size == apple_pos.x and new_head[1] // cell_size == apple_pos.y:
            snake_body.append(snake_body[-1])  # Grow the snake
            snake_directions.append(snake_directions[-1])
            main_game.fruit.randomize()  # Move the apple
            apple_pos = main_game.fruit.pos
        else:
            # Move the snake: new head, followed by all other segments
            snake_body = [new_head] + snake_body[:-1]
            snake_directions = [direction] + snake_directions[:-1]

        # Draw the snake
        for i, segment in enumerate(snake_body):
            if i == 0:  # Head
                angle = direction_of_snake[snake_directions[i]]
                snake_head_rotated = pygame.transform.rotate(snake_head_image, angle)
                screen.blit(snake_head_rotated, segment)
            else:  # Body
                angle = direction_of_snake[snake_directions[i]]
                snake_body_rotated = pygame.transform.rotate(snake_body_image,angle)
                screen.blit(snake_body_rotated, segment)

        # Draw the apple
        main_game.draw_elements()

        pygame.display.update()
        
        # Frame rate
        clock.tick(10)

main_menu()



