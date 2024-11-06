import pygame
import time
import sys
from button import Button

pygame.init()

cell_number = 40
cell_size = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size


# Window resolution
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont("Arial", 26)
back_font = pygame.font.SysFont("Arial", 20)

# Button variables
button_surface = pygame.image.load("Snake/basic_button.png").convert()
button_surface = pygame.transform.scale(button_surface, (235, 55))
back_button_surface = pygame.image.load("Snake/basic_button.png").convert()
back_button_surface = pygame.transform.scale(back_button_surface, (100, 40))

#snake picture
snake_speed = 20
snake_head_image = pygame.image.load('Snake/snake head.png').convert_alpha()
snake_head_image = pygame.transform.scale(snake_head_image, (40,40))  # Resize image to 20x20 pixels more or less
snake_head = snake_head_image
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


# Play screen
def play():
    global direction

    snake_body = [(20, 20)]  # Initial position
    direction = (1, 0)

    while True:
        screen.fill((172, 206, 96))

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

        pygame.display.update()
        
        # Frame rate
        clock.tick(10)

main_menu()



