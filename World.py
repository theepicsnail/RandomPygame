import pygame
class Cell(pygame.Sprite):
    Clipping = False
class Layer:
    cells=[]
    properties = {}
    
class Level(pygame.Sprite):
    path = None
    staticLayer = None
    layers = []
    
    def __init__(self):
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
        
        pass
    
    
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
                
        