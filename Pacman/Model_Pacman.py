import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man')

# Set up clock
clock = pygame.time.Clock()

# Pac-Man settings
pacman_size = 40
pacman_x = SCREEN_WIDTH // 2
pacman_y = SCREEN_HEIGHT // 2
pacman_speed = 5
pacman_direction = 'STOP'

# Food settings
food_size = 10
food_x = random.randint(0, SCREEN_WIDTH - food_size)
food_y = random.randint(0, SCREEN_HEIGHT - food_size)

# Function to draw Pac-Man
def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), pacman_size // 2)

# Function to draw food
def draw_food(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, food_size, food_size])

# Game loop
def game_loop():
    global pacman_x, pacman_y, pacman_direction, food_x, food_y

    running = True
    score = 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    pacman_direction = 'RIGHT'
                elif event.key == pygame.K_UP:
                    pacman_direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    pacman_direction = 'DOWN'

        # Pac-Man movement
        if pacman_direction == 'LEFT':
            pacman_x -= pacman_speed
        elif pacman_direction == 'RIGHT':
            pacman_x += pacman_speed
        elif pacman_direction == 'UP':
            pacman_y -= pacman_speed
        elif pacman_direction == 'DOWN':
            pacman_y += pacman_speed

        # Boundary conditions for Pac-Man
        if pacman_x < 0:
            pacman_x = SCREEN_WIDTH
        elif pacman_x > SCREEN_WIDTH:
            pacman_x = 0
        if pacman_y < 0:
            pacman_y = SCREEN_HEIGHT
        elif pacman_y > SCREEN_HEIGHT:
            pacman_y = 0

        # Check for collision between Pac-Man and food
        if (pacman_x - pacman_size // 2 < food_x < pacman_x + pacman_size // 2 and
            pacman_y - pacman_size // 2 < food_y < pacman_y + pacman_size // 2):
            score += 1
            food_x = random.randint(0, SCREEN_WIDTH - food_size)
            food_y = random.randint(0, SCREEN_HEIGHT - food_size)

        # Draw Pac-Man and food
        draw_pacman(pacman_x, pacman_y)
        draw_food(food_x, food_y)

        # Display the score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])

        # Update the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

    pygame.quit()
    quit()

# Start the game
game_loop()
