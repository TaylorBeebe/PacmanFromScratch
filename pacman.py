from entity import *

##
# The class for Pacman. Inherits all the stuff from Entity located in entity.py
## 
class Pacman(Entity):

    ##
    # Initialize Pacman's variables
    ##
    def __init__(self, x, y, speed = defaultPacSpeed, debug = False):
        super().__init__("Pacman",x,y,speed, debug)

        self.pacClosed = pygame.image.load("pictures/waca1.1.png")   # Pacman image mouth closed
        self.pacMid = pygame.image.load("pictures/waca2.1.png")      # Pacman image mouth midway open
        self.pacOpen = pygame.image.load("pictures/waca3.1.png")     # Pacman image mouth fully open
        
        # An list so we can properly transition between wacas
        self.pacList = [self.pacMid,self.pacMid,self.pacOpen,self.pacOpen,self.pacMid,self.pacMid,self.pacClosed,self.pacClosed]
        
        self.currentPac = 0                                         # Current waca image
        self.numberOfDotsEaten = 0                                  # Total number of dots eaten including special dots. Total dots on board = 244

    ##
    # Changes currentPac to the next Pacman in the image list
    ##
    def UpdatePac(self):
        self.currentPac += 1
        if self.currentPac == 8:
            self.currentPac = 0

    ##
    # We only have one set of sprites for Pac, so just rotate him based on direction.
    # Returns current degree rotation for Pacman
    ##
    def GetRotation(self,dx,dy):
        if(dx == 0):            # If not left or right
            if(dy == 1):        # If down
                return 270
            elif(dy == -1):     # Otherwise up
                return 90
        elif(dy == 0):          # If not up or down
            if(dx == 1):        # If right
                return 0
            elif(dx == -1):     # Otherwise left
                return 180
        return 0

    ##
    # Updates Pacman's position each frame
    ##
    def Update(self,dx,dy,speed = defaultPacSpeed):

        # True if the movement generator successfully yields
        Success = False

        # If I'm frozen, check our timer
        if(self.freeze):
            self.CheckFreeze()
        
        # If I'm not frozen
        if(not self.freeze):
            
            # Try to use our current generator to move us between squares
            try:
                Success = next(self.movementInterpolator)

            # If the generator has completed, that must mean we are once again
            # located in a grid square and can change directions/speed and stuff
            except:

                # Update our speed
                self.speed = speed

                # Create a new generator with our desired direction
                self.movementInterpolator = self.Move(dx,dy)

                # Try to use it again
                try:
                    Success = next(self.movementInterpolator)
                
                # If it didn't work, we're probably just stopped. No biggie
                except:
                    pass
        
        # Draw Pac on the screen
        screen.blit(pygame.transform.rotate(self.pacList[self.currentPac], 
                                            self.GetRotation(self.deltaX,self.deltaY)), 
                                            self.GetPixelCoordsForDraw())

        # If Success is true, that must mean the generator did its thing so we can change
        # the openness of Pacman's mouth. If Success is false, that must mean we are currently
        # stopped or the game is broken
        if Success:
            self.UpdatePac()
        else:
            self.currentPac = 0