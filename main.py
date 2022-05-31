# imports
import pygame, sys
from pygame.locals import *
from random import randint
from time import sleep
from queue import PriorityQueue

# initialization
pygame.init()

WIDTH = HEIGHT = 400
SIZE = 40
SPEED = 10

windowSurface = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
pygame.display.set_caption('Grid Revision 1')

BLACK = (0,0,0)
GREY = (100,100,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
PURPLE = (151,50,168)
YELLOW = (255, 255, 0)

class Node:
  def __init__(self, row, col, width, total_rows):
    self.x = col*width//total_rows
    self.y = row*width//total_rows
    self.row = row
    self.col = col
    self.color = WHITE
    self.width = width
    self.neighbors = []
    self.total_rows = total_rows

  def draw(self, surface):
    pygame.draw.rect(surface,self.color, (self.x, self.y, self.width//self.total_rows, self.width//self.total_rows))

  def get_pos(self):
    return self.col, self.row

  def is_start(self):
    return self.color == ORANGE

  def is_end(self):
    return self.color == PURPLE

  def is_barrier(self):
    return self.color == BLACK

  def is_empty(self):
    return self.color == WHITE

  def is_open(self):
    return self.color == GREEN

  def is_closed(self):
    return self.color == RED

  def is_path(self):
    return self.color == YELLOW

  def to_start(self):
    self.color = ORANGE

  def to_open(self):
    self.color = GREEN

  def to_closed(self):
    self.color = RED

  def to_end(self):
    self.color = PURPLE

  def to_barrier(self):
    self.color = BLACK

  def to_path(self):
    self.color = YELLOW

  def reset(self):
    self.color = WHITE

  def update_neighbors(self, grid):
    self.neighbors = []
    # down
    if self.row < (self.total_rows-1) and not grid[self.row+1][self.col].is_barrier():
      self.neighbors.append(grid[self.row+1][self.col])
    # up
    if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
      self.neighbors.append(grid[self.row-1][self.col])
    # right
    if self.col < (self.total_rows-1) and not grid[self.row][self.col+1].is_barrier():
      self.neighbors.append(grid[self.row][self.col+1])
    # left
    if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
      self.neighbors.append(grid[self.row][self.col-1])

  def __lt__(self, other):
    #less than
    return False

def h(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  return abs(x1-x2)+abs(y1-y2)

def reconstruct_path(came_from, current, draw):
  while current in came_from:
    current = came_from[current]
    current.to_path()
    draw()

def algorithm(draw, grid, start, end):
  count = 0
  open_set = PriorityQueue()
  # append
  # (fscore, count for needing to break ties, start)
  open_set.put((0, count, start))
  # what node did this one come from
  came_from = {}
  gscore = {node: float("inf") for row in grid for node in row}
  gscore[start] = 0
  fscore = {node: float("inf") for row in grid for node in row}
  fscore[start] = h(start.get_pos(), end.get_pos())
  # keep track of items in queue
  open_set_hash = {start}
  while not open_set.empty():
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    # gets the node from the open set, starts at start
    current = open_set.get()[2]
    open_set_hash.remove(current)

    if current == end:
      reconstruct_path(came_from, end, draw)
      end.to_end()
      start.to_start()
      return True # make path

    for neighbor in current.neighbors:
      # distance between nodes is one
      temp_g_score = gscore[current]+1
      if temp_g_score < gscore[neighbor]:
        came_from[neighbor] = current
        gscore[neighbor] = temp_g_score
        fscore[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
        if neighbor not in open_set_hash:
          count +=1
          open_set.put((fscore[neighbor], count, neighbor))
          open_set_hash.add(neighbor)
          neighbor.to_open()
    draw()
    if current!= start:
      current.to_closed()
  return False 
    
def make_grid(rows, width):
  grid = []
  for i in range(rows):
    grid.append([])
    for j in range(width):
      grid[i].append(Node(i,j,width, rows))
  return grid

def draw_grid(surface, rows, width):
  size = width//rows
  for i in range(rows):
    # horizontal
    pygame.draw.line(surface,GREY,(0,i*size),(width, i*size))
    for j in range(rows):
      # vertical
      pygame.draw.line(surface, GREY, (j*size, 0), (j*size, width))

def draw(surface, grid, rows, width):
  surface.fill(WHITE)
  for row in grid:
    for col in row:
      col.draw(surface)
  draw_grid(surface, rows, width)
  pygame.display.update()

def check_mouse_pos(width):
  x,y = pygame.mouse.get_pos()
  row = y//width
  col = x//width
  #print(row,col)
  return row, col
  
grid = make_grid(SIZE,WIDTH)
draw(windowSurface,grid,SIZE,WIDTH)
fps = pygame.time.Clock()
released = True
start = None
end = None
type = None
started = False

while True:
  # check for quit event
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == MOUSEBUTTONDOWN:
      released = False
      if event.button == 1:
        type = 1
      elif event.button == 3:
        type = 3
    if event.type == MOUSEBUTTONUP:
      released = True
    if event.type == KEYDOWN:
      if event.key ==K_SPACE and start and end:
        for row in grid:
          for node in row:
            if node.is_open() or node.is_closed() or node.is_path():
              node.reset()
        for row in grid:
          for node in row:
            node.update_neighbors(grid)
        algorithm(lambda: draw(windowSurface, grid, SIZE,WIDTH), grid, start, end)
      if event.key == K_c:
        start = None
        end = None
        grid = make_grid(SIZE,WIDTH)
      

    
  if not released and type == 1:
    mouseRow, mouseCol = check_mouse_pos(WIDTH//SIZE)
    if not start and not grid[mouseRow][mouseCol].is_end():
      start = grid[mouseRow][mouseCol]
      grid[mouseRow][mouseCol].to_start()
    elif not end and not grid[mouseRow][mouseCol].is_start():
      end = grid[mouseRow][mouseCol]
      grid[mouseRow][mouseCol].to_end()
    elif not grid[mouseRow][mouseCol].is_start() and not grid[mouseRow][mouseCol].is_end():
      grid[mouseRow][mouseCol].to_barrier()
  elif not released and type == 3:
    mouseRow, mouseCol = check_mouse_pos(SIZE)
    if grid[mouseRow][mouseCol].is_start():
      start = None
      grid[mouseRow][mouseCol].reset()
    elif grid[mouseRow][mouseCol].is_end():
      end = None
      grid[mouseRow][mouseCol].reset()
    else:
      grid[mouseRow][mouseCol].reset()

  
  draw(windowSurface,grid,SIZE,WIDTH)
  fps.tick(SPEED)
    











