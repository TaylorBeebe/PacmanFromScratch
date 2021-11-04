from tools import *

## 
# Entity is the highest level class for our characters. It contains functions and variables common to both the Pacman and the ghosts
##
class Entity(object):
    def __init__(self,name, x, y, speed, debug = False):
        self.x = x                              # This entity's current x position aligned to grid
        self.y = y                              # This entity's current y position aligned to grid
        self.deltaX = -1                        # This entity's current x direction
        self.deltaY = 0                         # This entity's current y direction
        self.speed = speed                      # This entity's current speed
        self.movementInterpolator = None        # Whenever moving, we create a generator to interpolate between squares
        self.name = name                        # This entity's name
        self.debug = debug                      # True if this entity should print debug info
        self.CurrPixelOffset = [0,0]            # Stores this entity's current pixel offset used when moving between squares
        self.freeze = False                     # True if this entity should freeze in place
        self.freezeTimer = -1                   # Timer for setting how long this entity should freeze     
        self.timeToFreeze = 1.5                 # Length of time to freeze in seconds                        

    ##
    # This gets the actual pixel coordinates of the grid location at which we draw this entity
    ##
    def GetPixelCoordsForDraw(self):
        return((self.x * squareLen) - squareLen/4 + self.CurrPixelOffset[0], (self.y * squareLen) - squareLen/4 + self.CurrPixelOffset[1])
    
    ##
    # This gets the pixel location of the center of this entity used for collision detection
    ##
    def GetPixelCoordsForCollision(self):
        return((self.x * squareLen) + squareLen / 2 + self.CurrPixelOffset[0], (self.y * squareLen) + squareLen / 2 + self.CurrPixelOffset[1])
    
    ##
    # Returns this entity's x and y coordinates of this entity in a tuple
    ##
    def GetPos(self):
        return (self.x,self.y)
    
    ##
    # Sets this entity's position to the input
    ##
    def SetPos(self,x,y):
        self.x = x
        self.y = y
    
    ##
    # I decided to make freeze functions common to all entity's. It would be more difficult to make freeze into like
    # a globabl boolean because in the original Pacman, if a ghost had been eaten and was heading back to the ghost house 
    # then they are exempt from freezing.
    ##
    def StartFreeze(self):
        
        # Get the current time so we can check later how long we have been frozen
        self.freezeTimer = pygame.time.get_ticks()

        # I am now frozen
        self.freeze = True

        if(self.debug):
            print("%s now frozen" % self.name)
    
    ##
    # This checks if 
    # 1. I am frozen
    # 2. If the time elapsed since I started being frozen has exceeded the amount of time I'm supposed to be frozen.
    # If both are true, then I set my frozen variable to false
    ##
    def CheckFreeze(self):
        
        if(self.freeze and ((pygame.time.get_ticks() - self.freezeTimer) / 1000 >= self.timeToFreeze)):
            self.freeze = False


    ##
    # Returns the direction of this entity in a tuple
    ##
    def GetDir(self):
        return(self.deltaX,self.deltaY)

    ##
    # Sets this entity's direction to the input
    ##
    def SetDir(self,dx,dy):
        self.deltaX = dx
        self.deltaY = dy

    ##
    # Checks if this entity and some other entity passed in (otherRef) are currently colliding.
    # collisionPixelThreshold is stored in tools.py right now
    ##
    def CheckCollision(self,otherRef):
        myPixel = self.GetPixelCoordsForCollision()
        theirPixel = otherRef.GetPixelCoordsForCollision()
        return math.sqrt((myPixel[1] - theirPixel[1])**2 + (myPixel[0] - theirPixel[0])**2) <= collisionPixelThreshold
    
    ##
    # A Generator which "interpolates" this entity's position between grid squares.
    # Every time we yield, it means we've updated our CurrPixelOffset, so next time we are
    # drawn we will be in a different offset than before so it will look like we're moving.
    # Once this entity has reached their grid location, the generator stops yielding and a new 
    # one must be created to interpolate this entity to his next grid. This generator is created
    # in each subclass's unique "Update()" function. Note that we aren't actually yielding anything
    # that important, this is just a simple way to make sure that once we're done yeilding, this entity
    # is located at the next grid square.
    ##
    def Move(self,dx,dy):

        # Special cases occur if we are warping between sides. We can tell if this is the case
        # By checking if our current destination will take us to either (28,14) or (-1,14)
        # NOTE: In the case that we are going to (-1,14), our calculations take us to a negative
        #       pixel value which pygame seems to be okay with :)
        swappingSidesL2R = ((self.x + dx == -1) and (self.y + dy == 14))
        swappingSidesR2L = ((self.x + dx == 28) and (self.y + dy == 14))

        # Sets our current speed. Speed is just the number of pixels we move each frame
        speed = squareLen / self.speed

        # Make sure the direction we want to go (dx,dy) will not take us to a wall. 
        # If it won't, set that as the direction to which we are moving. Also set it to the direction we
        # are moving if we are about to swap sides
        if (swappingSidesL2R or swappingSidesR2L or grid[self.y + dy][self.x + dx] <= maxMovableGridSquareValue):
            self.deltaX = dx
            self.deltaY = dy
            if(self.debug):
                print("%s in move generator, new Direction: (%d,%d)" % (self.name,self.deltaX,self.deltaY))

        # We check this one more time because in the last if statement, we set our deltaX and deltaY to the input only if it's a
        # valid move. In this case, we double check that the current value of deltaX and deltaY will still be a valid move. This
        # is how we avoid allowing Pacman or one of the ghosts to turn mid-wall and come to a stop
        if (swappingSidesL2R or swappingSidesR2L or grid[self.y + self.deltaY][self.x + self.deltaX] <= maxMovableGridSquareValue):

            # self.speed is the number of frames it takes for this entity to reach the next square
            # and we use it to evenly move between squares.
            # NOTE: we expect that whatever set our self.speed variable did so by dividing the length of a grid square by some value
            #       this is handled at the start of this function.
            for step in range(self.speed):
                self.CurrPixelOffset[0] = float(step) * float(self.deltaX) * speed
                self.CurrPixelOffset[1] = float(step) * float(self.deltaY) * speed
                yield True                                                   
            
            # If we're switching sides, set our grid location to be the opposite side of the board so we can run Move() again 
            # to finish the movement.
            if(swappingSidesL2R):
                self.x = 28
                self.y = 14
            elif(swappingSidesR2L):
                self.x = -1
                self.y = 14

            # If we're swapping sides
            if (swappingSidesL2R or swappingSidesR2L):

                if(self.debug):
                    print("%s swapping sides" % (self.name))
                
                # Yield another generator so we are forced into moving one more square (to get to
                # the other side) before being allowed to change directions
                yield from self.Move(self.deltaX,self.deltaY)

                if(self.debug):
                    print("%s completed swapping" % (self.name))

            # If we're not swapping sides, update our position and finish the function
            else:
                self.x += self.deltaX
                self.y += self.deltaY
                if(self.debug):
                    print ("%s Pos = (%d,%d), Dir = (%d,%d)" % (self.name,self.x, self.y, self.deltaX, self.deltaY))

            # Since we're now located at a grid squre, we can reset our offset values
            self.CurrPixelOffset[0] = 0
            self.CurrPixelOffset[1] = 0
