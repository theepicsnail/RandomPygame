import pygame
import Utils
import SpriteSheet
try:
    from zlib import decompress
except:
    decompress = lambda x:x



class Cell(pygame.sprite.Sprite):
    Clipping = False
    
class Layer:
    cellData=[]
    width = 0
    height = 0
    properties = {}
    name = ""
    sheet = None
    def __init__(self,l,sheet):
        self.sheet = sheet
        self.name = l[0]
        self.properties = dict(l[1])
        start = None
        data = []
        for i in l[2]:
            if type(i)==tuple:
                if start != None:
                    self.cellData.append((start,data))
                    data = []
                start = i
            else:
                data.append(Utils.num2pos(i))
        if start != None:
            self.cellData.append((start,data))
    def __getitem__(self,item):
        print "get:",self.name,item,self.properties
        try:
            return eval(self.properties[item])
        except:
            print "exception"
            return True
    def render(self,image,collision):
        for (pos,vals) in self.cellData:
            print pos
            r,c=pos
            for v in vals:
                image.blit(self.sheet[v[1]*32,v[0]*32,32,32],(c*32,r*32))
                c=c+1
                if c == self.width:
                    r=r+1
                    c=0
            
class Level(pygame.sprite.Sprite):
    path = None
    staticLayer = None
    layers = []
    width = 0
    height = 0
    columns = 0
    rows = 0
    cellSize = 32
    collision = []
    sheet = None
    
    def __init__(self):
        self.sheet = SpriteSheet.SpriteSheet(Utils.ImagePath("town01.png"))
        pass
    def __saveState__(self):
        """Prior to loading, the state of the level is saved so that
        in the case of an error we can restore the level"""
        
        pass
    def __restoreState__(self):
        """If loading a level fails, this will restore the level to the previous
        state."""
        pass
    def __discardState__(self):
        """If loading a level is sucessfull this will clean up the state"""
        pass
    def loadLevel(self,path):
        f = file("Data\%s"%path,"rb")
        data = f.read()
        try:
            data = decompress(data)
        except:pass
        levelData,layerData = eval(data,{"__builtins__":None},{})
        
        self.columns = 100#levelData[0]
        self.rows = 100#levelData[1]
        self.cellSize = 32
        
        self.width = self.columns*self.cellSize
        self.height = self.rows * self.cellSize
        self.image = pygame.Surface((self.width,self.height))
        self.layers = map(lambda x:Layer(x,self.sheet),layerData)
        
        self.generateImage()
    
    def generateImage(self):
        for l in self.layers:
            if l["Visibility"]:
                print "rendering",l.name
                l.render(self.image,self.collision)
        self.layers[0].name,self.layers[0].cellData[1]
        
    def load(self,path):
        self.__saveState__()
        try:
            if not self.loadLevel(path):
                self.__restoreState__()
            else:
                self.__discardState__()
                return True
        except:
            self.__restoreState__()
        return False
                
        