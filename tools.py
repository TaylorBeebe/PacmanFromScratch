import pygame
import random
from enum import Enum
import math

dotRegular = 0                                                  # Regular square with a dot
dotJunction = 1                                                 # Junction with a dot (ghosts can turn at junctions)
dotRestricted = 2                                               # Restricted junction with a dot (ghosts can turn but not upwards at restricted junctions)
noDotRegular = 3                                                # Regular square with no dot
noDotJunction = 4                                               # Junction with no dot
noDotRestricted = 5                                             # Restricted junction with no dot
slowdown = 6                                                    # Slowdown space (on the lanes where you warp between sides)
dotSpecial = 7                                                  # Special dot square
dotSpecialJunction = 8                                          # Special dot square at a junction
ghostHouse = 9                                                  # Ghost house squares
inaccessible = 10                                               # Walls

maxMovableGridSquareValue = 8                                   # 8 is the greatest value of a square that we can move onto
maxDotValue = 2                                                 # 2 is the greatest value of a square on which there is a normal dot
diffDotNoDot = 3                                                # Value difference between a square type which has a dot and that same square type without a dot
diffSpecDotNoSpecDot = -4                                       # Value difference between a square type which has a special dot and that same square type without a special dot

pygame.init()                                                   # Initialize pygame

WHITE = (255,255,255)
gameHeight = 620                                                # Game window height
gameWidth = 560                                                 # Game window width
screen = pygame.display.set_mode((gameWidth, gameHeight))       # Sets the size of our game window
pygame.display.set_caption("PACMAN")                            # Sets the caption of our game window
background = pygame.image.load("pictures/pacback.png")          # Load the background
squareLen = 20                                                  # Pixel length of each board square
squareOffset = squareLen / 4                                    # Default offset for entities in square so they appear at the center of the square
CIRCLE = 3                                                      # Size of a regular dot
LARGECIRCLE = 9                                                 # Size of a special dot
numRows = 31                                                    # Number of rows (y coords) in the game grid
numColumns = 28                                                 # Number of columns (x coords) in the game grid
numberStartingDots = 244                                        # Number of dots in the game
specialDotBlinkUserEvent = pygame.USEREVENT + 1                 # Event value for making special dots blink


# NOTE: Lower speed is faster
defaultPacSpeed = 8                                             # Pacman default speed
defaultGhostSpeed = 10                                          # Ghost default speed
ghostHouseGhostSpeed = 15                                       # Ghost in ghost house speed
slowdownGhostSpeed = 14                                         # Ghost on slowdown sqauare speed
eatenGhostSpeed = 5                                             # Ghost which has been eaten and is heading back to the ghost house speed
specialDotGhostSpeed = 16                                       # Ghosts which are frightened speed

collisionPixelThreshold = 16                                    # Pixel distance between two entities to test for collision

