import pygame,random

NEIGHBOURS = (0,0,0)            #BLACK
WHITE = (255,255,255)           #WHITE
FOOD = (0,255,0)                #GREEN
ENEMY   = (255,0,0)             #RED
AI  = (0,0,255)                 #BLUE
BLOCK = (255,255,0)             #YELLOW
# This sets the width and height of each grid location
width  = 9
height = 9
xlimit, ylimit = (99,99)
# This sets the margin between each cell
margin = 1

grid = []
for row in range(100):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(100):
        grid[row].append(0) # Append a cell
def genfood(xlimit, ylimit):
    i = 0
    while i < 100:
        row = random.randint(0, xlimit)
        column = random.randint(0, ylimit)
        grid[row][column] = 3
        i+=1
def genenemy(xlimit, ylimit):
    i = 0
    while i<35:
        row = random.randint(0, xlimit)
        column = random.randint(0, ylimit)
        grid[row][column] = 4
        i+=1
def spawnai(xlimit, ylimit):
    length = random.randint(0,10)
    i = 0
    row = random.randint(0,xlimit)
    column = random.randint(0,ylimit)
    grid[row][column] = 1
    while i != length:
        row +=1
        grid[row][column] = 1
        i+=1


genfood(xlimit, ylimit)
genenemy(xlimit, ylimit)
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
#grid[1][5] = 1
 
# Initialize pygame
pygame.init()
 
# Set the height and width of the screen
size = [1000, 1000]
screen = pygame.display.set_mode(size)
 
# Set title of screen
pygame.display.set_caption("AI test")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
current = 4
x_change = 0
y_change = 0

pygame.init()
snake_segments = []
length = random.randint(5,10)
i = 0
x = random.randint(1,xlimit-10)
y = random.randint(1,ylimit-10)
while i != length:
    if x<99:
        x +=1
        i+=1
        segment = (x,y)
        snake_segments.append(segment)
        print(snake_segments)
# -------- Main Program Loop -----------
while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = 0
                y_change = -1
                print("LEFT")
            if event.key == pygame.K_RIGHT:
                x_change = 0
                y_change = 1
                print("RIGHT")
            if event.key == pygame.K_UP:
                x_change = -1
                y_change = 0
                print("UP")
            if event.key == pygame.K_DOWN:
                x_change = 1
                y_change = 0
                print("DOWN")
 
    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    old_segment = snake_segments.pop()
    grid[old_segment[0]][old_segment[1]] = 0    
    # Figure out where new segment will be

    if x <= xlimit and y <= ylimit and x >= 0 and y >= 0:
        x = snake_segments[0][0]+x_change
        y = snake_segments[0][1]+y_change
        segment = (x,y)
        print(x,y)
    if x < 0:
        x = 99
        segment = (x,y)
    if x > 99:
        x = 0
        segment = (x,y)
    if y < 0:
        y = 99
        segment = (x,y)
    if y > 99:
        y = 0
        segment = (x,y)

    print(segment,"segment")
    # Insert new segment into the list
    snake_segments.insert(0, segment)
    keys=pygame.key.get_pressed()  
    if keys[pygame.K_1]:
        current = 1
    elif keys[pygame.K_2]:
        current = 2
    elif keys[pygame.K_3]:
        current = 3
    elif keys[pygame.K_4]:
        current = 4
    if event.type == pygame.QUIT: # If user clicked close
        done = True # Flag that we are done so we exit this loop
    elif event.type == pygame.MOUSEBUTTONDOWN:
        # User clicks the mouse. Get the position
        pos = pygame.mouse.get_pos()
        # Change the x/y screen coordinates to grid coordinates
        column = pos[0] // (width + margin)
        row = pos[1] // (height + margin)
        grid[row][column] = current
        print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(NEIGHBOURS)
    for item in snake_segments:
        grid[item[0]][item[1]] = 1

 
    # Draw the grid
    for row in range(100):
        for column in range(100):
            color = WHITE
            if grid[row][column] == 0:
                color = WHITE
            if grid[row][column] == 1:
                color = AI
            elif grid[row][column] == 2:
                color = BLOCK
            elif grid[row][column] == 3:
                color = FOOD
            elif grid[row][column] == 4:
                color = ENEMY
            pygame.draw.rect(screen,
                             color,
                             [(margin+width)*column+margin,
                              (margin+height)*row+margin,
                              width,
                              height])
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()


