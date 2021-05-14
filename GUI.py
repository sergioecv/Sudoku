#import pygame, sys
#import time
import pygame, sys
from sudoku import solve, possible, possibleSolution
from pygame.locals import *

pygame.font.init()

class Grid:
    grid = [[5, 3, 0,   0, 7, 0,    0, 0, 0],
            [6, 0, 0,   1, 9, 5,    0, 0, 0],
            [0, 9, 8,   0, 0, 0,    0, 6, 0],

            [8, 0, 0,   0, 6, 0,    0 ,0 ,3],
            [4, 0, 0,   8, 0, 3,    0, 0, 1],
            [7, 0, 0,   0, 2, 0,    0, 0, 6],

            [0, 6, 0,   0, 0, 0,    2, 8, 0],
            [0, 0, 0,   4, 1, 9,    0, 0, 5],
            [0, 0, 0,   0, 8, 0,    0, 7, 9]]
    
    # Initializes the object
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None

    # Creates backup values for the grid before the new guess
    def oldValues(self):
        self.test = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        return self.test

    # Updates grid
    def updateModel(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Checks if the value at the cell is possible
    def place(self, valueF):
        row, col = self.selected 
        if self.cubes[row][col].value == 0:
            self.oldValues()
            self.cubes[row][col].setValue(valueF)
            self.updateModel()
            # Checks if the value is possible and if theres a solution with that value
            if possible(row, col, valueF, self.test) and possibleSolution(self.model):
                self.oldValues()
                return True
            else: 
                self.cubes[row][col].setValue(0)
                self.cubes[row][col].setTemp(0)
                self.updateModel()
                return False

    # Draws the possible answer
    def sketchValue(self, valueF):
        row, col = self.selected
        self.cubes[row][col].setTemp(valueF)

    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)
                

    # Selects the cell
    def select(self, row, col):
        # Reset selection
        for i in range(self.rows):
            for j in range(self.rows):
                self.cubes[i][j].selected = False
        # Update the new selection
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # Clears cell
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].setTemp(0)
    
    # Returns the row and col
    def click(self, pos):
        row, col = pos
        if row < self.width and col < self.height:
            gap = self.width / 9
            x = row // gap
            y = col // gap
            return(int(y), int(x))
        else:
            return None
    # Checks if the sudoku is completed
    def isFinished(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.cubes[y][x].value == 0:
                    return False
        return True

class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def setValue(self, val):
        self.value = val

    def setTemp(self, val):
        self.temp = val

    # Draws on the screen
    def draw(self, screen):
        font = pygame.font.SysFont('javanesetext', numberSize)
        x = self.col * cellSize
        y = self.row * cellSize

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, lightergray)
            screen.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, black)
            screen.blit(text, (x + (cellSize/2 - text.get_width()/2), y + (cellSize/2 - text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(screen, orange, (x,y, cellSize ,cellSize), 3)



# initialize variable to define them as global
screen = None
fps = 10                                # frames per second
WinMult = 6                             # changes the size of the grid by modifying this variable
WinSize = 90                            # window size  
WinWidth = WinMult * WinSize            # width of the window
WinHeight = WinMult * WinSize           # height of the window
white = (255,255,255)                   # color of the window
black = (0,0,0)                         # color of grid line
lightgray = (200, 200, 200)             # color of grid line
orange = (249, 168, 0)                  # color of the cell selected
red = (250, 0, 0)                       # color of the  "x"
lightergray = (128, 128, 128)           # color of the sketched number
quadrantSize = (WinSize * WinMult) // 3 # size of the quadrant
cellSize = quadrantSize // 3            # size of each cell
numberSize = cellSize // 6 * 5


# Draw every iteration
def redraw(screen, grid):
    screen.fill(white)
    # Draw time
    font = pygame.font.SysFont("javanesetext", numberSize)
    sketchGrid()
    grid.draw(screen)

# draws the grid lines
def sketchGrid():
    # draw lighter lines
    for x in range(0, WinWidth, cellSize):
        pygame.draw.line(screen, lightgray, (x,0) , (x,WinHeight))
    for y in range(0, WinHeight, cellSize):
        pygame.draw.line(screen, lightgray, (0,y), (WinWidth, y))
    # draw darker lines
    for x in range(0, WinWidth, quadrantSize):
        pygame.draw.line(screen, black, (x,0) , (x,WinHeight))
    for y in range(0, WinHeight, quadrantSize):
        pygame.draw.line(screen, black, (0,y), (WinWidth, y))
    return None
    

# main function
def main():
    global screen
    
    # initilize screen
    pygame.init()
    
    screen = pygame.display.set_mode((WinWidth, WinHeight))

    # initializes object grid
    grid = Grid(9, 9, WinWidth, WinHeight)

    # shows screen with format and leyend desired
    pygame.display.set_caption("Sudoku solver") 

    screen.fill(white)
    sketchGrid()

    key = None
    run = True
    

    # main loop
    while run:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    grid.clear()
                    key = None
                # if pressed return key, checks if temp value is possible
                if event.key == pygame.K_RETURN:
                    y, x = grid.selected
                    if grid.cubes[y][x].temp != 0:
                        if grid.place(grid.cubes[y][x].temp):
                            print('Correct!')
                        else:
                            print('Wrong')
                        key = None

                        if grid.isFinished():
                            print('GAME OVER')
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None
        if grid.selected and key != None:
            grid.sketchValue(key)
        redraw(screen, grid)

        # updates game
        pygame.display.update()
        


main()
pygame.quit()



