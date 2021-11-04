from ghost import *

##
# The Pink Ghost :D
# Class containing properties and functions specific to the pink ghost
#
# Pinky's behavior is as follows: Pinky is able to leave the ghost house immediately and always tries to get in front
# of Pacman
##
class Pinky(Ghost):
    def __init__(self,x,y,scatterPos,pacRef,speed = defaultGhostSpeed, debug = False):
        super().__init__("Pink Ghost",
                         x,                                                 # My current position x coord 
                         y,                                                 # My current position y coord   
                         scatterPos,                                        # The position I go to when scattering   
                         x,                                                 # My position x coord in the ghost house (set to my current position because I start in the ghost house)
                         y,                                                 # My position y coord in the ghost house (set to my current position because I start in the ghost house)
                         pygame.image.load("pictures/pinkGhostD.png"),      # Pink ghost eyes down image
                         pygame.image.load("pictures/pinkGhostU.png"),      # Pink ghost eyes up image  
                         pygame.image.load("pictures/pinkGhostL.png"),      # Pink ghost eyes left image 
                         pygame.image.load("pictures/pinkGhostR.png"),      # Pink ghost eyes right image
                         pacRef,                                            # A reference to Pacman 
                         speed,                                             # My speed  
                         debug)                                             # True if clyde should print debug messages                                                                                                               
        
        # I start in the ghost house moving up
        self.deltaX = 0
        self.deltaY = 1

    ##
    # Specific Update function which chooses target square based on Pinky's behavior in the original Pacman
    ##
    def Update(self, speed = defaultGhostSpeed):
        
        # If I'm in the ghost house I can leave immediately as per original Pacman
        if(self.inGhostHouse):
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

                    # Set my target to be 4 squares in front of Pacman
                    tarX = pacLoc[0] + (4 * pacDir[0])
                    tarY = pacLoc[1] + (4 * pacDir[1])
                    

                    # Make sure that my target it within bounds, if it isn't then fix it
                    (tarX,tarY) = FixOutofBoundsCoords(tarX,tarY)
                    
                    # Update my target
                    self.targetX = tarX
                    self.targetY = tarY

        # Call Update() in Ghost located in ghost.py
        super().Update(speed)