# -1import pygame
import sys
import random

# 初始化 pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 定义屏幕和网格尺寸
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 定义蛇类
class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE * 3, GRID_SIZE * 3), (GRID_SIZE * 2, GRID_SIZE * 3), (GRID_SIZE, GRID_SIZE * 3)]
        self.direction = (GRID_SIZE, 0)

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        if (new_direction[0] + self.direction[0] != 0) or (new_direction[1] + self.direction[1] != 0):
            self.direction = new_direction

    def is_dead(self):
        head = self.body[0]
        if head in self.body[1:] or head[0] < 0 or head[1] < 0 or head[0] >= SCREEN_WIDTH or head[1] >= SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

# 定义食物类
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_new_position(snake_body)

    def generate_new_position(self, snake_body):
        while True:
            x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# 主游戏循环
def game_loop():
    snake = Snake()
    food = Food(snake.body)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))

        snake.move()

        if snake.body[0] == food.position:
            snake.grow()
            food = Food(snake.body)

        if snake.is_dead():
            break

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(10)

# 运行游戏
if __name__ == "__main__":
    while True:
        game_loop()
