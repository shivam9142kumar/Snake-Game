import pygame
import sys
import random
import os

# Direction constants
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)
BORDER_COLOR = (200, 200, 200)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)

class SnakeGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.high_score = self.load_high_score()
        self.reset()

    def reset(self):
        self.direction = RIGHT
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.apple = self.generate_apple()
        self.score = 0

    def generate_apple(self):
        return (random.randrange(20, self.width - 20, 20), random.randrange(40, self.height - 20, 20))

    def start_screen(self):
        self.display.fill(BLACK)
        title_text = self.font_large.render('Snake Game', True, GREEN)
        instruction_text1 = self.font_small.render('Use arrow keys to move', True, WHITE)
        instruction_text2 = self.font_small.render('Press any key to start', True, WHITE)
        self.display.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 3))
        self.display.blit(instruction_text1, (self.width // 2 - instruction_text1.get_width() // 2, self.height // 2 - 30))
        self.display.blit(instruction_text2, (self.width // 2 - instruction_text2.get_width() // 2, self.height // 2 + 30))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_exit_confirmation()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.countdown()

    def countdown(self):
        countdown_numbers = [3, 2, 1, 'GO!']
        for number in countdown_numbers:
            self.display.fill(BLACK)
            countdown_text = self.font_large.render(str(number), True, GREEN)
            self.display.blit(countdown_text, (self.width // 2 - countdown_text.get_width() // 2, self.height // 3))
            pygame.display.update()
            pygame.time.wait(1000)  # Wait for 1 second

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.show_exit_confirmation()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

        head = self.snake[0]
        if self.direction == UP:
            new_head = (head[0], head[1] - 20)
        elif self.direction == DOWN:
            new_head = (head[0], head[1] + 20)
        elif self.direction == LEFT:
            new_head = (head[0] - 20, head[1])
        elif self.direction == RIGHT:
            new_head = (head[0] + 20, head[1])

        self.snake.insert(0, new_head)
        if self.snake[0] == self.apple:
            self.apple = self.generate_apple()
            self.score += 1
        else:
            self.snake.pop()

        if (self.snake[0][0] < 20 or self.snake[0][0] >= self.width - 20 or
            self.snake[0][1] < 40 or self.snake[0][1] >= self.height - 20 or
            self.snake[0] in self.snake[1:]):
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.reset()

    def render(self):
        self.display.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.display, BORDER_COLOR, pygame.Rect(20, 40, self.width - 40, self.height - 60), 2)
        
        # Draw the snake's body
        for i, pos in enumerate(self.snake):
            if i == 0:  # Head of the snake
                pygame.draw.rect(self.display, (255, 255, 0), pygame.Rect(pos[0], pos[1], 20, 20))  # Yellow head
                pygame.draw.circle(self.display, BLACK, (pos[0] + 10, pos[1] + 10), 5)  # Eyes on the head
            else:  # Body of the snake
                body_color = (0, 200, 0)  # Dark green body color
                # Create a striped effect
                if i % 2 == 0:
                    pygame.draw.rect(self.display, body_color, pygame.Rect(pos[0], pos[1], 20, 20))
                else:
                    pygame.draw.rect(self.display, (0, 150, 0), pygame.Rect(pos[0], pos[1], 20, 20))  # Slightly lighter green
        
        # Draw the apple
        pygame.draw.rect(self.display, RED, pygame.Rect(self.apple[0], self.apple[1], 20, 20))

        # Draw the score
        score_text = self.font_small.render(f'Score: {self.score}', True, WHITE)
        self.display.blit(score_text, [10, 10])
        
        # Draw the high score (positioned at top-right corner)
        high_score_text = self.font_small.render(f'High Score: {self.high_score}', True, WHITE)
        high_score_x = self.width - high_score_text.get_width() - 10  # 10 pixels from the right edge
        high_score_y = 10  # 10 pixels from the top edge
        self.display.blit(high_score_text, [high_score_x, high_score_y])
        
        pygame.display.update()

    def load_high_score(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                return int(file.read().strip())
        return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def show_exit_confirmation(self):
        self.display.fill(BLACK)
        confirmation_text = self.font_large.render('Are you sure you want to quit?', True, WHITE)
        yes_text = self.font_small.render('Press Y to Yes, N to No', True, WHITE)
        self.display.blit(confirmation_text, (self.width // 2 - confirmation_text.get_width() // 2, self.height // 3))
        self.display.blit(yes_text, (self.width // 2 - yes_text.get_width() // 2, self.height // 2))
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.running = False
                        return
                    elif event.key == pygame.K_n:
                        waiting = False

    def run(self):
        self.start_screen()
        self.running = True
        while self.running:
            self.step()
            self.render()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
