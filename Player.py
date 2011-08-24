import pygame
import Configuration
import SpriteSheet
import Utils
class Player(pygame.sprite.Sprite):
    Location=[0,0]
    
    def __init__(self,num):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [
            SpriteSheet.SpriteStripAnim(
                Utils.ImagePath("Character0%i.png"%num), 
                (0,48*i,32,38),4,(0,0,0),True,10
            )
            for i in xrange(4)
        ]
        self.animation = self.sprites[0]
    
    _Velocity=[0,0]
    
    @property
    def Velocity(self):
        """Velocity property of a player.
        This automatically starts/stops animation"""
        return self._Velocity
    
    @Velocity.setter
    def Velocity(self,val):
        self._Velocity = val
        if val==[0,0]:
            self.animation.stop()
            return
        elif self._Velocity[1]>0:
            self.animation = self.sprites[0]
        elif self._Velocity[0]<0:
            self.animation = self.sprites[1]
        elif self._Velocity[0]>0:
            self.animation = self.sprites[2]
        else:
            self.animation = self.sprites[3]
        self.animation.iter()#starts animation.
    
    def update(self):
        self.Location[0]+=self._Velocity[0]
        self.Location[1]+=self._Velocity[1]
        self.image = self.animation.next()

class HumanPlayer(Player):
    def handleKey(self, event):
        if event.key == pygame.K_LSHIFT:
            factor = 3
            if event.type==pygame.KEYUP:
                factor = 1.0/factor #invert the factor
                
            v[0] = v[0]*factor
            v[1] = v[1]*factor
            self.Velocity = v
            return True
           
        if event.key not in Configuration.Keys:
            return False #Not a key we use... yet
        
        newDir = Configuration.Keys.index(event.key)
        scale = 1
        if event.type == pygame.KEYUP:
            scale = -1
        
        v = self.Velocity
        v[0] += scale*[0,-1,1,0][newDir]
        v[1] += scale*[1,0,0,-1][newDir]
        self.Velocity = v
        return True
        
        
        
        
        
        
        
        
        
        
        
        
            