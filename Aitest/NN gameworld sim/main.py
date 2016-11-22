import pygame
import random
import bfs
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255) 
width = 9
height = 9
margin = 1
x = 100
y = 100
grid = []
for row in range(x):
    grid.append([])
    for column in range(y):
        grid[row].append(0)
pygame.init()
size = [1000, 1000]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NN Game test")
clock = pygame.time.Clock()
def spawnai():
    length = 1
    i = 0
    head_x = random.randint(1,x-15)
    head_y = random.randint(1,y-15)
    while i != length:
        if head_x< x:
            head_x +=1
            i+=1
            segment = (head_x,head_y)
            snake_segments.append(segment)
            print(snake_segments)
    return head_x,head_y
def genfoodlist(x, y):
    i = 0
    foodlist = []
    while i < 1:
        row = random.randint(0, x)
        column = random.randint(0, y)
        foodlist.append((row,column))
        i+=1
    return foodlist
def travel(x_loc, y_loc):
    endpoint = ((x_loc, y_loc))
    graph = bfs.matrix_to_dict(x,y)
    path = bfs.bfs(graph, head, endpoint)
    for coord in path:
        grid[coord[0]][coord[1]] = 4
foodlist = genfoodlist(x-1, y-1)
for food in foodlist:
        grid[food[0]][food[1]] = 3
snake_segments = []
spawned = spawnai()
done = False
head = snake_segments[0]

while done == False:
    head = snake_segments[0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_t:
                travel(foodlist[0][0], foodlist[0][1])
    for part in snake_segments:
        grid[part[0]][part[1]] = 1
    screen.fill(BLACK)
    for row in range(x):
        for column in range(y):
            color = WHITE
            if grid[row][column] == 0:
                color = WHITE
            elif grid[row][column] == 1:
                color = BLUE
            elif grid[row][column] == 3:
                color = GREEN
            elif grid[row][column] == 4:
                color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(margin+width)*column+margin,
                              (margin+height)*row+margin,
                              width,
                              height])
    clock.tick(60) 
    pygame.display.flip()
pygame.quit()

