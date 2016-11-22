import pygame


screen = 0
def initializePygame(windowSize):
    # Initialize pygame
    pygame.init()
 
    # Set the height and width of the screen
    size = [windowSize[0], windowSize[1]]
    global screen
    screen = pygame.display.set_mode(size)
 
    # Set title of screen
    pygame.display.set_caption("Dots")
def CreateGrid(mapsize, tileColor):
    # Set the screen background
    global screen
    screen.fill((0, 0, 0))
    # Draw the grid
    for row in range(5):
        for column in range(5):
            print(row, column)
            pygame.draw.rect(screen,
                             (0 , 255, 0),
                             ((1+9) * (row + 1),( 1 + 9) * (column + 1), 9, 9))
initializePygame([1000, 1000])
CreateGrid(0, 0)
#popSize = input("Population Size?")
#genome = []


