from ghost import *

##
# The Blue Ghost :P
# Class containing properties and functions specific to the blue ghost
#
# Inky's behavior is as follows: Inky uses the position of the red ghost to position themselves such that Pacman
# is between them and the red ghost
##
class Inky(Ghost):
    def __init__(self,x,y,scatterPos,pacRef,redRef,speed = defaultGhostSpeed, debug = False):

        super().__init__("Blue Ghost",
                        x,                                                  # My current position x coord
                        y,                                                  # My current position y coord
                        scatterPos,                                         # The position I go to when scattering
                        x,                                                  # My position x coord in the ghost house (set to my current position because I start in the ghost house)
                        y,                                                  # My position y coord in the ghost house (set to my current position because I start in the ghost house)
                        pygame.image.load("pictures/blueGhostD.png"),       # Blue ghost eyes down image
                        pygame.image.load("pictures/blueGhostU.png"),       # Blue ghost eyes up image
                        pygame.image.load("pictures/blueGhostL.png"),       # Blue ghost eyes left image
                        pygame.image.load("pictures/blueGhostR.png"),       # Blue ghost eyes right image
                        pacRef,                                             # A reference to Pacman
                        speed,                                              # My speed
                        debug)                                              # True if clyde should print debug messages
                        
        # I start in the ghost house moving down
        self.deltaX = 0
        self.deltaY = -1

        # I need a reference to the red ghost for targetting
        self.redRef = redRef

    ##
    # Specific Update function which chooses target square based on Inky's behavior in the original Pacman
    ##
    def Update(self, speed = defaultGhostSpeed):

        # If I'm in the ghost house and Pacman has eaten 30 of the dots, I can leave as per original Pacman
        if(self.pacRef.numberOfDotsEaten >= 30 and self.inGhostHouse):
            self.inGhostHouse = False
            self.leavingGhostHouse = True

        # If I'm frightened, check if I should still be frightened
        if (self.mode == Mode.frightened):
            self.CheckFrighten()

        # If I'm not in/entering/exiting the ghost house and I'm not frightened, then I should conduct normal targetting proceedure
        if(not (self.inGhostHouse or self.leavingGhostHouse or self.enteringGhostHouse or self.setTargetToEnterGhostHouse or self.mode == Mode.frightened)):

            # Check if I should scatter or if I should continue to scatter if I'm currently scattering
            self.ShouldScatter()

            # If I'm scattering, call Scatter() in Ghost located in ghost.py
            if self.mode == Mode.scatter:
                super().Scatter()
            
            # If I'm chasing Pacman
            elif self.mode == Mode.chase:

                # If I can turn, then it makes sense to update my target
                if self.CanTurn():

                    # Get Pacman's location
                    pacLoc = self.pacRef.GetPos()

                    # Get Pacman's direction
                    pacDir = self.pacRef.GetDir()

                    # Take Pacman's location and look two squares in front of it
                    basisX = pacLoc[0] + (2 * pacDir[0])
                    basisY = pacLoc[1] + (2 * pacDir[1])

                    # Make sure that the square it within bounds, if it isn't then adjust it back in bounds
                    (basisX,basisY) = FixOutofBoundsCoords(basisX,basisY)
                    
                    # Get the position of the red ghost
                    redLoc = self.redRef.GetPos()

                    # Get the offset vector between the square two spaces ahead of Pacman and the location of
                    # the red ghost and multiply that by two. This causes Inky to try to position themselves
                    # such that Pacman is between them and the red ghost
                    offsetX = (basisX - redLoc[0]) * 2
                    offsetY = (basisY - redLoc[1]) * 2

                    # Set my target to be the red ghost's position plus the offset vector I just calculated
                    targetX = redLoc[0] + offsetX
                    targetY = redLoc[1] + offsetY

                    # Make sure that the square it within bounds, if it isn't the fix it
                    (targetX,targetY) = FixOutofBoundsCoords(targetX,targetY)
                    
                    # Update my target
                    self.targetX = targetX
                    self.targetY = targetY

                    if(self.debug):
                        print("%s Red Loc: (%d,%d) - Pac + 2: (%d,%d) - Offset Vector: (%d,%d) - New Target: (%d,%d)" % (self.name,redLoc[0],redLoc[1],basisX,basisY,offsetX,offsetY,targetX,targetY))

        # Call Update() in Ghost located in ghost.py
        super().Update(speed)