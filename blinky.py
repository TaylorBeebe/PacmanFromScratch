from ghost import *

##
# The Red Ghost :O
# Class containing properties and functions specific to the red ghost
#
# Blinky's behavior is as follows: Get Pacman!
##
class Blinky(Ghost):
    def __init__(self,x,y,scatterPos,pacRef,speed = defaultGhostSpeed, debug = False):
        
        super().__init__("Red Ghost",
                         x,                                                 # My current position x coord 
                         y,                                                 # My current position y coord   
                         scatterPos,                                        # The position I go to when scattering   
                         13,                                                # My position x coord in the ghost house
                         14,                                                # My position y coord in the ghost house
                         pygame.image.load("pictures/redGhostD.png"),       # Blue ghost eyes down image
                         pygame.image.load("pictures/redGhostU.png"),       # Blue ghost eyes up image  
                         pygame.image.load("pictures/redGhostL.png"),       # Blue ghost eyes left image 
                         pygame.image.load("pictures/redGhostR.png"),       # Blue ghost eyes right image
                         pacRef,                                            # A reference to Pacman 
                         speed,                                             # My speed  
                         debug)                                             # True if clyde should print debug messages                                                                                                               
        
        # I start outside the ghost house moving left
        self.deltaX = -1
        self.deltaY = 0

        # Override these because I start outside the ghost house
        self.inGhostHouse = False

        # Set my mode to chase, but this will immediately be set to scatter once update is called, causing
        # the red ghost to reverse direction as per orignal Pacman
        self.mode = Mode.chase

    ##
    # Specific Update function which chooses target square based on Blinky's behavior in the original Pacman
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
                if self.CanTurn():
                    
                    # Get Pacman's location
                    pacloc = self.pacRef.GetPos()

                    # Set my target to Pacman
                    self.targetX = pacloc[0]
                    self.targetY = pacloc[1]

        # Call Update() in Ghost located in ghost.py
        super().Update(speed)
