from pacman import Pacman
from pinky import Pinky
from clyde import Clyde
from inky import Inky
from blinky import Blinky
from ghost import Mode
from tools import *

##
# Sets all ghosts in the ghost list to frightened mode
##
def SetModeFrighten(ghosts):

    for ghost in ghosts:
        ghost.Frightened()

##
# Main game loop
##
def game_loop():
    
    dx = 1                                                                      # Player's desired x direction
    dy = 0                                                                      # Player's desired y direction
    
    gameOver = False                                                            # Loop until the user clicks the close button (quit)
    blink = False                                                               # True if the special dots should be illuminated
    
    clock = pygame.time.Clock()                                                 # Used to manage how fast the screen updates

    pacmanStartingX = 4                                                         # Starting position x coord for pacman
    pacmanStartingY = 1                                                         # Starting position x coord for pacman

    pacman = Pacman(pacmanStartingX, pacmanStartingY,defaultPacSpeed)           # Reference to Pacman
    redGhost = Blinky(13,11,(24,0),pacman,defaultGhostSpeed)                    # Reference to red ghost
    blueGhost = Inky(11,14,(27,30),pacman,redGhost,defaultGhostSpeed)           # Reference to blue ghost
    pinkGhost = Pinky(13,14,(0,0),pacman,defaultGhostSpeed)                     # Reference to pink ghost
    orangeGhost = Clyde(15,14,(0,30),pacman,defaultGhostSpeed)                  # Reference to orange ghost

    ghostList = [redGhost,blueGhost,pinkGhost,orangeGhost]                      # List of all the ghosts

    pygame.event.Event(specialDotBlinkUserEvent, {'special dot blink' : None})  # Event timer to make the special dots blink

    pygame.time.set_timer(specialDotBlinkUserEvent, 175)                        # Start timer for the dot blinking


    while not gameOver:
        eventQueue = pygame.event.get()
        for event in eventQueue:                            # User did something
            if event.type == pygame.QUIT:                   # If user clicked close
                gameOver = True                             # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:                # If user pushed a key down
                if event.key == pygame.K_LEFT:              # If that key was left
                    dx = -1
                    dy = 0
                if event.key == pygame.K_RIGHT:             # If that key was right
                    dx = 1
                    dy = 0
                if event.key == pygame.K_UP:                # If that key was up
                    dx = 0
                    dy = -1
                if event.key == pygame.K_DOWN:              # If that key was down
                    dx = 0
                    dy = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:      # User clicks the mouse.
                
                # Get the position
                pos = pygame.mouse.get_pos()         

                # Change the x/y screen coordinates to grid coordinates        
                column = pos[0] // squareLen                
                row = pos[1] // squareLen                   
                
                # Print it for debug purposes
                print((column,row)) 

            # If the timer has gone off for the special dot blink, then flip the boolean 
            elif event.type == specialDotBlinkUserEvent:
                blink = not blink

        # Redraw background on each frame
        screen.blit(background,(0,0))                       

        # Draw the grid
        for row in range(numRows):
            for column in range(numColumns):

                # If the grid square is a dot, draw the dot
                if (grid[row][column]) <= maxDotValue:
                    pygame.draw.circle(screen, 
                                        WHITE, 
                                        (squareLen * column + 10, 
                                        squareLen * row + 10),
                                        CIRCLE)

                # If the grid square is a special dot, draw the special dot as long as they aren't currently blinking
                elif ((grid[row][column]) == dotSpecial or grid[row][column] == dotSpecialJunction) and blink:
                    pygame.draw.circle(screen, 
                                        WHITE, 
                                        (squareLen * column + 10, 
                                        squareLen * row + 10),
                                        LARGECIRCLE)
                                        
        # Draw Pacman
        pacman.Update(dx,dy)                                  
        
        # Get Pacman's current location
        curPacLoc = pacman.GetPos()

        # If Pacman's location is within grid bounds (it's possible it isn't if we are swapping sides)
        if (CheckLocationBounds(curPacLoc[0],curPacLoc[1])):

            # Check to see if we've eaten a dot
            if(grid[curPacLoc[1]][curPacLoc[0]] <= maxDotValue):

                # Incrase the value of this square with diffDotNoDot (located in tools.py) so it is still
                # the type of square it was originally (junction or regular) but no longer has a dot 
                grid[curPacLoc[1]][curPacLoc[0]] += diffDotNoDot 

                # Increment Pacman's eaten dot counter
                pacman.numberOfDotsEaten += 1

            # If we've eaten a special dot
            elif(grid[curPacLoc[1]][curPacLoc[0]] == dotSpecial or grid[curPacLoc[1]][curPacLoc[0]] == dotSpecialJunction):

                # Add the value of this square with diffSpecDotNoSpecDot (located in tools.py) so it is still
                # a the type of square it was originally (junction or regular) but no longer has a special dot
                grid[curPacLoc[1]][curPacLoc[0]] += diffSpecDotNoSpecDot

                # Tell all the ghosts that Pacman is pissed off
                SetModeFrighten(ghostList)

                # Increment Pacman's eaten dot counter 
                pacman.numberOfDotsEaten += 1
        
        # If we've eaten all the dots, game over
        if(pacman.numberOfDotsEaten >= numberStartingDots):
            gameOver = True

        # Update each ghost
        redGhost.Update()
        blueGhost.Update()
        pinkGhost.Update()
        orangeGhost.Update()

        # Check if any ghost has collided with Pacman
        for ghost in ghostList:

            # If Pacman has collided with ghost
            if(pacman.CheckCollision(ghost)):

                # If ghost is frightened, ghost is not frozen, and ghost has not been eaten already
                if (ghost.mode == Mode.frightened and not pacman.freeze and not ghost.hasBeenEaten):

                    # Om nom nom nom nom
                    ghost.CollideWithPacman()

                    # Set Pacman to freeze
                    pacman.StartFreeze()

                    # Set all ghosts to freeze unless they've been eaten and are thus travelling back to
                    # the ghost house as per orignal Pacman
                    for ghost1 in ghostList:
                        if not ghost1.hasBeenEaten:
                            ghost1.StartFreeze()

                    # Break the outer for loop because there's no reason to check the other ghosts if we've
                    # collided with this one on this frame
                    break
                    
                # If the ghost wasn't frightened, hadn't been eaten, and Pacman isn't currently frozen (to catch the case where Pacman continually collides with
                # a ghost he's eating)
                if (ghost.mode != Mode.frightened and not ghost.hasBeenEaten and not pacman.freeze):
                    
                    # Then no more wacas :(
                    gameOver = True

        clock.tick(60)                                      #Limit to 60 frames per second
        pygame.display.update()                             #Updates the screen with what we've drawn.

    
game_loop()
pygame.quit()
quit()
