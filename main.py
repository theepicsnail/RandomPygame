import pygame
import Utils
import SpriteSheet
import Configuration
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
		
		
	
def draw_background(screen, tile_img):
    img_rect = tile_img.get_rect()
    
    nrows = int(screen.get_height() / img_rect.height) + 1
    ncols = int(screen.get_width() / img_rect.width) + 1
    
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = (x * img_rect.width, 
                                y * img_rect.height)
            screen.blit(tile_img, img_rect)
	
		
pygame.init()
clock = pygame.time.Clock()

pygame.mixer.music.load(Utils.AudioPath("bg.mp3"))
pygame.mixer.music.play(-1,0);
screen=pygame.display.set_mode(Configuration.ScreenSize)
grassImage = pygame.image.load(Utils.ImagePath("grass.jpg"))

ss = [
	SpriteSheet.SpriteStripAnim(Utils.ImagePath("tori_gaku_01.png"), (0,48*i,32,38),4,(0,0,0),True,10)
	for i in xrange(4)
]
anim = ss[0]
anim.iter()
anim.stop()
			
PlayerLoc = [0,0]
PlayerVel = [0,0]
def handleKey(event,pressed):
    global anim,PlayerVel
    try:
        newDir = Configuration.Keys.index(event.key)
        scale = 1
        if not pressed:
            scale = -1
        
        
        PlayerVel[0] += scale*[0,-1,1,0][newDir]
        PlayerVel[1] += scale*[1,0,0,-1][newDir]
        
        if PlayerVel==[0,0]:
            anim.stop()
            return
        elif PlayerVel[1]==1:
            anim=ss[0]
        elif PlayerVel[0]==-1:
            anim=ss[1]
        elif PlayerVel[0]==1:
            anim=ss[2]
        else:
            anim=ss[3]
        anim.iter()
            
    except:
        print event,pressed
        
def updatePlayer(dt):
    global PlayerLoc,PlayerVel
    PlayerLoc[0]+=PlayerVel[0]*dt/10.0
    PlayerLoc[1]+=PlayerVel[1]*dt/10.0
    
while True:
    time_passed = clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        elif event.type == pygame.KEYDOWN:
            handleKey(event,True)
        elif event.type == pygame.KEYUP:
            handleKey(event,False)
            
    updatePlayer(time_passed) 
    draw_background(screen,grassImage)
    screen.blit(anim.next(),PlayerLoc)
    pygame.display.flip()
    
    
    
    
    
    
    
    
    
    