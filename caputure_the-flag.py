import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Capture the Flag Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Player variables
PLAYER_SIZE = 40
player_speed = 5
team_blue_players = []
team_red_players = []
flag_blue = None
flag_red = None

# Game variables
flag_captured = False
flag_carrier = None

# Flag class
class Flag:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, 40, 40)
        self.captured = False

# Player class
class Player:
    def __init__(self, x, y, color, team):
        self.x = x
        self.y = y
        self.color = color
        self.team = team
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.has_flag = False

    def move(self, keys):
        if self.team == "blue":
            if keys[pygame.K_w]:
                self.y -= player_speed
            if keys[pygame.K_s]:
                self.y += player_speed
            if keys[pygame.K_a]:
                self.x -= player_speed
            if keys[pygame.K_d]:
                self.x += player_speed
        elif self.team == "red":
            if keys[pygame.K_UP]:
                self.y -= player_speed
            if keys[pygame.K_DOWN]:
                self.y += player_speed
            if keys[pygame.K_LEFT]:
                self.x -= player_speed
            if keys[pygame.K_RIGHT]:
                self.x += player_speed

        self.rect.topleft = (self.x, self.y)

# Initialize teams
def init_teams():
    global team_blue_players, team_red_players, flag_blue, flag_red
    team_blue_players = [Player(100, 100, BLUE, "blue")]
    team_red_players = [Player(700, 500, RED, "red")]

    # Create flags for each team
    flag_blue = Flag(50, 50, BLUE)
    flag_red = Flag(750, 550, RED)

# Check for flag capture
def check_flag_capture():
    global flag_carrier, flag_captured
    for player in team_blue_players + team_red_players:
        if not player.has_flag and player.team == "blue" and player.rect.colliderect(flag_red.rect):
            player.has_flag = True
            flag_carrier = player
        if not player.has_flag and player.team == "red" and player.rect.colliderect(flag_blue.rect):
            player.has_flag = True
            flag_carrier = player

# Check for scoring
def check_score():
    global flag_carrier, flag_captured
    if flag_carrier and flag_carrier.has_flag:
        if flag_carrier.team == "blue" and flag_carrier.rect.colliderect(pygame.Rect(50, 50, 40, 40)):
            flag_captured = True
            return "Blue team wins!"
        if flag_carrier.team == "red" and flag_carrier.rect.colliderect(pygame.Rect(750, 550, 40, 40)):
            flag_captured = True
            return "Red team wins!"
    return None

# Game loop
def game_loop():
    global flag_captured
    init_teams()
    running = True

    while running:
        screen.fill(WHITE)

        # Display the flags
        pygame.draw.rect(screen, flag_blue.color, flag_blue.rect)
        pygame.draw.rect(screen, flag_red.color, flag_red.rect)

        # Player movement
        keys = pygame.key.get_pressed()
        for player in team_blue_players + team_red_players:
            player.move(keys)
            pygame.draw.rect(screen, player.color, player.rect)

        # Check for flag capture
        check_flag_capture()

        # Check for scoring
        result = check_score()
        if result:
            draw_text(result, font, GREEN, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(2000)
            init_teams()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()