# Creates an array for our grid
def CreatePacGrid(numRows,numColumns):
    grid = []
    for row in range(numRows):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])

        # Append the cell which is inaccessible by default
        for column in range(numColumns):
            grid[row].append(inaccessible)
    
    # Set the normal movable spaces with and without dots
    grid[1][1] = dotRegular
    grid[1][2] = dotRegular
    grid[1][3] = dotRegular
    grid[1][4] = dotRegular
    grid[1][5] = dotRegular
    grid[1][6] = dotRegular
    grid[1][7] = dotRegular
    grid[1][8] = dotRegular
    grid[1][9] = dotRegular
    grid[1][10] = dotRegular
    grid[1][11] = dotRegular
    grid[1][12] = dotRegular
    grid[1][15] = dotRegular
    grid[1][16] = dotRegular
    grid[1][17] = dotRegular
    grid[1][18] = dotRegular
    grid[1][19] = dotRegular
    grid[1][20] = dotRegular
    grid[1][21] = dotRegular
    grid[1][22] = dotRegular
    grid[1][23] = dotRegular
    grid[1][24] = dotRegular
    grid[1][25] = dotRegular
    grid[1][26] = dotRegular
    grid[2][1] = dotRegular
    grid[2][6] = dotRegular
    grid[2][12] = dotRegular
    grid[2][15] = dotRegular
    grid[2][21] = dotRegular
    grid[2][26] = dotRegular
    grid[3][1] = dotRegular
    grid[3][6] = dotRegular
    grid[3][12] = dotRegular
    grid[3][15] = dotRegular
    grid[3][21] = dotRegular
    grid[3][26] = dotRegular
    grid[4][1] = dotRegular
    grid[4][6] = dotRegular
    grid[4][12] = dotRegular
    grid[4][15] = dotRegular
    grid[4][21] = dotRegular
    grid[4][26] = dotRegular
    grid[5][1] = dotRegular
    grid[5][2] = dotRegular
    grid[5][3] = dotRegular
    grid[5][4] = dotRegular
    grid[5][5] = dotRegular
    grid[5][6] = dotRegular
    grid[5][7] = dotRegular
    grid[5][8] = dotRegular
    grid[5][9] = dotRegular
    grid[5][10] = dotRegular
    grid[5][11] = dotRegular
    grid[5][12] = dotRegular
    grid[5][13] = dotRegular
    grid[5][14] = dotRegular
    grid[5][15] = dotRegular
    grid[5][16] = dotRegular
    grid[5][17] = dotRegular
    grid[5][18] = dotRegular
    grid[5][19] = dotRegular
    grid[5][20] = dotRegular
    grid[5][21] = dotRegular
    grid[5][22] = dotRegular
    grid[5][23] = dotRegular
    grid[5][24] = dotRegular
    grid[5][25] = dotRegular
    grid[5][26] = dotRegular
    grid[6][1] = dotRegular
    grid[6][6] = dotRegular
    grid[6][9] = dotRegular
    grid[6][18] = dotRegular
    grid[6][21] = dotRegular
    grid[6][26] = dotRegular
    grid[7][1] = dotRegular
    grid[7][6] = dotRegular
    grid[7][9] = dotRegular
    grid[7][18] = dotRegular
    grid[7][21] = dotRegular
    grid[7][26] = dotRegular
    grid[8][1] = dotRegular
    grid[8][2] = dotRegular
    grid[8][3] = dotRegular
    grid[8][4] = dotRegular
    grid[8][5] = dotRegular
    grid[8][6] = dotRegular
    grid[8][9] = dotRegular
    grid[8][10] = dotRegular
    grid[8][11] = dotRegular
    grid[8][12] = dotRegular
    grid[8][15] = dotRegular
    grid[8][16] = dotRegular
    grid[8][17] = dotRegular
    grid[8][18] = dotRegular
    grid[8][21] = dotRegular
    grid[8][22] = dotRegular
    grid[8][23] = dotRegular
    grid[8][24] = dotRegular
    grid[8][25] = dotRegular
    grid[8][26] = dotRegular
    grid[9][6] = dotRegular
    grid[9][12] = noDotRegular
    grid[9][15] = noDotRegular
    grid[9][21] = dotRegular
    grid[10][6] = dotRegular
    grid[10][12] = noDotRegular
    grid[10][15] = noDotRegular
    grid[10][21] = dotRegular
    grid[11][6] = dotRegular
    grid[11][9] = noDotRegular
    grid[11][10] = noDotRegular
    grid[11][11] = noDotRegular
    grid[11][12] = noDotRegular
    grid[11][13] = noDotRegular
    grid[11][14] = noDotRegular
    grid[11][15] = noDotRegular
    grid[11][16] = noDotRegular
    grid[11][17] = noDotRegular
    grid[11][18] = noDotRegular
    grid[11][21] = dotRegular
    grid[12][6] = dotRegular
    grid[12][9] = noDotRegular
    grid[12][18] = noDotRegular
    grid[12][21] = dotRegular
    grid[13][6] = dotRegular
    grid[13][9] = noDotRegular
    grid[13][18] = noDotRegular
    grid[13][21] = dotRegular
    grid[14][0] = dotRegular
    grid[14][1] = dotRegular
    grid[14][2] = dotRegular
    grid[14][3] = dotRegular
    grid[14][4] = dotRegular
    grid[14][5] = noDotRegular
    grid[14][6] = dotRegular
    grid[14][7] = noDotRegular
    grid[14][8] = noDotRegular
    grid[14][9] = noDotRegular
    grid[14][18] = noDotRegular
    grid[14][19] = noDotRegular
    grid[14][20] = noDotRegular
    grid[14][21] = dotRegular
    grid[14][22] = noDotRegular
    grid[14][23] = dotRegular
    grid[14][24] = dotRegular
    grid[14][25] = dotRegular
    grid[14][26] = dotRegular
    grid[14][27] = dotRegular
    grid[15][6] = dotRegular
    grid[15][9] = noDotRegular
    grid[15][18] = noDotRegular
    grid[15][21] = dotRegular
    grid[16][6] = dotRegular
    grid[16][9] = noDotRegular
    grid[16][18] = noDotRegular
    grid[16][21] = dotRegular
    grid[17][6] = dotRegular
    grid[17][9] = noDotRegular
    grid[17][10] = noDotRegular
    grid[17][11] = noDotRegular
    grid[17][12] = noDotRegular
    grid[17][13] = noDotRegular
    grid[17][14] = noDotRegular
    grid[17][15] = noDotRegular
    grid[17][16] = noDotRegular
    grid[17][17] = noDotRegular
    grid[17][18] = noDotRegular
    grid[17][21] = dotRegular
    grid[18][6] = dotRegular
    grid[18][9] = noDotRegular
    grid[18][18] = noDotRegular
    grid[18][21] = dotRegular
    grid[19][6] = dotRegular
    grid[19][9] = noDotRegular
    grid[19][18] = noDotRegular
    grid[19][21] = dotRegular
    grid[20][1] = dotRegular
    grid[20][2] = dotRegular
    grid[20][3] = dotRegular
    grid[20][4] = dotRegular
    grid[20][5] = dotRegular
    grid[20][6] = dotRegular
    grid[20][7] = dotRegular
    grid[20][8] = dotRegular
    grid[20][9] = dotRegular
    grid[20][10] = dotRegular
    grid[20][11] = dotRegular
    grid[20][12] = dotRegular
    grid[20][15] = dotRegular
    grid[20][16] = dotRegular
    grid[20][17] = dotRegular
    grid[20][18] = dotRegular
    grid[20][19] = dotRegular
    grid[20][20] = dotRegular
    grid[20][21] = dotRegular
    grid[20][22] = dotRegular
    grid[20][23] = dotRegular
    grid[20][24] = dotRegular
    grid[20][25] = dotRegular
    grid[20][26] = dotRegular
    grid[21][1] = dotRegular
    grid[21][6] = dotRegular
    grid[21][12] = dotRegular
    grid[21][15] = dotRegular
    grid[21][21] = dotRegular
    grid[21][26] = dotRegular
    grid[22][1] = dotRegular
    grid[22][6] = dotRegular
    grid[22][12] = dotRegular
    grid[22][15] = dotRegular
    grid[22][21] = dotRegular
    grid[22][26] = dotRegular
    grid[23][1] = dotRegular
    grid[23][2] = dotRegular
    grid[23][3] = dotRegular
    grid[23][6] = dotRegular
    grid[23][7] = dotRegular
    grid[23][8] = dotRegular
    grid[23][9] = dotRegular
    grid[23][10] = dotRegular
    grid[23][11] = dotRegular
    grid[23][12] = dotRegular
    grid[23][13] = noDotRegular
    grid[23][14] = noDotRegular
    grid[23][15] = dotRegular
    grid[23][16] = dotRegular
    grid[23][17] = dotRegular
    grid[23][18] = dotRegular
    grid[23][19] = dotRegular
    grid[23][20] = dotRegular
    grid[23][21] = dotRegular
    grid[23][24] = dotRegular
    grid[23][25] = dotRegular
    grid[23][26] = dotRegular
    grid[24][3] = dotRegular
    grid[24][6] = dotRegular
    grid[24][9] = dotRegular
    grid[24][18] = dotRegular
    grid[24][21] = dotRegular
    grid[24][24] = dotRegular
    grid[25][3] = dotRegular
    grid[25][6] = dotRegular
    grid[25][9] = dotRegular
    grid[25][18] = dotRegular
    grid[25][21] = dotRegular
    grid[25][24] = dotRegular
    grid[26][1] = dotRegular
    grid[26][2] = dotRegular
    grid[26][3] = dotRegular
    grid[26][4] = dotRegular
    grid[26][5] = dotRegular
    grid[26][6] = dotRegular
    grid[26][9] = dotRegular
    grid[26][10] = dotRegular
    grid[26][11] = dotRegular
    grid[26][12] = dotRegular
    grid[26][15] = dotRegular
    grid[26][16] = dotRegular
    grid[26][17] = dotRegular
    grid[26][18] = dotRegular
    grid[26][21] = dotRegular
    grid[26][22] = dotRegular
    grid[26][23] = dotRegular
    grid[26][24] = dotRegular
    grid[26][25] = dotRegular
    grid[26][26] = dotRegular
    grid[27][1] = dotRegular
    grid[27][12] = dotRegular
    grid[27][15] = dotRegular
    grid[27][26] = dotRegular
    grid[28][1] = dotRegular
    grid[28][12] = dotRegular
    grid[28][15] = dotRegular
    grid[28][26] = dotRegular
    grid[29][1] = dotRegular
    grid[29][2] = dotRegular
    grid[29][3] = dotRegular
    grid[29][4] = dotRegular
    grid[29][5] = dotRegular
    grid[29][6] = dotRegular
    grid[29][7] = dotRegular
    grid[29][8] = dotRegular
    grid[29][9] = dotRegular
    grid[29][10] = dotRegular
    grid[29][11] = dotRegular
    grid[29][12] = dotRegular
    grid[29][13] = dotRegular
    grid[29][14] = dotRegular
    grid[29][15] = dotRegular
    grid[29][16] = dotRegular
    grid[29][17] = dotRegular
    grid[29][18] = dotRegular
    grid[29][19] = dotRegular
    grid[29][20] = dotRegular
    grid[29][21] = dotRegular
    grid[29][22] = dotRegular
    grid[29][23] = dotRegular
    grid[29][24] = dotRegular
    grid[29][25] = dotRegular
    grid[29][26] = dotRegular

    # Locations of junctions
    junctions = [(1, 1),(6, 1),(12, 1),(15, 1),(21, 1),(26, 1),(1, 5),(6, 5),(12, 5),(15, 5),(21, 5),(26, 5),(1, 8),
                (6, 8),(9, 8),(12, 8),(15, 8),(18, 8),(21, 8),(26, 8),(9, 11),(18, 11),(6, 14),(9, 14),(18, 14),(21, 14),(9, 17),
                (18, 17),(1, 20),(6, 20),(12, 20),(15, 20),(21, 20),(26, 20),(1, 23),(6, 23),(21, 23),(24, 23),(1, 26),(6, 26),
                (9, 26),(12, 26),(15, 26),(18, 26),(21, 26),(26, 26),(26, 29),(1, 29),(18, 5),(9, 5),(9, 20),(18, 20),(18, 23),
                (9, 23),(3, 26),(24, 26),(12, 29),(15, 29),(3,23),(26, 23)
                ]

    # Locations of restricted junctions
    restrictedJunctions = [(12, 11),(15, 11),(12, 23),(15, 23)]

    # Locations of slowdown squares
    slowdownSquares = [(0,14),(1,14),(2,14),(3,14),(4,14),(23,14),(24,14),(25,14),(26,14),(27,14)]

    # Locations of specil dots
    specialDots = [(26, 3),(1, 3),(1, 23),(26, 23)]

    # Squares of the ghost house
    ghostHouseSquares = [(11,13),(11,14),(11,15),(12,13),(12,14),(12,15),(13,13),(13,14),(13,15),(14,13),(14,14),
                        (14,15),(15,13),(15,14),(15,15),(16,13),(16,14),(16,15)
                        ]

    # Set the junctions
    for x in junctions:
        if grid[x[1]][x[0]] == dotRegular:
            grid[x[1]][x[0]] = dotJunction
        else:
            grid[x[1]][x[0]] = noDotJunction

    # Set the restricted junctions
    for x in restrictedJunctions:
        if grid[x[1]][x[0]] == dotRegular:
            grid[x[1]][x[0]] = dotRestricted
        else:
            grid[x[1]][x[0]] = noDotRestricted

    # Set the slowdown squares
    for x in slowdownSquares:
        grid[x[1]][x[0]] = slowdown

    # Set the special dots
    for x in specialDots:
        if grid[x[1]][x[0]] == dotJunction:
            grid[x[1]][x[0]] = dotSpecialJunction
        else:
            grid[x[1]][x[0]] = dotSpecial

    # Set the ghost house squares
    for x in ghostHouseSquares:
        grid[x[1]][x[0]] = ghostHouse

    # Return the grid
    return grid


##
# Returns true if the given x,y are within the game board
##
def CheckLocationBounds(x,y):
    return x >= 0 and x <= 27 and y >= 0 and y <= 30

##
# Fixes the given x,y if they are out of bounds
##
def FixOutofBoundsCoords(x,y):
    if x < 0:
        x = 1
    elif x > numColumns - 1:
        x = numColumns - 2
    elif y < 0:
        y = 1
    elif y > numRows - 1:
        y = numRows - 2
    
    return (x,y)

# Set the grid so all files can access it
grid = CreatePacGrid(numRows,numColumns)
