from random import randint
from pygame.math import Vector2
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)
LIGHT_GREEN = (50, 255, 50)

BLOCK_SIZE = 20

W = 25
H = W + 2

class Direction:
    RIGHT = Vector2(1, 0)
    LEFT = Vector2(-1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    PAUSE = Vector2(0,0)


class Snake:
    def __init__(self):
        self.body = [Vector2(11, 12), Vector2(10,12), Vector2(9,12)]
        self.direction = Direction.PAUSE
        self.new_block = False
        pygame.mixer.init()
        self.crunch_sound = pygame.mixer.Sound('V2/crunch.wav')

    def draw_snake(self):
        for block in self.body:
            x = block.x*BLOCK_SIZE
            y = block.y*BLOCK_SIZE
            outer_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            inner_rect = pygame.Rect(x+2, y+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
            pygame.draw.rect(game.display, DARK_GREEN, outer_rect)
            pygame.draw.ellipse(game.display, LIGHT_GREEN, inner_rect)
    
    def move(self):
        if self.direction == Direction.PAUSE:
            pass
        elif self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.direction = Direction.PAUSE
        self.body = [Vector2(11, 12), Vector2(10,12), Vector2(9,12)]
        game.score = 0
        

class Food:
    def __init__(self):
        self.new_food()
        
    def place_food(self):
        food_rect = pygame.Rect(self.pos.x*BLOCK_SIZE, self.pos.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        game.display.blit(game.apple,food_rect)

    def new_food(self):
        self.x = randint(0, W-1)
        self.y = randint(2, H-1)
        self.pos = Vector2(self.x, self.y)
        

class Game:
    def __init__(self):
        self.food = Food()
        self.snake = Snake()
        self.score = 0
        self.high_score = 0
        self.snakes = 1
        self.speed = 100
        pygame.init()
        pygame.display.set_caption('Snake')
        self.display = pygame.display.set_mode((W*BLOCK_SIZE, H*BLOCK_SIZE))
        self.apple = pygame.image.load('V2/apple.png').convert_alpha()
        self.trophy = pygame.image.load('V2/trophy.png').convert_alpha()
        self.font = pygame.font.SysFont('arial', 25)
        self.clock = pygame.time.Clock()
        self.game_over_sound = pygame.mixer.Sound('V2/game_over.wav')

    def update(self):
        self.snake.move()
        self.eat_food()
        self.death()
    
    def draw_elements(self):
        self.display.fill(BLACK)
        self.food.place_food()
        self.snake.draw_snake()
        self.score_board()
        pygame.draw.line(game.display, WHITE, [0, 38], [500, 38], 2)
        pygame.display.update()

    def eat_food(self):
        if self.food.pos == self.snake.body[0]:
            self.snake.play_crunch_sound()
            self.food.new_food()
            self.add_score()
            self.snake.add_block()
        
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.new_food()

    def score_board(self):
        score_board = pygame.Rect(BLOCK_SIZE/2, BLOCK_SIZE/2, BLOCK_SIZE, BLOCK_SIZE)
        self.display.blit(self.apple, score_board)
        score_text = self.font.render(str(self.score), True, WHITE)
        self.display.blit(score_text, [2*BLOCK_SIZE, BLOCK_SIZE/4])
        high_score_board = pygame.Rect(4*BLOCK_SIZE, BLOCK_SIZE/2, BLOCK_SIZE, BLOCK_SIZE)
        self.display.blit(self.trophy, high_score_board)
        high_score_text = self.font.render(str(self.high_score), True, WHITE)
        self.display.blit(high_score_text, [5.5*BLOCK_SIZE, BLOCK_SIZE/4])
        snakes_outer_rect = pygame.Rect(7.5*BLOCK_SIZE, BLOCK_SIZE/2, BLOCK_SIZE, BLOCK_SIZE)
        snakes_inner_rect = pygame.Rect(7.5*BLOCK_SIZE+2, BLOCK_SIZE/2+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
        pygame.draw.rect(game.display, DARK_GREEN, snakes_outer_rect)
        pygame.draw.ellipse(game.display, LIGHT_GREEN, snakes_inner_rect)
        snakes_text = self.font.render(str(self.snakes), True, WHITE)
        self.display.blit(snakes_text, [9*BLOCK_SIZE, BLOCK_SIZE/4])

    def add_score(self):
        self.score += 1

    def death(self):
        if not 0 <= self.snake.body[0].x < W or not 2 <= self.snake.body[0].y < H:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print("Snake " + str(self.snakes) + " Game Over! New High Score: " + str(self.high_score))
        else:
            print("Snake " + str(self.snakes) + " Game Over! Score: " + str(self.score))
        self.play_game_over()
        self.snakes += 1
        self.snake.reset()
    
    def play_game_over(self):
        self.game_over_sound.play()


if __name__ == "__main__":
    game = Game()

    DISPLAY_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(DISPLAY_UPDATE, game.speed)


    while True:
        for event in pygame.event.get():
            if event.type == DISPLAY_UPDATE:
                game.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_x:
                    print(str(game.snakes) + " Snakes, High Score: " + str(game.high_score))
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LEFT and game.snake.direction is not Direction.RIGHT and game.snake.direction is not Direction.PAUSE:
                    game.snake.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and game.snake.direction is not Direction.LEFT:
                    game.snake.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and game.snake.direction is not Direction.DOWN:
                    game.snake.direction = Direction.UP
                elif event.key == pygame.K_DOWN and game.snake.direction is not Direction.UP:
                    game.snake.direction = Direction.DOWN
            elif event.type == pygame.QUIT:
                print(str(game.snakes) + " Snakes, High Score: " + str(game.high_score))
                pygame.quit()
                quit()
        
        game.draw_elements()
        game.clock.tick(60)