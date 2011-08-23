
# Size of break-out blocks
block_width=23
block_height=15
 
# This class represents each block that will get knocked out by the ball
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self,color,x,y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])
 
        # Fill the image with the appropriate color
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y
 
# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):
    # Speed in pixels per cycle
    speed = 10.0
     
    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0
     
    # Direction of ball (in degrees)
    direction = 200
 
    width=10
    height=10
     
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])
         
        # Color the ball
        self.image.fill(white)
         
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
         
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
     
    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self,diff):
        self.direction = (180-self.direction)%360
        self.direction -= diff
     
    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
         
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
         
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
         
        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y=1
             
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360-self.direction)%360
            self.x=1
             
        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth-self.width:
            self.direction = (360-self.direction)%360
            self.x=self.screenwidth-self.width-1
         
        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False
         
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
         
        self.width=75
        self.height=15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
         
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.topleft = (0,self.screenheight-self.height)
     
    # Update the player
    def update(self):
        # Get where the mouse is
        pos = pygame.mouse.get_pos()
        # Set the left side of the player bar to the mouse position
        self.rect.left = pos[0]
        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.left > self.screenwidth - self.width:
            self.rect.left = self.screenwidth - self.width
 
 