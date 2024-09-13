import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanded Capture the Flag Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

# Fonts
font = pygame.font.Font(None, 36)

# Player and Game variables
PLAYER_SIZE = 40
player_speed = 5
team_blue_players = []
team_red_players = []
flag_blue = None
flag_red = None
obstacles = []
power_ups = []

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
    def __init__(self, x, y, color, team, tag_radius=40):
        self.x = x
        self.y = y
        self.color = color
        self.team = team
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.has_flag = False
        self.tag_radius = tag_radius
        self.speed_boost = 1.0

    def move(self, keys, control_scheme):
        if self.team == "blue":
            if keys[control_scheme["up"]]:
                self.y -= player_speed * self.speed_boost
            if keys[control_scheme["down"]]:
                self.y += player_speed * self.speed_boost
            if keys[control_scheme["left"]]:
                self.x -= player_speed * self.speed_boost
            if keys[control_scheme["right"]]:
                self.x += player_speed * self.speed_boost
        elif self.team == "red":
            if keys[control_scheme["up"]]:
                self.y -= player_speed * self.speed_boost
            if keys[control_scheme["down"]]:
                self.y += player_speed * self.speed_boost
            if keys[control_scheme["left"]]:
                self.x -= player_speed * self.speed_boost
            if keys[control_scheme["right"]]:
                self.x += player_speed * self.speed_boost

        self.rect.topleft = (self.x, self.y)

    def tag_opponent(self, opponent):
        distance = pygame.math.Vector2(self.x - opponent.x, self.y - opponent.y).length()
        return distance <= self.tag_radius and opponent.has_flag

    def apply_power_up(self, power_up):
        if power_up == "speed_boost":
            self.speed_boost = 1.5
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # Power-up lasts 5 seconds
        elif power_up == "shield":
            pass  # Add shield mechanic here

# Obstacles
class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

# Power-ups
class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.active = True

# Initialize teams
def init_teams():
    global team_blue_players, team_red_players, flag_blue, flag_red, obstacles, power_ups
    team_blue_players = [
        Player(100, 100, BLUE, "blue", 40),
        Player(150, 150, BLUE, "blue", 40)
    ]
    team_red_players = [
        Player(700, 500, RED, "red", 40),
        Player(650, 550, RED, "red", 40)
    ]

    # Create flags
    flag_blue = Flag(50, 50, BLUE)
    flag_red = Flag(750, 550, RED)

    # Add obstacles
    obstacles = [
        Obstacle(300, 200, 100, 50),
        Obstacle(500, 400, 100, 50),
    ]

    # Add power-ups
    power_ups = [
        PowerUp(400, 300, "speed_boost"),
        PowerUp(200, 150, "shield"),
    ]

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

# Check for tagging
def check_tagging():
    global flag_carrier
    for player in team_blue_players:
        for opponent in team_red_players:
            if player.tag_opponent(opponent):
                opponent.has_flag = False
                flag_carrier = None

    for player in team_red_players:
        for opponent in team_blue_players:
            if player.tag_opponent(opponent):
                opponent.has_flag = False
                flag_carrier = None

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

# Check for power-up collection
def check_power_ups():
    global power_ups
    for player in team_blue_players + team_red_players:
        for power_up in power_ups:
            if power_up.active and player.rect.colliderect(power_up.rect):
                player.apply_power_up(power_up.type)
                power_up.active = False

# Game loop
def game_loop():
    global flag_captured
    init_teams()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw flags
        pygame.draw.rect(screen, flag_blue.color, flag_blue.rect)
        pygame.draw.rect(screen, flag_red.color, flag_red.rect)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, GRAY, obstacle.rect)

        # Draw power-ups
        for power_up in power_ups:
            if power_up.active:
                pygame.draw.rect(screen, YELLOW, power_up.rect)

        # Move players
        keys = pygame.key.get_pressed()
        for player in team_blue_players:
            player.move(keys, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d})
            pygame.draw.rect(screen, player.color, player.rect)

        for player in team_red_players:
            player.move(keys, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT})
            pygame.draw.rect(screen, player.color, player.rect)

        # Check for flag capture and tagging
        check_flag_capture()
        check_tagging()

        # Check for power-ups
        check_power_ups()

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
            elif event.type == pygame.USEREVENT + 1:
                for player in team_blue_players + team_red_players:
                    player.speed_boost = 1.0

        pygame.display.update()

# Function to display text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Run the game
if __name__ == "__main__":
    game_loop()
    pygame.quit()