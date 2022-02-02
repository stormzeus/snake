import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
pygame.display.set_caption("snake")


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x,y')
BLOCK_SIZE = 20
SPEED = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont('Ariel', 25)


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w//2, self.h//2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.food = None
        self.score = 0
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):

        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self._move(action)
        self.snake.insert(0, self.head)

        # game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        game_over = False
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        if pt.x > self.w-BLOCK_SIZE or pt.x < 0 or pt.y > self.h-BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill((120, 120, 120))  # CHANGE BG LATER
        for pt in self.snake:
            pygame.draw.rect(self.display, RED, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, WHITE, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = FONT.render("SCORE: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):

        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):  # no turn
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):  # turn right
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx]
        else:  # turn left
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x, y = self.head.x, self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)


# if __name__ == '__main__':
#     game = SnakeGameAI()

#     while 1:

#         game_over, score = game.play_step()
#         if game_over == True:
#             break

#     pygame.quit()
