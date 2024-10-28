import pygame
import time
import os
import random




pygame.init()



# Get the screen resolution
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Calculate position for the window to be centered at the top-right
window_width, window_height = 640, 480
top_right_x = screen_width - window_width - 175
top_right_y = 0

# Set environment variable for window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{top_right_x},{top_right_y}"


# Do not change this so they will be consistent between games and able to keep room for the Neural Network window
width = 800
height = 650

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption('Snake')



air = pygame.image.load("Pacman/images/dot.png")


# Set clock speed
clock = pygame.time.Clock()

# Color definitions
black = (10, 10, 10)  # Changed to white color for clarity
blue = (32,36,221)

# Menu variables
outside_border = pygame.Rect(10, 15, 200, height - 30)
inside_border = pygame.Rect(15, 20, 190, height - 40)





grid = {(x, y): 'dot' for x in range(28) for y in range(36)}

grid = {
    (0, 0): 'dot', (0, 1): 'dot', (0, 2): 'dot', (0, 3): 'dot', (0, 4): 'dot', (0, 5): 'dot', (0, 6): 'dot', (0, 7): 'dot', (0, 8): 'dot', (0, 9): 'dot', (0, 10): 'dot', (0, 11): 'dot', (0, 12): 'dot', (0, 13): 'dot', (0, 14): 'dot', (0, 15): 'dot',(0, 16): 'dot', (0, 17): 'dot', (0, 18): 'dot', (0, 19): 'dot', (0, 20): 'dot', (0, 21): 'dot', (0, 22): 'dot', (0, 23): 'dot',(0, 24): 'dot', (0, 25): 'dot', (0, 26): 'dot', (0, 27): 'dot', (0, 28): 'dot', (0, 29): 'dot', (0, 30): 'dot', (0, 31): 'dot',(0, 32): 'dot', (0, 33): 'dot', (0, 34): 'dot', (0, 35): 'dot',
    (1, 0): 'dot', (1, 1): 'dot', (1, 2): 'dot', (1, 3): 'dot', (1, 4): 'dot', (1, 5): 'dot', (1, 6): 'dot', (1, 7): 'dot',(1, 8): 'dot', (1, 9): 'dot', (1, 10): 'dot', (1, 11): 'dot', (1, 12): 'dot', (1, 13): 'dot', (1, 14): 'dot', (1, 15): 'dot',(1, 16): 'dot', (1, 17): 'dot', (1, 18): 'dot', (1, 19): 'dot', (1, 20): 'dot', (1, 21): 'dot', (1, 22): 'dot', (1, 23): 'dot',
    (1, 24): 'dot', (1, 25): 'dot', (1, 26): 'dot', (1, 27): 'dot', (1, 28): 'dot', (1, 29): 'dot', (1, 30): 'dot', (1, 31): 'dot',(1, 32): 'dot', (1, 33): 'dot', (1, 34): 'dot', (1, 35): 'dot',
    (2, 0): 'dot', (2, 1): 'dot', (2, 2): 'dot', (2, 3): 'dot', (2, 4): 'dot', (2, 5): 'dot', (2, 6): 'dot', (2, 7): 'dot',(2, 8): 'dot', (2, 9): 'dot', (2, 10): 'dot', (2, 11): 'dot', (2, 12): 'dot', (2, 13): 'dot', (2, 14): 'dot', (2, 15): 'dot',(2, 16): 'dot', (2, 17): 'dot', (2, 18): 'dot', (2, 19): 'dot', (2, 20): 'dot', (2, 21): 'dot', (2, 22): 'dot', (2, 23): 'dot',(2, 24): 'dot', (2, 25): 'dot', (2, 26): 'dot', (2, 27): 'dot', (2, 28): 'dot', (2, 29): 'dot', (2, 30): 'dot', (2, 31): 'dot',(2, 32): 'dot', (2, 33): 'dot', (2, 34): 'dot', (2, 35): 'dot',
    # ... (Continue this pattern until you reach the final row)
    (27, 0): 'dot', (27, 1): 'dot', (27, 2): 'dot', (27, 3): 'dot', (27, 4): 'dot', (27, 5): 'dot', (27, 6): 'dot', (27, 7): 'dot',
    (27, 8): 'dot', (27, 9): 'dot', (27, 10): 'dot', (27, 11): 'dot', (27, 12): 'dot', (27, 13): 'dot', (27, 14): 'dot', (27, 15): 'dot',
    (27, 16): 'dot', (27, 17): 'dot', (27, 18): 'dot', (27, 19): 'dot', (27, 20): 'dot', (27, 21): 'dot', (27, 22): 'dot', (27, 23): 'dot',
    (27, 24): 'dot', (27, 25): 'dot', (27, 26): 'dot', (27, 27): 'dot', (27, 28): 'dot', (27, 29): 'dot', (27, 30): 'dot', (27, 31): 'dot',
    (27, 32): 'dot', (27, 33): 'dot', (27, 34): 'dot', (27, 35): 'dot'
}






def check_escape():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()


def menu():
    screen.fill((0, 0, 0))  # Clear the screen with a black background
    
    pygame.draw.rect(screen, blue, outside_border, border_radius=20)
    pygame.draw.rect(screen, black, inside_border, border_radius=20)
    


def find_cordinates(x,y):
      px = (18*x) + 240
      py = (18*y)+ 0
      return px,py


def run_graph(level):
      for key in level:
            x,y = key
            
            if key == (x,y):
                px,py = find_cordinates(key[0],key[1])
                if level[(x,y)] == 'dot':
                    screen.blit(air,(px,py))


def __main__():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw menu and check for escape
        menu()
        check_escape()
        run_graph(grid)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)  # Adjust as necessary for smoothness

    pygame.quit()


__main__()