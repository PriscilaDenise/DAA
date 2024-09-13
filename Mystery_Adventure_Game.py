import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mystery Adventure Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Player setup
player_pos = [100, 100]
player_speed = 5

# Game variables
inventory = []
puzzle_solved = False

# Objects/Clues in the environment
class Clue:
    def __init__(self, x, y, name, collected=False):
        self.x = x
        self.y = y
        self.name = name
        self.rect = pygame.Rect(x, y, 40, 40)
        self.collected = collected

# Create initial clues
clues = [
    Clue(400, 300, "Key"),
    Clue(200, 150, "Note"),
]

# Rooms in the game
class Room:
    def __init__(self, name, objects=None):
        self.name = name
        self.objects = objects if objects else []

# Create rooms
rooms = [
    Room("Living Room", ["Couch", "Lamp", "Table"]),
    Room("Study", ["Desk", "Bookshelf", "Safe"]),
]

current_room = rooms[0]

# Functions to display text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to handle clue collection
def collect_clue(player_pos):
    global clues, inventory
    for clue in clues:
        if not clue.collected and clue.rect.collidepoint(player_pos):
            clue.collected = True
            inventory.append(clue.name)
            draw_text(f"You found a {clue.name}!", font, GREEN, 200, 550)
            pygame.display.update()
            pygame.time.wait(1000)

# Puzzle system
def solve_puzzle():
    global puzzle_solved, inventory
    if "Key" in inventory:
        draw_text("You used the Key to unlock the door!", font, GREEN, 200, 550)
        puzzle_solved = True
    else:
        draw_text("You need a Key to unlock this door.", font, RED, 200, 550)
    pygame.display.update()
    pygame.time.wait(1000)

# Game loop
def game_loop():
    global player_pos, current_room, puzzle_solved
    running = True

    while running:
        screen.fill(WHITE)

        # Display current room and inventory
        draw_text(f"Current Room: {current_room.name}", font, BLACK, 10, 10)
        draw_text(f"Inventory: {', '.join(inventory)}", font, BLACK, 10, 50)

        # Display room objects
        for idx, obj in enumerate(current_room.objects):
            draw_text(f"{obj}", font, BLACK, 10, 100 + idx * 40)

        # Display clues
        for clue in clues:
            if not clue.collected:
                pygame.draw.rect(screen, BLUE, clue.rect)

        # Player movement
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

        # Check for clue collection
        collect_clue(player_pos)

        # Puzzle solving
        if keys[pygame.K_SPACE] and current_room.name == "Study" and not puzzle_solved:
            solve_puzzle()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()
