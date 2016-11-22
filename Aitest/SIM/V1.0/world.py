import pygame
import random
import numpy
import logging
import timeit
logging.basicConfig(level=logging.CRITICAL) #Change to logging.INFO to see logs
logger = logging.getLogger(__name__)
class World(object):
    def __init__(self, worldWidth, worldHeight, cellWidth, cellHeight, cellMargin):
        #Colours#
        self.colours = {'black' : (0, 0, 0),    #Neighbours
                    'white' : (255, 255, 255),  #Empty cells
                    'green' : (0, 255, 0),  #Food
                    'red' : (255, 0, 0),    #Enemies
                    'blue' : (0, 0, 255),   #Ai bots
                    'yellow' : (255, 255, 0)    #Walls/blocks
                    }
        
        #World Constants#
        #One cell is one rectangle in the grid
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.cellMargin = cellMargin
        self.emptyCells = []
        self.blockList = []
        self.foodList = []
        self.activeBots = []
        logging.info('Instance initialised')
    def create(self):
        self.grid = []
        #Create 2d matrix
        for row in range(self.worldWidth):
            self.grid.append([])
            for column in range(self.worldHeight):
                self.grid[row].append(0)
        logging.info('Matrix created')
    def initWorld(self):
        pygame.init()
        logger.info('Pygame initialised')
        #Set the height and width of the screen
        size = [1000, 1000]
        self.screen = pygame.display.set_mode(size)
        #Set title of screen
        pygame.display.set_caption("Snake Sim")
        self.clock = pygame.time.Clock()
        # Draw the grid
        self.create()
        self.updateWorld()
    def updateWorld(self):
##        for row in range(self.worldWidth):
##            for column in range(self.worldHeight):
##                if self.grid[row][column] == 0 and (row,column) not in self.emptyCells:
##                    self.emptyCells.append((row,column))
##                elif self.grid[row][column] == 2 and (row, column) not in self.blockList: 
##                    self.blockList((row,column))
##                elif self.grid[row][column] == 3 and (row, column) not in self.foodList:
##                    self.foodList.append((row,column))
        logging.info('World update start')
        self.screen.fill(self.colours['black'])
        grid = numpy.array(self.grid)
        self.updateAI()
        for row in range(self.worldWidth):
            for column in range(self.worldHeight):
                color = self.colours['white']
                if grid[row][column] == 0:     #Empty cells
                    color = self.colours['white']
                elif grid[row][column] == 1:     #Cells occupied by an AI
                    color = self.colours['blue']
                elif grid[row][column] == 2:    #Cells that are occupied by blocks
                    color = self.colours['yellow']
                elif grid[row][column] == 3:    #Food cells
                    color = self.colours['green']
                elif grid[row][column] == 4:    #Enemy cells
                    color = self.colours['red']
                elif grid[row][column] == 5:    #Feeler cells
                    color = self.colours['black']
                pygame.draw.rect(self.screen,
                                 color,
                                 [(self.cellMargin+self.cellWidth)*column+self.cellMargin,
                                  (self.cellMargin+self.cellHeight)*row+self.cellMargin,
                                  self.cellWidth,
                                  self.cellHeight])
        logging.info('Game world drawn')
        self.clock.tick(60)
        pygame.display.flip()
        logging.info('Game world updated')
    def updateAI(self):
        try:
            for segment in self.snake_segments:
                self.grid[segment[0]][segment[1]] = 1
            logging.info('All segments in self.snake_segmnets set to 1')
        except:
            logging.info('No self.snake_segments')
    def moveAI(self, x_change, y_change):
        old_segment = self.snake_segments.pop()
        self.grid[old_segment[0]][old_segment[1]] = 0
        logging.info('Old segment, %s removed', str(old_segment))
        if self.x <= self.worldWidth and self.y <= self.worldHeight and self.x >= 0 and self.y >= 0:
            self.x = self.snake_segments[0][0] + x_change
            self.y = self.snake_segments[0][1]+y_change
            segment = (self.x,self.y)
        if self.x < 0:
            self.x = 99
            segment = (self.x,self.y)
            logging.info('self.x was smaller than 0')
        if self.x > 99:
            self.x = 0
            segment = (self.x,self.y)
            logging.info('self.x was bigger than 99')
        if self.y < 0:
            self.y = 99
            segment = (self.x,self.y)
            logging.info('self.y was smaller than 0')
        if self.y > 99:
            self.y = 0
            segment = (self.x,self.y)
            logging.info('self.y was bigger than 99')
        logging.info('self.x set to %s', str(self.x))
        logging.info('self.y set to %s', str(self.y))
        logging.info('segment set to %s', str(segment))
        self.snake_segments.insert(0, segment)
        logging.info('new segment added to snake_segments')
        logging.info('AI moved')
        self.updateWorld()
    def giveAIInfo(self, snake_segments):
        self.snake_segments = snake_segments
        logging.info('snake_segments updated; snake_segments = {}'.format(self.snake_segments))
    def xAndY(self, x,y):
        self.x = x
        self.y = y
    def activeBotsAppend(self, botID):
        self.activeBots.append(botID)
        logging.info('Active bot added: %s', str(botID))
    def activeBotsRemove(self, botID):
        self.activeBots.remove(botID)
        logging.info('Active bot removed: %s', str(botID))
##a = World(100, 100, 9, 9, 1)
##a.initWorld()
##a.updateWorld()
##pygame.quit()
