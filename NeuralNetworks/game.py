import numpy as np
import random
import threading
import math
import pygame

organisms = []
size = (1000, 1000)
xlimit, ylimit = ((int)(size[0] * 0.1) - 1, (int)(size[1] * 0.1) - 1)
BLACK = (0, 0, 0)  # BLACK
WHITE = (255, 255, 255)  # WHITE
FOOD = (0, 255, 0)  # GREEN
ENEMY = (255, 0, 0)  # RED
AI = (0, 0, 255)  # BLUE
BLOCK = (255, 255, 0)  # YELLOW

grid = []
food = []


class Organism:
    def __init__(self, n_inputs, n_hidden, n_outputs, spawn_x, spawn_y, index):
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs
        self.index = index
        random.seed(index)
        self.weights_1 = 2 * np.random.random((self.n_inputs, self.n_hidden)) - 1
        self.weights_2 = 2 * np.random.random((self.n_hidden, self.n_outputs)) - 1

        self.pos_x = spawn_x
        self.pos_y = spawn_y
        self.prev_x = 0
        self.prev_y = 0

        self.energy = 300
        self.decreaseWeights()
        self.randomMutation()

    def update_pos(self, x, y):
        if x < 0:
            x = xlimit
        if x > xlimit:
            x = 0
        if y < 0:
            y = ylimit
        if y > ylimit:
            y = 0
        self.prev_x = self.pos_x
        self.prev_y = self.pos_y
        self.pos_x = x
        self.pos_y = y

    def update_self(self, i_n, i_e, i_s, i_w, f_d):
        inp = np.array([[i_n, i_e, i_s, i_w, f_d]])
        hl1 = np.tanh(np.dot(inp, self.weights_1))
        o = np.tanh(np.dot(hl1, self.weights_2))
        # o= random.choice([0.24, 0.49, 0.74, 1])
        if o < 0.25:
            self.update_pos(self.pos_x, self.pos_y + 1)
        # print("N")
        elif 0.25 <= o < 0.5:
            self.update_pos(self.pos_x + 1, self.pos_y)
        # print("E")
        elif 0.5 <= o < 0.75:
            self.update_pos(self.pos_x, self.pos_y - 1)
        # print("S")
        elif 0.75 <= o <= 1:
            self.update_pos(self.pos_x - 1, self.pos_y)
        # print("W")
        if getGrid(-self.pos_y, self.pos_x) == 2:
            addFood()
            self.eat(100)
        elif getGrid(-self.pos_y, self.pos_x) == 3:
            self.eat(500)
        self.energy -= 1
        if self.energy <= 0:
            self.die()

    def eat(self, en):
        self.energy += en

    def die(self):
        organisms.remove(self)
        modifyGrid(self.prev_x, self.prev_y, 3)

    def decreaseWeights(self):
        self.weights_1 *= 0.999
        self.weights_2 *= 0.999
        threading.Timer(1 / 60, self.decreaseWeights).start()

    def randomMutation(self):
        self.weights_1 = self.weights_1 + random.uniform(-0.1, 0.10)
        self.weights_2 = self.weights_2 + random.uniform(-0.1, 0.1)
        threading.Timer(1 / 60, self.randomMutation).start()


def computeDistance(myX, myY, targetX, targetY):
    return math.sqrt(((targetX - myX) ** 2 + (targetY - myY) ** 2))


def spawnOrganisms(num):
    for i in range(num):
        organisms.append(Organism(5, 2, 1, random.randint(0, 99), random.randint(0, 99), i))


def addFood():
    fx = random.randint(0, xlimit)
    fy = random.randint(0, ylimit)
    global food
    food = [fx, fy]
    modifyGrid(fx, fy, 2)
    #threading.Timer(1, addFood).start()


def modifyGrid(x, y, value):
    grid[-y][x] = value


def convertCoords(x, y):
    return [-y, x]


def getGrid(x, y):
    return grid[x][y]


def main_game(size_x, size_y, refresh_rate):
    # This sets the width and height of each grid location
    cell_width = 9
    cell_height = 9
    # This sets the margin between each cell
    margin = int(size_x * 0.001)
    cells_x = int(size_x * 0.1)
    cells_y = int(size_y * 0.1)
    for row in range(cells_x):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(cells_y):
            grid[row].append(0)  # Append a cell
    pygame.init()

    # Set the height and width of the screen
    screen_size = [size_x, size_y]
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    # Set title of screen
    pygame.display.set_caption("Evolution Simulation")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    pygame.init()
    addFood()
    current = 2
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("LEFT")
                if event.key == pygame.K_RIGHT:
                    print("RIGHT")
                if event.key == pygame.K_UP:
                    print("UP")
                if event.key == pygame.K_DOWN:
                    print("DOWN")
        for org in organisms:
            modifyGrid(org.pos_x, org.pos_y, 1)
            modifyGrid(org.prev_x, org.prev_y, 0)
            x = org.pos_x
            y = org.pos_y
            if x - 1 < 0:
                x = xlimit
            if x + 1 > xlimit:
                x = 0
            if y - 1 < 0:
                y = ylimit
            if y + 1 > ylimit:
                y = 0
            n = convertCoords(x, y + 1)
            e = convertCoords(x + 1, y)
            s = convertCoords(x, y - 1)
            w = convertCoords(x - 1, y)
            fd = computeDistance(x, y, food[0], food[1])
            # a = computeDistance(org.pos_x, org.pos_y, 0, 0)
            org.update_self(getGrid(n[0], n[1]), getGrid(e[0], e[1]), getGrid(s[0], s[1]), getGrid(w[0], w[1]), fd)
        # if x < 0:
        #     x = 99
        #     segment = (x,y)
        # if x > 99:
        #     x = 0
        #     segment = (x,y)
        # if y < 0:
        #     y = 99
        #     segment = (x,y)
        # if y > 99:
        #     y = 0
        #     segment = (x,y)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            current = 1
        elif keys[pygame.K_2]:
            current = 2
        elif keys[pygame.K_3]:
            current = 3
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (cell_width + margin)
            row = pos[1] // (cell_height + margin)
            grid[row][column] = current
            print("Click ", pos, "Grid coordinates: ", row, column)

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(cells_x):
            for column in range(cells_y):
                color = WHITE
                if grid[row][column] == 0:
                    color = WHITE
                if grid[row][column] == 1:
                    color = AI
                elif grid[row][column] == 2:
                    color = FOOD
                elif grid[row][column] == 3:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(margin + cell_width) * column + margin,
                                  (margin + cell_height) * row + margin,
                                  cell_width,
                                  cell_height])

        # Limit to 60 frames per second
        clock.tick(refresh_rate)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


spawnOrganisms(10)
main_game(size[0], size[1], 30)
