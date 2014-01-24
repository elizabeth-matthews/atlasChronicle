from pygame import image, Surface, transform, Rect

from helpers import TILE_SIZE, TRANSPARENT_COLOR, SCALE


class FrameManager(object):
   def __init__(self):
      self.__frames = {}
         
   def loadFrames(self, key, size=(TILE_SIZE, TILE_SIZE)):
      self.__frames[key] = []
         
      # load and scale image
      sheet = image.load(key)
      if SCALE != 1:
         sheet = transform.scale(sheet, [SCALE * x for x in sheet.get_size()])
      sheet = sheet.convert()
      
      # load all frames
      i = 0
      for x in range(0, sheet.get_size()[0], size[0]):
         self.__frames[key].append([])
         j = 0
         
         for y in range(0, sheet.get_size()[1], size[1]):
         
            self.__frames[key][i].append(Surface(size))
            frameArea = Rect((x, y), size)
            self.__frames[key][i][j].blit(sheet, (0,0), frameArea)
            self.__frames[key][i][j].set_colorkey(TRANSPARENT_COLOR)
            
            j += 1
            
         i += 1
   
   
   def getFrame(self, key, i1, i2):
      if key not in self.__frames.keys():
         self.loadFrames(key)
      
      return self.__frames[key][i1][i2]

   
FRAMES = FrameManager()