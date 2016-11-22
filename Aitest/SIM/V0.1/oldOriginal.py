import pygame,random, numpy

NEIGHBOURS = (0,0,0)            #BLACK
WHITE = (255,255,255)           #WHITE
FOOD = (0,255,0)                #GREEN
ENEMY   = (255,0,0)             #RED
AI  = (0,0,255)                 #BLUE
BLOCK = (255,255,0)             #YELLOW
FEELERS = (0,0,0)
# This sets the width and height of each grid location
width  = 9
height = 9
x_limit, y_limit = (99,99)
# This sets the margin between each cell
margin = 1
health = 50
grid = []
for row in range(x_limit+1):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(y_limit+1):
        grid[row].append(0) # Append a cell
player = True
def move(x,y):
    c = random.choice([1,2,3,4,5])
    if c == 1:
        x_change = random.choice([-1,0,1])
        y_change = random.choice([-1,0,1])
    elif c == 2:
        x_change = random.choice([0,1])
        y_change = random.choice([-1,0,1])
    elif c == 3:
        x_change = 1
        y_change = 0
    elif c == 4:
        x_change = 0
        y_change = -1
    elif c == 5:
        x_change = 0
        y_change = 0
    return x_change,y_change
def update_food(foodlist):
    c = random.choice([1])
    if c == 1:
        a,b = random.randint(0,99),random.randint(0,99)
        foodlist.append((a,b))
        print("Food added to ", a,b)
        print("Number of food pieces", len(foodlist))
    for food in foodlist:
        grid[food[0]][food[1]] = 3

def update():
    for row in range(x_limit+1):
        for column in range(y_limit+1):
            if grid[row][column] == 3:
                if ((row,column)) not in foodlist:
                    foodlist.append((row,column))
            if grid[row][column] == 4:
                if ((row,column)) not in enemylist:
                    enemylist.append((row,column))
def grow(health):
    c = random.choice([0,1])
    if c == 1:
        a = snake_segments[0][0]
        b = snake_segments[0][1]
        new = (a,b)
        snake_segments.append(new)
        health += 1
    print("Snake is",len(snake_segments),"blocks long")
    return health
def shrink():
    c = random.choice([0,1])
    if c == 1:
        old_segment = snake_segments.pop()
        grid[old_segment[0]][old_segment[1]] = 0
    print("Snake is",len(snake_segments),"blocks long")
def genfoodlist(x_limit, y_limit):
    i = 0
    foodlist = []
    while i < 100:
        row = random.randint(0, x_limit)
        column = random.randint(0, y_limit)
        foodlist.append((row,column))
        update_food(foodlist)
        i+=1
    return foodlist
def genenemy(x_limit, y_limit):
    i = 0
    enemylist = []
    while i<35:
        row = random.randint(0, x_limit)
        column = random.randint(0, y_limit)
        enemylist.append((row,column))
        grid[row][column] = 4
        i+=1
    return enemylist
def spawnai():
    length = random.randint(2,15)
    i = 0
    x = random.randint(1,x_limit-15)
    y = random.randint(1,y_limit-15)
    while i != length:
        if x<99:
            x +=1
            i+=1
            segment = (x,y)
            snake_segments.append(segment)
            print(snake_segments)
    return x,y
def sensors(head):
    row = head[0]
    column = head[1]
    grid[row+1][column] = 5
    grid[row-1][column] = 5
    grid[row][column+1] = 5
foodlist = genfoodlist(x_limit, y_limit)
enemylist = genenemy(x_limit, y_limit)
 
# Initialize pygame
pygame.init()
 
# Set the height and width of the screen
size = [1000, 1000]
screen = pygame.display.set_mode(size)
 
# Set title of screen
pygame.display.set_caption("AI test")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen update_foods
clock = pygame.time.Clock()
current = 4
x_change = 0
y_change = 0
pause = False
player = True
snake_segments = []
spawned = spawnai()
x = spawned[0]
y = spawned[1]
def main(x,y,health,current,head):
    update()
    old_segment = snake_segments.pop()
    grid[old_segment[0]][old_segment[1]] = 0
##    grid[x+1][y] = 0
##    grid[x-1][y] = 0
##    grid[x][y+1] = 0
    if head in foodlist:
        foodlist.remove(head)
        grow(health)
        update_food(foodlist)
    if head in enemylist:
        enemylist.remove(head)
        health -= 1
        if len(snake_segments) > 5:
            shrink()
        print("Snakes health is ", health)
    # Figure out where new segment will be
    if x <= x_limit and y <= y_limit and x >= 0 and y >= 0:
        x = snake_segments[0][0]+x_change
        y = snake_segments[0][1]+y_change
        segment = (x,y)
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
    grid_to_update = numpy.array(grid)
    for row in range(x_limit+1):
        for column in range(y_limit+1):
            color = WHITE
            if grid_to_update[row][column] == 0:
                color = WHITE
            if grid_to_update[row][column] == 1:
                color = AI
            elif grid_to_update[row][column] == 2:
                color = BLOCK
            elif grid_to_update[row][column] == 3:
                color = FOOD
            elif grid_to_update[row][column] == 4:
                color = ENEMY
            elif grid_to_update[row][column] == 5:
                color = FEELERS
            pygame.draw.rect(screen,
                             color,
                             [(margin+width)*column+margin,
                              (margin+height)*row+margin,
                              width,
                              height])
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    pygame.display.flip()
    head = snake_segments[0]
    return current, head, health
# -------- Main Program Loop -------- #
while done == False:
    head = snake_segments[0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_p:
                pause = True
            if event.key == pygame.K_a:
                player = False

        if player == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                    y_change = -1
                if event.key == pygame.K_RIGHT:
                    x_change = 0
                    y_change = 1
                if event.key == pygame.K_UP:
                    x_change = -1
                    y_change = 0
                if event.key == pygame.K_DOWN:
                    x_change = 1
                    y_change = 0
        while pause == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If user clicked close
                    pause = False
                    done = True # Flag that we are done so we exit this loop
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_p:
                        pause = False
        while player == False:
            current,head,health = main(x,y,health,current,head)
            x_change,y_change = move(x,y)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        print("Player True")
                        player = True
                if event.type == pygame.QUIT: # If user clicked close
                    player = True
                    done = True
            
    current,head,health = main(x,y,health,current,head)
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()


