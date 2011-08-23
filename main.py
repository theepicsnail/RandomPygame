import pygame
import Configuration
import Player
import Utils
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
grassImage = pygame.image.load(Utils.ImagePath("grass.jpg"))

player = Player.HumanPlayer(1)#num = which sprite to use.
		
def handleKey(event):
    global player,DEBUG
    
    if player.handleKey(event):
        return;
        
    if event.key==293:#F12
        DEBUG=(event.type==pygame.KEYDOWN)
    else:
        print event
    #f event.key
        
    
def displayDebug():
    gameprint("Loc:%r"%PlayerLoc,0,0,(0,0,0))
    gameprint("Vel:%r"%PlayerVel,0,20,(0,0,0))
    
while True:
    time_passed = clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            handleKey(event)
            
    player.update()
    draw_background(screen,grassImage,map(lambda x:x/-2,player.Location))
    screen.blit(player.image,player.Location)
    
    if DEBUG:
        displayDebug();
    pygame.display.flip()
    
    
    
    
    
    
    
    
    
    