import pygame
from pygame.locals import *
import time
import random


SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.x = random.randrange(0, 20) * SIZE
        self.y = random.randrange(0, 20) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randrange(0, 20) * SIZE
        self.y = random.randrange(0, 20) * SIZE


class Snake:
    def __init__(self, parent_screen, length=6):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpg').convert()
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((20 * SIZE, 20 * SIZE))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (650, 10))

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake collides with apple:
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            self.snake.increase_length()
            self.apple.move()

        # Snake collides with itself:
        for i in range(3, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                raise 'Game over!'

        # Snake collides with edges:
        if self.snake.x[0] < 0 or self.snake.x[0] > 19*SIZE or self.snake.y[0] < 0 or self.snake.y[0] > 19*SIZE:
            raise 'Game over!'

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line_1 = font.render(f'Game over. Your score is: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(line_1, (150, 300))
        line_2 = font.render('To play again press Enter. To exit press Escape.', True, (255, 255, 255))
        self.surface.blit(line_2, (150, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
