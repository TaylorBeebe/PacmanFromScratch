from ghost import *

##
# The Orange Ghost ;)
# Class containing variables and functions specific to the orange ghost
#
# Clyde's behavior is as follows: When Clyde is close to Pacman, they retreat to their scatter position. When their
# further away from Pac, they pursue Pac
##
class Clyde(Ghost):
    def __init__(self,x,y,scatterPos,pacRef,speed = defaultGhostSpeed, debug = False):

        super().__init__("Orange Ghost",
                        x,                                                  # My current position x coord
                        y,                                                  # My current position y coord
                        scatterPos,                                         # The position I go to when scattering
                        x,                                                  # My position x coord in the ghost house (set to my current position because I start in the ghost house)
                        y,                                                  # My position y coord in the ghost house (set to my current position because I start in the ghost house)
                        pygame.image.load("pictures/orangeGhostD.png"),     # Orange ghost eyes down image
                        pygame.image.load("pictures/orangeGhostU.png"),     # Orange ghost eyes up image
                        pygame.image.load("pictures/orangeGhostL.png"),     # Orange ghost eyes left image
                        pygame.image.load("pictures/orangeGhostR.png"),     # Orange ghost eyes right image
                        pacRef,                                             # A reference to Pacman
                        speed,                                              # My speed
                        debug)                                              # True if clyde should print debug messages
        
        # I start in the ghost house moving down
        self.deltaX = 0                                                     
        self.deltaY = -1

    ##
    # Specific Update function which chooses target square based on Clyde's behavior in the original Pacman
    ##
    def Update(self, speed = defaultGhostSpeed):
        
        # If I'm in the ghost house and Pacman has eaten 1/3 of the dots, I can leave as per original Pacman
        if((self.pacRef.numberOfDotsEaten / numberStartingDots >= 1 / 3) and self.inGhostHouse):
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

                    # Get the distance from Pacman
                    distFromPac = math.sqrt((self.x - pacLoc[0])**2 + (self.y - pacLoc[1])**2)

                    # If my distance is greater than 8 squares, pursue Pacman
                    if distFromPac > 8:
                        self.targetX = pacLoc[0]
                        self.targetY = pacLoc[1]
                    
                    # Otherwise, retreat to my scatter position
                    else:
                        self.targetX = self.scatterPos[0]
                        self.targetY = self.scatterPos[1]
        
        # Call Update() in Ghost located in ghost.py
        super().Update(speed)