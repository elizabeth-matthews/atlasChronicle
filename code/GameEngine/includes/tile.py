from frameManager import FRAMES

class TileInfo(object):
   def __init__(self, key="None",):
      self.key = key
      self.__visited = False
      self.__teleporter = False
      self.__teleLocation = [0,0]

class Tile(object):
   def __init__(self, ix, t, key="None"):
      self.info = TileInfo(key)
      self.type = t
      self.__frameKey = "tiles/FinalFantasy6/ff6MapMinimal.png"
      if self.type == "mountain":
         self.__frameIndex = [0 + (ix[0] % 2),
                              15 + (ix[1] % 2)]
      elif self.type == "water":
         self.__frameIndex = [1,0]
      else:
         if self.type.startswith("grass"):
            self.__frameIndex = [0,0]
         elif self.type.startswith("desert"):
            self.__frameIndex = [0, 3]
         elif self.type.startswith("forest"):
            self.__frameIndex = [0, 6]
         elif self.type.startswith("snow"):
            self.__frameIndex = [0, 9]
         elif self.type.startswith("plains"):
            self.__frameIndex = [0, 12]
         else:
            self.__frameIndex = [0,0]
         
         if self.type.endswith("A"):
            self.__frameIndex[1] += 1
         elif self.type.endswith("B"):
            self.__frameIndex[0] += 1
            self.__frameIndex[1] += 1
         elif self.type.endswith("C"):
            self.__frameIndex[1] += 2
         elif self.type.endswith("D"):
            self.__frameIndex[0] += 1
            self.__frameIndex[1] += 2
            
   
   def draw(self, canvas, offset=(0,0)):
      canvas.blit(FRAMES.getFrame(self.__frameKey, self.__frameIndex[0],  self.__frameIndex[1]),
                  offset)
      
