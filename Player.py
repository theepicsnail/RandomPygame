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
    pressed = set()
    running = False
    def handleEvent(self, event):
        if event.type==pygame.KEYDOWN:
            self.pressed|=set([event.key])
        elif event.type==pygame.KEYUP:
            self.pressed-=set([event.key])
        else:
            return False # we only care about keyboard events
        
        if event.key == Configuration.SPEED:
            self.running = (Configuration.SPEED in self.pressed)
            self.recomputeVelocity()
            return True
        if event.key in Configuration.Keys:
            self.recomputeVelocity()
            return True
            
        return False# we did not use the key.
            
    def recomputeVelocity(self):
        dirs = Configuration.Keys & self.pressed
        v = [0,0]
        amp = 3 if self.running else 1
        if Configuration.RIGHT in dirs:    v[0]+=amp
        if Configuration.LEFT  in dirs:    v[0]-=amp
        if Configuration.DOWN  in dirs:    v[1]+=amp
        if Configuration.UP    in dirs:    v[1]-=amp
        self.Velocity = v
        
class AutoWalkHumanPlayer(HumanPlayer):
    target = None
    def handleEvent(self,event):
        HumanPlayer.handleEvent(self,event)
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                self.target = Utils.tupleSum(event.pos,(-16,-32))
                print "Set target:",self.target
            if event.button==3:
                if self.target!=None:
                    self.Velocity=[0,0]
                self.target = None
                print "Unset target."
    def update(self):
        HumanPlayer.update(self)
        if self.target == None:
            return
        
        v = [0,0]
        if self.target[0] < self.Location[0]:
            v[0]=-1
            
        if self.target[0] > self.Location[0]:
            v[0]=1
            
        if self.target[1] < self.Location[1]:
            v[1]=-1
            
        if self.target[1] > self.Location[1]:
            v[1]=1
            
        if v != self.Velocity:
            self.Velocity = v
        
        
        
        