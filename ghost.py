from entity import *

##
# A little class for referencing modes for ghosts
##
class Mode(Enum):
    chase = 0
    scatter = 1
    frightened = 2

##
# Class containing properties and functions used by all ghosts. Inherits from Entity located in entity.py
##
class Ghost(Entity):

    # Class level variables which don't need to be instanced between ghosts
    ghostImgEyesD = pygame.image.load("pictures/eyesD.png")                     # Just the ghost eyes looking down
    ghostImgEyesU = pygame.image.load("pictures/eyesU.png")                     # Just the ghost eyes looking up
    ghostImgEyesL = pygame.image.load("pictures/eyesL.png")                     # Just the ghost eyes looking left
    ghostImgEyesR = pygame.image.load("pictures/eyesR.png")                     # Just the ghost eyes looking right
    pointsImg200 = pygame.image.load("pictures/200.png")                        # 200 points!
    pointsImg400 = pygame.image.load("pictures/400.png")                        # 400 points :)
    pointsImg800 = pygame.image.load("pictures/800.png")                        # 800 points :D
    pointsImg1600 = pygame.image.load("pictures/1600.png")                      # 1600 points :O
    ghostImgFrightBlue = pygame.image.load("pictures/frightened1.png")          # Blue frightened sprite
    ghostImgFrightWhite = pygame.image.load("pictures/frightened1.png")         # White frightened sprite NOTE: Haven't actually implemented the white images yet
    currentPointsMulti = -1                                                     # A variable used to get the proper points image from pointsList
    pointsList = [pointsImg200,pointsImg400,pointsImg800,pointsImg1600]         # A list with consecutive points values. Points go up if Pac eats more than one ghost on a single frighten

    def __init__(self,                                      # self... duh
                 name,                                      # This ghost's name
                 x,                                         # This ghost's current position x coord
                 y,                                         # This ghost's current position y coord
                 scatterPos,                                # Where this ghost heads to in "scatter" mode
                 ghostHouseRefLocX,                         # This ghost's position x coord in the ghost house
                 ghostHouseRefLocY,                         # This ghost's position y coord in the ghost house
                 ghostImgD,                                 # Image of this ghost eyes down
                 ghostImgU,                                 # Image of this ghost eyes up
                 ghostImgL,                                 # Image of this ghost eyes left
                 ghostImgR,                                 # Image of this ghost eyes right
                 pacRef,                                    # A reference to Pacman
                 speed = defaultGhostSpeed,                 # The speed of this ghost
                 debug = False):                            # True if we want to show debug messages for this ghost

        super().__init__(name,x,y,speed,debug)              # Call Entity with info common among all entities

        self.pacRef = pacRef                                # Reference to Pacman
        
        self.targetX = 0                                    # Current target's x-coord
        self.targetY = 0                                    # Current target's x-coord

        self.inGhostHouse = True                            # True if currently in ghost house
        self.leavingGhostHouse = False                      # True if we are exiting the ghost house
        self.enteringGhostHouse = False                     # True if we are leaving the ghost house
        self.setTargetToEnterGhostHouse = False             # True if we need to set our target to be the ghost house
        self.hasBeenEaten = False                           # True if we have been eaten by Pacman :(
        self.ghostHouseRefLocX = ghostHouseRefLocX
        self.ghostHouseRefLocY = ghostHouseRefLocY
        self.CurrPixelOffset[0] = squareLen / 2             # Because we start in the ghost house, we need to override our starting offset            
        self.CurrPixelOffset[1] = 0                          
        self.ghostHouseEnterLocL = (13,11)                  # The spot where ghosts can enter the ghost house on the left
        self.ghostHouseEnterLocR = (14,11)                  # The spot where ghosts can enter the ghost house on the right

        self.ghostImgD = ghostImgD                          
        self.ghostImgU = ghostImgU                          
        self.ghostImgL = ghostImgL                          
        self.ghostImgR = ghostImgR                          

        self.mode = Mode.chase                              # Current mode
        self.changedModeChaseScatterEaten = False           # True if we just switched mode to chase or scatter or this ghost has been eaten
        self.changedModeFrightened = False                  # True if we just switched mode to frighened
        self.preFrightenedMode = Mode.scatter               # Mode we were in before becoming frightened so we can return to it post frighten
        
        self.scatterPos = scatterPos                        
        self.scatterCount = 0                               # Number of times we've scattered
        self.scatterTimes = [7,7,5,5]                       # Length of times for each scatter period in seconds
        self.timeBetweenScatter = 20                        # Number of seconds between scatter periods
        self.scatterTimer = -1                              # Timer for keeping track of length between scatter periods
        
        self.frightenedTimer = -1                           # Timer for keeping track of length of frighten periods
        self.maxTimeFrightened = 5                          # Max amount of time a ghost can be frightened (can be eaten to cut this short)
        self.pausedFrightenedTimer = False                  # True if we've had to pause the frighened timer due to pacman freezing us by eating one of our friends :(
        
    ##
    # Sets our target position to our scatter position
    ## 
    def Scatter(self):
        self.targetX = self.scatterPos[0]
        self.targetY = self.scatterPos[1]

    ##
    # Called when we collide with Pacman.
    ##
    def CollideWithPacman(self):

        # If I haven't already been eaten and I'm currently frightened
        if(not self.hasBeenEaten and self.mode == Mode.frightened):
            
            # Set my eaten to true
            self.hasBeenEaten = True

            # I need to head for the ghost house
            self.setTargetToEnterGhostHouse = True

            # Set to true so Update knows I can immediately change direction to whatever my pathfinding says is best
            self.changedModeChaseScatterEaten = True

            # Start my freeze process
            self.StartFreeze()

            # I've been eaten, so the next time a ghost is eaten the points will be higher
            Ghost.currentPointsMulti += 1
    
    ##
    # Called when I become frightened
    ##
    def Frightened(self):

        # If I'm not already frightened
        if (not self.hasBeenEaten):
            
            # Store the mode I was in before I became frightened so I can return to it
            self.preFrightenedMode = self.mode

            # Set my mode to frighened
            self.mode = Mode.frightened

            # Store whatever the current elapsed time is on the scatter timer so I can restore it later
            self.scatterTimer = pygame.time.get_ticks() - self.scatterTimer

            # Get the current time for tracking how long I've been frightened
            self.frightenedTimer = pygame.time.get_ticks()

            # Set to true so Update knows I should immediately reverse direction as per original Pacman
            self.changedModeFrightened = True

            # Set this to false just in case it was somehow true. Don't see how that's possible but w/e
            self.changedModeChaseScatterEaten = False

            if(self.debug):
                print("%s pausing scatter timer at: %d. New mode: %s" % (self.name, self.scatterTimer, self.mode))             

    ##
    # Called whenever we want to check our frighen timer
    ##
    def CheckFrighten(self):
        
        # If 1. I'm not frozen
        #    2. My current mode is frighened
        #    3. The time elapsed since I became frighened is greater than the time I should be allowed to stay frightened
        if(not self.freeze and self.mode == Mode.frightened and ((pygame.time.get_ticks() - self.frightenedTimer) / 1000 >= self.maxTimeFrightened)):

            if(self.debug):
                print("%s frightened timer up! Value: %d. New mode: %s" % (self.name, self.frightenedTimer, self.preFrightenedMode))

            # Set my mode back to the mode I was in before becoming frightened
            self.mode = self.preFrightenedMode

            # Set to true so Update knows I can immediately change direction to whatever my pathfinding says is best
            self.changedModeChaseScatterEaten = True

            # Restore my scatter timer by offsetting the current time with the elapsed time I stored in self.scatter timer when Frighten() was called
            self.scatterTimer = pygame.time.get_ticks() - self.scatterTimer

            if(self.debug):
                print("%s offset scatter timer: %d" % (self.name, self.scatterTimer))
            
            # Reset the points multiplier
            Ghost.currentPointsMulti = -1

    ##
    # Called when we need to become frozen
    ## 
    def StartFreeze(self):

        # Call the StartFreeze() function located in Entity in entity.py
        super().StartFreeze()

        # If I'm frightened
        if(self.mode == Mode.frightened):

            # Store the elapsed time on my frightened timer so I can restore it when freeze is finished
            self.frightenedTimer = pygame.time.get_ticks() - self.frightenedTimer

            # Set this to true so when CheckFreeze() is called it knows I need to do some extra stuff in addition to calling CheckFreeze() in Entity
            self.pausedFrightenedTimer = True

            if(self.debug):
                print("%s pausing frightened timer at: %d due to freeze" % (self.name, self.frightenedTimer)) 

    ##
    # Checks the state of my freeze status
    ##
    def CheckFreeze(self):

        # Call the CheckFreeze() function located in Entity in entity.py
        super().CheckFreeze()
        
        # If I'm not frozen and I have paused my frighten timer
        if(not self.freeze and self.pausedFrightenedTimer):

            # Restore my frighten timer by offsetting the current time with the elapsed seconds I stored on self.frightenedTimer
            self.frightenedTimer = pygame.time.get_ticks() - self.frightenedTimer

            # I've restored my frightened timer, so I can set this to false
            self.pausedFrightenedTimer = False

            if(self.debug):
                print("%s offset frightened timer: %d" % (self.name, self.frightenedTimer))


    ##
    # Function which sets my target to the input
    ##
    def SetTarget(self,newX,newY):
        self.targetX = newX
        self.targetY = newY
    
    ##
    # Function checks if I've reached my current target
    ##
    def HasReachedTarget(self):
        return (self.x == self.targetX) and (self.y == self.targetY)


    ##
    # Function checks if I've reached one of the two enter/exit locations for the ghost house
    ##
    def HasReachedEnterLoc(self):
        return ((self.x == self.ghostHouseEnterLocL[0]) and (self.y == self.ghostHouseEnterLocL[1])) or ((self.x == self.ghostHouseEnterLocR[0]) and (self.y == self.ghostHouseEnterLocR[1]))
    
    ##
    # Checks if I'm currently at a restricted junction (meaning I can't turn upwards)
    ##
    def AtARestrictedJunction(self):

        # Double check that my location is in bounds. Need to do this because Move() in Entity
        # sets my location to be outside the grid when I'm swapping sides
        if(not CheckLocationBounds(self.x,self.y)):
            return

        # True if my current grid location has value equal to either one of the restricted grid values located in tools.py
        return (grid[self.y][self.x] == noDotRestricted or grid[self.y][self.x] == dotRestricted)

    ##
    # Checks if I'm at a regular junction
    ## 
    def AtAJunction(self):
        
        # Double check that my location is in bounds. Need to do this because Move() in Entity
        # sets my location to be outside the grid when I'm swapping sides
        if(not CheckLocationBounds(self.x,self.y)):
            return

        # True if my current grid location has value equal to either one of the junction grid values located in tools.py
        return (grid[self.y][self.x] == noDotJunction or grid[self.y][self.x] == dotJunction or grid[self.y][self.x] == dotSpecialJunction)

    ##
    # Returns true if I can currently turn. Ghosts aren't allowed to change directions before a junction unless they have just changed modes
    ##
    def CanTurn(self):
        return self.AtAJunction() or self.AtARestrictedJunction()
    
    ##
    # Returns whatever my image should be
    ##
    def GetImg(self):
        
        if(self.hasBeenEaten):                                          # If I've been eaten
                    
            if(self.freeze):                                            # If I'm frozen 
                return Ghost.pointsList[Ghost.currentPointsMulti]       # That must means I've just been eaten and should disply points
            
            else:                                                       # Otherwise I'm heading to the ghost house and I'm just eyes
                if ((self.deltaX,self.deltaY) == (1,0)):                # If right
                    return Ghost.ghostImgEyesR
                elif ((self.deltaX,self.deltaY) == (-1,0)):             # Elif left
                    return Ghost.ghostImgEyesL
                elif ((self.deltaX,self.deltaY) == (0,1)):              # Elif down
                    return Ghost.ghostImgEyesD
                else:                                                   # Otherwise up
                    return Ghost.ghostImgEyesU

        else:                                                           # If I haven't been eaten
            if (self.mode == Mode.frightened):  
                return Ghost.ghostImgFrightBlue  
            elif ((self.deltaX,self.deltaY) == (1,0)):                  # If right
                return self.ghostImgR
            elif ((self.deltaX,self.deltaY) == (-1,0)):                 # Elif left
                return self.ghostImgL
            elif ((self.deltaX,self.deltaY) == (0,1)):                  # Elif down
                return self.ghostImgD
            else:                                                       # Otherwise up
                return self.ghostImgU

    ##
    # Measures the distance between my TARGET grid position and the possible grid position.
    # This is used by ghosts to determine which way they should turn. Whatever yields the
    # shortest distance is the direction taken, even if that is not the shortest path as
    # per original Pacman
    ##
    def MeasureDistance(self,possibleX,possibleY):
        
        # Make possible grid location can actually be reached
        if(CheckLocationBounds(possibleX,possibleY) and grid[possibleY][possibleX] != inaccessible):

            # Distance formula
            return math.sqrt((self.targetY - possibleY)**2 + (self.targetX - possibleX)**2)
        
        # If it can't, just return some high value so this turn won't be chosen
        else:
            return 9999
    
    ##
    # Checks if this ghost should scatter and sets the appropriate variables if yes
    ##
    def ShouldScatter(self):

        # If I'm in the ghost house, or I've alrady scattered the max number of times, exit
        if(self.inGhostHouse or self.scatterCount >= len(self.scatterTimes)):
            return

        # If I haven't yet set my scatter timer, or the timer has exceeded the time between scatter periods
        if ((self.scatterTimer < 0) or ((pygame.time.get_ticks() - self.scatterTimer) / 1000 >= self.timeBetweenScatter)):

            if(self.debug):
                    print("%s scattering" % (self.name))
            
            # Get the current time for checking how long I've been scattering
            self.scatterTimer = pygame.time.get_ticks()

            # Set my mode to scatter
            self.mode = Mode.scatter

            # Let Update() know I've changed modes so I can immediately pick a new direction
            self.changedModeChaseScatterEaten = True
        
        # If I'm scattering
        if(self.mode == Mode.scatter):

            # Check if my timer has exceeded the time for this scatter period
            if ((pygame.time.get_ticks() - self.scatterTimer) / 1000 >= self.scatterTimes[self.scatterCount]):

                # Increase my scatter count so I used the next scatter value in my self.scatterTimes list
                self.scatterCount += 1

                if(self.debug):
                    print("%s chasing" % (self.name))

                # Get the current time for checking how long since my last scatter period
                self.scatterTimer = pygame.time.get_ticks()

                # Set my mode to chase. Get Pacman!
                self.mode = Mode.chase

                # Let Update() know I've changed modes so I can immediately pick a new direction
                self.changedModeChaseScatterEaten = True
    
    ##
    # Called when I can change direction. If canReverse is true, then reversing direction is a possibility,
    # if restricted is true, then turning upwards is not a possibility
    ##
    def chooseTurn(self, canReverse = False, restricted = False):

        # Used for storing the distance and direction of each possible turn choice
        choices = {}

        # If I'm moving left or right, or I'm allowed to reverse direction
        if(self.deltaX != 0 or canReverse):

            # If I'm allowed to move upwards
            if not restricted:
                
                # Get the distance from my target if I move upwards
                choices[self.MeasureDistance(self.x,self.y-1)] = (0,-1)
            
            # Get the distance from my target if I move downwards
            choices[self.MeasureDistance(self.x,self.y+1)] = (0,1)


        # If I'm moving up or down, or I'm allowed to reverse direction
        if(self.deltaY != 0 or canReverse):

            # Get the distance from my target if I move left
            choices[self.MeasureDistance(self.x-1,self.y)] = (-1,0)

            # Get the distance from my target if I move right
            choices[self.MeasureDistance(self.x+1,self.y)] = (1,0)
        
        # Also get the distance from my target if I keep going in the same direction regardless
        choices[self.MeasureDistance(self.x + self.deltaX,self.y + self.deltaY)] = (self.deltaX,self.deltaY)

        # If I'm currently frightened, then the direction I choose must be random
        if(self.mode == Mode.frightened):

            # Keep picking a random turn til I get one which doesn't go into a wall
            while(True):
                randomChoice = random.choice(list(choices.keys()))
                if(randomChoice <= 100):
                    return choices[randomChoice]                

        # Return the turn which yields the smallest distance to my target
        return (choices[min(choices)])

    ##
    # Being in the ghost house is a special case because I'm between grid squares. This function
    # causes the ghost to oscillate up and down within the ghost house
    ##
    def GhostHouseMoveGen(self):

        if(abs(self.CurrPixelOffset[1]) >= squareLen / 2):
            self.deltaY *= -1

        self.CurrPixelOffset[1] += self.deltaY * (squareLen / ghostHouseGhostSpeed)

    ##
    # Called when I'm entering or exiting the ghost house
    # entering: True if I'm entring the ghost house
    # enterExitRefX, enterExitRefY: The location outside the ghost house which I'm going to if leaving and going away from if entering
    # speed: The speed I'm travelling
    ##
    def EnterExitGhostHouseGen(self,entering,enterExitRefX,enterExitRefY,speed = ghostHouseGhostSpeed):
        
        # This will hold the target positions we care about to exit/enter the ghost house
        targetPixelValues = []
    
        # When we test if this ghost has reached a desired pixel, we check if the absolute value
        # between this ghost's pixel and the target pixel is less than my movement per frame. This way,
        # there's no way we'd overshoot the target
        moveThreshold = (squareLen / speed)

        # To avoid writing a function for exiting and a function for entering because they're doing almost the same thing,
        # our targetPixelValues goes from inside ghost house to outside ghost house. When we're exiting, our target pixels go from the 
        # start to the end of the targetPixelValues list. When entering, we go backwards through the list.

        # dirScalar is 1 if we are going forwards through targetPixelValues, and -1 if we are going backwards
        dirScalar = 1

        # counts the number of loops we've done below so we know which pixel value to access in targetPixelValues
        counter = 0

        # 1 if we are entering the ghost house from the left, or we are exiting in general
        # GHOSTS ALWAYS EXIT LEFT, BUT THEY CAN ENTER FROM EITHER DIRECTION as per original Pacman
        leftScalar = 1

        # If we're entering
        if(entering):

            # Set the dirScalar to -1 so we can go backwards through the list
            dirScalar = -1

            # Set the counter to the last index of targetPixelValues so we start there
            counter = len(targetPixelValues) - 1

            # If I'm entering from the right, set the scalar to -1 so when I'm calculating my pixel offset I remain in the proper position
            if(self.x == self.ghostHouseEnterLocR[0]):
                leftScalar = -1

        if(self.debug):
            print("%s starting house enter/leave generator. xpos: %d ypos: %d xoffset: %d yoffset: %d" % (self.name,self.x,self.y,self.CurrPixelOffset[0],self.CurrPixelOffset[1]))


        # Stores the target pixels at each step in the entering/exiting process. We do some mulitiplication with leftScalar to make sure the ghost doesn't look weird
        # when entering from the right
        targetPixelValues = [ ((self.ghostHouseRefLocX * squareLen) - squareOffset + (squareLen / 2)        , ((self.ghostHouseRefLocY * squareLen) - squareOffset)),
                              ((enterExitRefX * squareLen)- squareOffset + (leftScalar * (squareLen / 2))   , ((self.ghostHouseRefLocY * squareLen) - squareOffset)),
                              ((enterExitRefX * squareLen) - squareOffset + (leftScalar * (squareLen / 2))  , ((enterExitRefY * squareLen) - squareOffset)),
                              ((enterExitRefX * squareLen) - squareOffset                                   , (enterExitRefY * squareLen) - squareOffset)
                            ]

        # We want to loop for the length of targetPixelValues. We don't actually use the x variable though because if we're entering
        # we want to walk backwards through the targetPixelValues list
        for x in range(len(targetPixelValues)):
            
            # Get my target x and y pixels from the list
            targetXPixel = targetPixelValues[counter][0]
            targetYPixel = targetPixelValues[counter][1]

            # Calculate my current pixels
            currentXPixel = (self.x * squareLen) - (squareOffset) + self.CurrPixelOffset[0]
            currentYPixel = (self.y * squareLen) - (squareOffset) + self.CurrPixelOffset[1]

            if(self.debug):
                print("%s target x pixel: %d, current x pixel: %d, current x offset: %d" % (self.name, targetXPixel, currentXPixel, self.CurrPixelOffset[0]))
                print("%s target y pixel: %d, current y pixel: %d, current y offset: %d" % (self.name, targetYPixel, currentYPixel, self.CurrPixelOffset[1]))

            # mustMoveLR is true if my x pixel doesn't match the target x pixel, meaning I need to move left or right
            mustMoveLR = abs(targetXPixel - currentXPixel) >= moveThreshold

            # mustMoveUD is true if my y pixel doesn't match the target y pixel, meaning I need to move up or down
            mustMoveUD = abs(targetYPixel - currentYPixel) >= moveThreshold

            # If I need to move left/right set my direction appropriately so the proper ghost image is displayed
            # and my offset is changing in the correct direction
            if(mustMoveLR and targetXPixel > currentXPixel):
                self.deltaX = 1
            elif(mustMoveLR):
                self.deltaX = -1
            
            # If I need to move up/down set my direction appropriately so the proper ghost image is displayed
            # and my offset is changing in the correct direction
            if(mustMoveUD and targetYPixel > currentYPixel):
                self.deltaY = 1
            elif(mustMoveUD):
                self.deltaY = -1

            if(self.debug):
                print("%s mustMoveLR: %s, mustMoveUD: %s" % (self.name, mustMoveLR, mustMoveUD))
                print("%s x dir: %d, y dir: %d" % (self.name,self.deltaX,self.deltaY))

            # While I still need to move to reach my target pixel
            while(mustMoveLR or mustMoveUD):
                
                # If I need to move left/right
                if(mustMoveLR):

                    # Increase my current pixel offset by my speed times my movement direction
                    self.CurrPixelOffset[0] += self.deltaX * moveThreshold

                    # Recalculate my current pixel x coord
                    currentXPixel = (self.x * squareLen) - (squareOffset) + self.CurrPixelOffset[0]

                    # Check if I still need to move left/right
                    mustMoveLR = abs(targetXPixel - currentXPixel) >= moveThreshold

                    if(self.debug):
                        print("%s updated x pixel loc: %d, distance from goal: %d" % (self.name,currentXPixel,abs(targetXPixel - currentXPixel)))

                # If I don't need to move left/right, make sure my deltaX is 0
                else:
                    self.deltaX = 0

                # If I need to move up/down
                if(mustMoveUD):

                    # Increase my current pixel offset by my speed times my movement direction
                    self.CurrPixelOffset[1] += self.deltaY * moveThreshold
                    
                    # Recalculate my current pixel y coord
                    currentYPixel = (self.y * squareLen) - (squareOffset) + self.CurrPixelOffset[1]
                    
                    # Check if I still need to move up/down
                    mustMoveUD = abs(targetYPixel - currentYPixel) >= moveThreshold
                    
                    if(self.debug):
                        print("%s updated y pixel loc: %d, distance from goal: %d" % (self.name,currentYPixel,abs(targetYPixel - currentYPixel)))
 
                # If I don't need to move up/down, make sure my deltaY is 0   
                else:
                    self.deltaY = 0

                # Keep yielding so Update() doesn't try to create a new generator. I need to yield until I've completed
                # movement toward all pixels in targetPixelValues
                yield True
            
            # Increment the counter by dirScalar so it goes +1 if we are moving forward through the list and -1 if we are moving backward
            counter += dirScalar

        # If I'm entering
        if(entering):

            # Set my current position to be my position in the ghost house
            self.x = self.ghostHouseRefLocX
            self.y = self.ghostHouseRefLocY

            # Set my offset to be the default offset for being in the ghost house
            # NOTE: we're always using the grid squre to the left of our desired position
            #       within the ghost house for reference
            self.CurrPixelOffset[0] = 10
            self.CurrPixelOffset[1] = 0

            # I'm in the ghost house
            self.inGhostHouse = True
            
            # Because I've entered the ghost house, that must mean I was been eaten. Reset my eaten variable
            self.hasBeenEaten = False

        # I must be leaving
        else:
            
            # Set my current position to be the exit position passed in
            self.x = enterExitRefX
            self.y = enterExitRefY

            # Reset my pixel offsets to zero
            self.CurrPixelOffset[0] = 0
            self.CurrPixelOffset[1] = 0

        # Yield here to avoid having my pixel offset reset to 0,0. If I didn't have this here, then Update() would immediately
        # try to create a new generator, and that would mean it would reset my pixel offset. If I've just entered the ghost house,
        # I would jump 10 pixels to the left for a frame before restarting this function to exit the ghost house. This is a little
        # workaround to avoid that. It does cause this ghost to remain in place for one frame too long when exiting, but at 60fps
        # that's fine
        yield True

    ##
    # Updates this ghost's position each frame
    ##
    def Update(self, targetX = None,targetY = None,speed = defaultGhostSpeed):
        
        # True if the movement generator successfully yields
        Success = False


        # If no targetX or targetY values were passed in, set them to my current target
        if targetX == None or targetY == None:
            targetX = self.targetX
            targetY = self.targetY

        
        # If I'm frozen, check if I should still be frozen
        if(self.freeze):
            self.CheckFreeze()
        
        # If I'm in the ghost house and I'm not frozen, run my ghost house oscillator function
        if (self.inGhostHouse and not self.freeze):
            self.GhostHouseMoveGen()

        # If I'm supposed to set my target to be the ghost house
        elif(self.setTargetToEnterGhostHouse):

            # Set my target to be the left ghost house enter square no matter what. It doesn't
            # really matter because we always enter from whichever enter point we reach first
            self.SetTarget(self.ghostHouseEnterLocL[0],self.ghostHouseEnterLocL[1])

            # I've set my target so this can be false
            self.setTargetToEnterGhostHouse = False

            # I'm entering the ghost house (even though I probably haven't reached it yet)
            self.enteringGhostHouse = True

        # If I'm leaving the ghost house
        elif (self.leavingGhostHouse):

            # Create the movement generator with entering = false and reference location = left ghost house enter/exit square
            self.movementInterpolator = self.EnterExitGhostHouseGen(False,self.ghostHouseEnterLocL[0],self.ghostHouseEnterLocL[1])

            # Set this to false so we dont't try to create another generator leave the house
            self.leavingGhostHouse = False

            # Set this to false just in case it was somehow true
            self.enteringGhostHouse = False

            if(self.debug):
                print("%s leaving ghost house" % (self.name))

        # If I'm entering the ghost house and I've reached an enter/exit square
        elif (self.enteringGhostHouse and self.HasReachedEnterLoc()):

            # Create the movement generator with entering = true and reference location = my current square
            self.movementInterpolator = self.EnterExitGhostHouseGen(True,self.x,self.y,eatenGhostSpeed)

            # Set this to false just in case it was somehow true
            self.leavingGhostHouse = False

            # Set this to false so we dont't try to create another generator to enter the house
            self.enteringGhostHouse = False

        # If I'm not in the ghost house and I'm not frozen
        if(not self.inGhostHouse and not self.freeze):

            # Try to update our location using our current movement generator
            try:
                Success = next(self.movementInterpolator)

            # It that failed, we must need a new movement generator
            except:

                # If I'm at a slowdown grid (ghosts slowdown in the side warp lanes as per original Pacman)
                if grid[self.y][self.x] == slowdown:
                    self.speed = slowdownGhostSpeed

                # If I've been eaten, then I must be heading back to the ghost house so I should go extra fast
                elif (self.hasBeenEaten):
                    self.speed = eatenGhostSpeed

                # Otherwise, set my speed to be whatever was passed into the function
                else:
                    self.speed = speed

                # Set my target to be the input target
                self.SetTarget(targetX,targetY)

                # Set my direction to be whatever my current direction is by default
                newDir = (self.deltaX,self.deltaY)
                

                # If I've changed mode to chase, scatter, or if I've been eaten
                if(self.changedModeChaseScatterEaten):

                    # Then I need to get a new direction and I'm allowed to reverse
                    newDir = self.chooseTurn(True,False)

                    # Set this to false so I'm not allowed to reverse until this is true again
                    self.changedModeChaseScatterEaten = False

                # If I've changed my mode to frightened, then I must reverse directions
                elif(self.changedModeFrightened):

                    # Reverse my current direction
                    newDir = (self.deltaX * -1, self.deltaY * -1)

                    # Set this to false so I don't do this again unintentionally
                    self.changedModeFrightened = False

                # If I'm at a junction, then I can turn
                elif self.AtAJunction():

                    if(self.debug):
                        print("%s at junction x:%d y:%d" % (self.name,self.x, self.y))
                    
                    # canReverse = false, restricted = false by default
                    newDir = self.chooseTurn()

                # If I'm at a junction, I can turn but not upwards as per orignial Pacman
                elif self.AtARestrictedJunction():

                    if(self.debug):
                        print("%s at restricted junction" % (self.name))
                    
                    # canReverse = false, restricted = true
                    newDir = self.chooseTurn(False,True)
                
                # Create a new movement generator based on the direction I'm travelling
                self.movementInterpolator = self.Move(newDir[0],newDir[1])

                # Update my position with the generator
                try:
                    Success = next(self.movementInterpolator)

                # If that didn't work, something is very wrong
                except:
                    print("%s CAN'T MOVE" % self.name)
        
        # Draw this ghost
        screen.blit(self.GetImg(), self.GetPixelCoordsForDraw())