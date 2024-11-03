import pygame
import time
import random
from sys import exit
from button import Button

pygame.init()

cell_number = 40
cell_size = 20

# Window resolution
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont("Arial", 26)

# Button variables
button_surface = pygame.image.load("Snake/basic_button.png").convert()
button_surface = pygame.transform.scale(button_surface, (235, 55))

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
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if exit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(60)

# Options screen
def options():
    print("Options screen")


# Play screen
def play():
    while True:
        for event in pygame.event.get():
            # Checks if the window is closed then terminates the program
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Checks if escape key is pressed then opens the menu screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        # Draw all elements
        pygame.display.update()
        screen.fill((172, 206, 96))
        
        # Frame rate
        clock.tick(60)

main_menu()



