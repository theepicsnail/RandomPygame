import pygame
import Configuration
import Player
import Utils
import World
#test
"""
class Grass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(Utils.ImagePath("grass.jpg"))
		self.rect = self.image.get_rect()
class Character(pygame.sprite.Sprite):
	def __init__(self,num=1):
		pygame.sprite.Sprite.__init__(self)
		self.imageSheet = pygame.image.load(Utils.ImagePath("tori_gaku_0%s.png"%num))
		self.images=[]
		for dir in range(4):#down left right up
			curAnim=[]
			for state in range(4):
				rect = pygame.Rect([state*32,dir*48,32,48])
				image = pygame.Surface(rect.size).convert()
				image.blit(self.sheet, (0, 0), rect)
				curAnim.append(image)
			self.images.append(curAnim)
		self.image=self.images[0][0]
		self.rect = self.image.get_rect()
		"""
		
	
def draw_background(screen, tile_img, offset=(0,0)):
    img_rect = tile_img.get_rect()
    xoff = offset[0]%img_rect.width
    yoff = offset[1]%img_rect.height
    
    nrows = int(screen.get_height() / img_rect.height) + 2
    ncols = int(screen.get_width() / img_rect.width) + 2
    
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = ((x-1) * img_rect.width+xoff, 
                                (y-1) * img_rect.height+yoff)
            screen.blit(tile_img, img_rect)
	
def gameprint(text,xx,yy,color):
   font = pygame.font.SysFont("Courier New",18)
   ren = font.render(text,1,color)
   screen.blit(ren, (xx,yy))

DEBUG=False 
pygame.init()
clock = pygame.time.Clock()

pygame.mixer.music.load(Utils.AudioPath("bg.mp3"))
#pygame.mixer.music.play(-1,-10);#count,position(sec)

screen=pygame.display.set_mode(Configuration.ScreenSize)
grassImage = pygame.image.load(Utils.ImagePath("stone.jpg"))

player = Player.AutoWalkHumanPlayer(1)#num = which sprite to use.
		
def handleEvent(event):
    global player,DEBUG
    if DEBUG:
        print event
    if player.handleEvent(event):
        return;
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        if event.key==293:#F12
            DEBUG^=(event.type==pygame.KEYDOWN)
            return 
    
    #f event.key
        
    
def displayDebug():
    global player
    gameprint("Loc:%r"%player.Location,0,0,(0,0,0))
    gameprint("Vel:%r"%player.Velocity,0,20,(0,0,0))
    
running = True
level = World.Level()
level.loadLevel("level.lvl")

maxCamPos = [level.width - Configuration.ScreenSize[0]/2,
            level.height - Configuration.ScreenSize[1]/2]
def updateCamera(ploc):
    if ploc[0] < Configuration.ScreenSize[0]/2:
        cx = 0
        px = ploc[0]
    elif ploc[0] < maxCamPos[0]:
        px =  Configuration.ScreenSize[0]/2
        cx = ploc[0]-px
    else:
        cx = level.width - Configuration.ScreenSize[0]
        px = ploc[0] - cx
    if ploc[1] < Configuration.ScreenSize[1]/2:
        cy = 0
        py = ploc[1]
    elif ploc[1] < maxCamPos[1]:
        py =  Configuration.ScreenSize[1]/2
        cy = ploc[1]-py
    else:
        cy = level.height- Configuration.ScreenSize[1]
        py = ploc[1] - cy
    
    return -cx,-cy,px,py
while running:
    time_passed = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        handleEvent(event)
    
    #jumps it to 5-8
    #draw_background(screen,grassImage,(0,0))#map(lambda x:x/-2,player.Location)
    # 2-4
    cx,cy,px,py = updateCamera(player.Location)
    
    screen.blit(level.image,(cx,cy))
    
    player.update()
    screen.blit(player.image,(px,py))
    
    if DEBUG:
        displayDebug();
    pygame.display.flip()
    
    
    
    
    
    
    
    
    
    
