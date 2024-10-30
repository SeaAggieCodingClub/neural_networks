import pygame
import time
import random
from sys import exit


pygame.init()

cell_number = 40
cell_size = 20

# Window resolution
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
main_font = pygame.font.SysFont("Arial", 30)

snake_speed = 20
snake_head = pygame.image.load('Snake/snake head.png').convert()
green = (0, 255, 0)

#def movement_snake(snake_block, snake_list):
#    for x in snake_list:
#        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if (position[0] in range(self.rect.left, self.rect.right)) and (position[1] in range(self.rect.top, self.rect.bottom)):
            print("Button pressed")

    def change_color(self, position):
        if (position[0] in range(self.rect.left, self.rect.right)) and (position[1] in range(self.rect.top, self.rect.bottom)):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")

# Button variables
button_surface = pygame.image.load("Snake/basic_button.png").convert()
button_surface = pygame.transform.scale(button_surface, (300, 100))

play_button = Button(button_surface, 400, 300, "Play")

# Main menu screen
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_button.check_for_input(pygame.mouse.get_pos())

        pygame.display.update()
        screen.fill("white")

        play_button.update()
        play_button.change_color(pygame.mouse.get_pos())

        clock.tick(60)



# Play screen
def play():
    while True:
        # Checks if the window is closed then terminates the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw all elements
        pygame.display.update()
        screen.fill((172, 206, 96))
        

        # Frame rate
        clock.tick(60)

play()



