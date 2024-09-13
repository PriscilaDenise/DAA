import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
player_health = 100
player_hunger = 100
wood = 0
stone = 0
day_time = 0  # Day/Night cycle
day_length = 6000  # Frames before night
is_night = False

# Player setup
player_pos = [400, 300]
player_speed = 5

# Resource objects (trees and rocks)
class Resource:
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.rect = pygame.Rect(x, y, 40, 40)

# Create initial resources
trees = [Resource(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 40), "tree") for _ in range(10)]
rocks = [Resource(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 40), "rock") for _ in range(10)]

# Functions to display text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to handle resource collection
def collect_resource(player_pos, resources, resource_type):
    global wood, stone
    for resource in resources:
        if resource.rect.collidepoint(player_pos):
            if resource_type == "tree":
                wood += 1
            elif resource_type == "rock":
                stone += 1
            resources.remove(resource)
            break

# Game loop
def game_loop():
    global player_health, player_hunger, wood, stone, day_time, is_night
    running = True

    while running:
        screen.fill(WHITE)

        # Manage day/night cycle
        day_time += 1
        if day_time >= day_length:
            is_night = not is_night
            day_time = 0

        # Decrease hunger over time
        if day_time % 200 == 0:
            player_hunger -= 1

        # Handle hunger effect on health
        if player_hunger <= 0:
            player_health -= 1
        if player_health <= 0:
            draw_text("Game Over", font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # Display player stats
        draw_text(f"Health: {player_health}", font, BLACK, 10, 10)
        draw_text(f"Hunger: {player_hunger}", font, BLACK, 10, 50)
        draw_text(f"Wood: {wood}", font, BLACK, 10, 90)
        draw_text(f"Stone: {stone}", font, BLACK, 10, 130)

        # Day/Night indicator
        if is_night:
            draw_text("Night", font, BLACK, SCREEN_WIDTH - 100, 10)
        else:
            draw_text("Day", font, BLACK, SCREEN_WIDTH - 100, 10)

        # Draw resources (trees and rocks)
        for tree in trees:
            pygame.draw.rect(screen, BROWN, tree.rect)
        for rock in rocks:
            pygame.draw.rect(screen, GRAY, rock.rect)

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Draw player
        pygame.draw.rect(screen, GREEN, (*player_pos, 40, 40))

        # Resource collection
        if keys[pygame.K_e]:
            collect_resource(player_pos, trees, "tree")
            collect_resource(player_pos, rocks, "rock")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()
