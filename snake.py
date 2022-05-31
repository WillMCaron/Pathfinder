# imports
import pygame, sys
from pygame.locals import *
from random import randint
from time import sleep

# initialization
pygame.init()

WIDTH = HEIGHT = 400
SIZE = 8
SPEED = 1
score = 0

windowSurface = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
pygame.display.set_caption('Grid Revision 1')

BLACK = (0,0,0)
GREY = (100,100,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Node:
  def __init__(self, row, col, width):
    self.x = col*width
    self.y = row*width
    self.row = row
    self.col = col
    self.color = WHITE
    self.width = width

  def draw(self, surface):
    pygame.draw.rect(surface,self.color, (self.x, self.y, self.width, self.width))

  def is_snake(self):
    return self.color == GREEN

  def is_apple(self):
    return self.color == RED

  def is_empty(self):
    return self.color == WHITE

  def to_snake(self):
    self.color = GREEN

  def to_apple(self):
    self.color = RED

  def reset(self):
    self.color = WHITE
    
    
def make_grid(rows, width):
  grid = []
  for i in range(rows):
    grid.append([])
    for j in range(width):
      grid[i].append(Node(i,j,SIZE))
  return grid

def draw_grid(surface, rows, width):
  size = width//rows
  for i in range(rows):
    # horizontal
    pygame.draw.line(surface,GREY,(0,i*size),(width, i*size))
    for j in range(rows):
      # vertical
      pygame.draw.line(surface, GREY, (j*size, 0), (j*size, width))

def draw(surface, grid, rows, width, snake, apple):
  surface.fill(WHITE)
  for row in grid:
    for col in row:
      col.draw(surface)
  apple.draw(surface)
  snake.draw(surface, apple)
  draw_grid(surface, rows, width)
  pygame.display.update()

def check_mouse_pos(width):
  x,y = pygame.mouse.get_pos()
  row = y//width
  col = x//width
  return row, col


class Snake:
  def __init__(self, size):
    #positions
    self.body = [[4,0],[4,1],[4,2]]
    self.pos = [4,2]
    self.direction = "right"
    self.change_to = "right"
    self.speed = 2
    self.width = WIDTH//size
    self.color = GREEN

  def move(self):
    if self.direction == "right":
      self.pos[1] += 1
    elif self.direction == "left":
      self.pos[1] -= 1
    elif self.direction == "up":
      self.pos[0] -= 1
    elif self.direction == "down":
      self.pos[0] += 1
    self.body.append(list(self.pos))

  def gameOver(self, rows):
      y,x = self.pos
      if x < 0 or x > rows-1 or y < 0 or y > rows-1:
        return False
      if self.pos in self.body[:len(self.body)-2]:
        return False
      return True

  def score(self, apple):
    global score
    if self.pos == apple.pos:
      apple.respawn(self.body)
      score += 10
    else:
      self.body.pop(0)

  def draw(self, surface, apple):
    y = self.body[0][0]
    x = self.body[0][1]
    self.move()
    self.score(apple)
    if self.gameOver(SIZE):
      for y,x in self.body:
        pygame.draw.rect(surface,self.color, (x*self.width, y*self.width, self.width, self.width))


class Apple:
  def __init__(self, snake, size):
    self.x = randint(0,7)
    self.y = randint(0,7)
    self.pos = [self.y, self.x]
    self.width = WIDTH//size
    self.color = RED
    while self.pos in snake.body:
      self.x = randint(0,7)
      self.y = randint(0,7)
      self.pos = [self.y, self.x]
    self.x = self.x*self.width
    self.y = self.y*self.width

  def draw(self, surface):
    pygame.draw.rect(surface,self.color, (self.x, self.y, self.width, self.width))

  def respawn(self, snake):
    self.x = randint(0,7)
    self.y = randint(0,7)
    self.pos = [self.y, self.x]
    while self.pos in snake:
      self.x = randint(0,7)
      self.y = randint(0,7)
      self.pos = [self.y, self.x]
    self.x = self.x*self.width
    self.y = self.y*self.width
  
running = True
grid = make_grid(SIZE,WIDTH)
fps = pygame.time.Clock()
snake = Snake(SIZE)
apple = Apple(snake, SIZE)
draw(windowSurface,grid,SIZE,WIDTH, snake, apple)

while running:
  # check for quit event
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == K_LEFT:
            snake.change_to = "left"
        elif event.key == K_RIGHT:
            snake.change_to = "right"
        elif event.key == K_UP:
            snake.change_to = "up"
        elif event.key == K_DOWN:
            snake.change_to = "down"
  if snake.change_to == "left" and snake.direction != "right":
    snake.direction = "left"
  elif snake.change_to == "right" and snake.direction != "left":
    snake.direction = "right"
  elif snake.change_to == "down" and snake.direction != "up":
    snake.direction = "down"
  elif snake.change_to == "up" and snake.direction != "down":
    snake.direction = "up"
  draw(windowSurface, grid, SIZE, WIDTH,snake,apple)
  running = snake.gameOver(SIZE)
  if score %10 == 0 and score != 0:
    SPEED += .01
  fps.tick(SPEED)
print(score)











