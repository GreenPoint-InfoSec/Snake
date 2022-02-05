import pygame
from random import randint
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_BLUE = (0, 50, 150)
LIGHT_BLUE = (0, 100, 255)

BLOCK_SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        # d = ['RIGHT', 'LEFT', 'UP', 'DOWN']
        # s = randint(1,4)
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.speed = 10
        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # user input
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction is not Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction is not Direction.LEFT:
                        self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction is not Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction is not Direction.UP:
                        self.direction = Direction.DOWN
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        # new food
        if self.head == self.food:
            self.score += 1
            self.speed += 1
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(self.speed)

        return game_over, self.score
    
    def _is_collision(self):
        # boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # self
        if self.head in self.snake[1:]:
            return True

        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, DARK_BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, LIGHT_BLUE, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score) + " Speed: " + str(self.speed), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()