import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quest Academy - Math World")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Game variables
score = 0
level = 1
total_questions = 0
correct_answers = 0

# Functions to display text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to generate a math problem (simple addition for demo)
def generate_math_problem():
    num1 = random.randint(1, 10 * level)
    num2 = random.randint(1, 10 * level)
    solution = num1 + num2
    return f"{num1} + {num2} = ?", solution

# Game logic
def math_quiz():
    global score, level, total_questions, correct_answers

    running = True
    input_answer = ""
    problem, solution = generate_math_problem()

    while running:
        screen.fill(WHITE)
        draw_text(f"Level: {level}", small_font, BLACK, 10, 10)
        draw_text(f"Score: {score}", small_font, BLACK, 10, 50)
        draw_text(f"Question: {problem}", font, BLACK, 250, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if answer is correct
                    if input_answer.isdigit() and int(input_answer) == solution:
                        score += 10
                        correct_answers += 1
                    else:
                        score -= 5

                    total_questions += 1
                    input_answer = ""
                    problem, solution = generate_math_problem()

                    # Level up every 5 correct answers
                    if correct_answers % 5 == 0:
                        level += 1
                elif event.key == pygame.K_BACKSPACE:
                    input_answer = input_answer[:-1]
                elif event.unicode.isdigit():
                    input_answer += event.unicode

        # Display input answer
        draw_text(f"Your Answer: {input_answer}", font, BLUE, 250, 300)

        # Display feedback
        if score < 0:
            draw_text("Oops! Try again.", font, RED, 250, 400)
        elif score >= 100:
            draw_text("Well done! Level Complete!", font, BLUE, 200, 400)
            pygame.time.wait(2000)
            return

        pygame.display.update()

# Main menu
def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Quest Academy - Math World", font, BLACK, 200, 150)
        draw_text("Press ENTER to Start", font, BLUE, 250, 300)
        draw_text("Press ESC to Quit", font, RED, 250, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    math_quiz()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    main_menu()
