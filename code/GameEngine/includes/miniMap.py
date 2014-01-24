from pygame import Surface, draw, Rect
from helpers import locations

import json
import copy

class MiniMap(object):
   def __init__(self, mapInfo):
      fp = open(mapInfo)
      
      jData = json.load(fp)
      
      fp.close()
      
      self.drawSize = 3
      self.downScale = 2
      self.__blinkCount = 0
      self.__showPlayer = True
      self.__blinkSpeed = 0.003
      self.__alpha = 200
      
      self.__colors = {
         "poi" : (255, 255, 255), "grassland" : (38,200,80),
         "forest" : (0,60,5), "plains" : (150,150,90),
         "mountain" : (117,26,12), "water" : (0,30,100),
         "desert" : (255,255,102), "snow" : (190,190,255)
      }

      self.poiLocs = []

      self.size = [x / self.downScale for x in jData["size"]]

      
      self.__map = Surface([x * self.drawSize for x in self.size])
      self.canvas = Surface([x * self.drawSize for x in self.size])
      
      self.canvas.set_alpha(self.__alpha)
      for x in range(self.size[0]):
         jRows = []
         for i in range(self.downScale):
            jRows.append(jData["tiles"][x * self.downScale + i])
            
         for y in range(self.size[1]):
            # draw each pixel
            tTypes = []
            for jr in jRows:
               for j in range(self.downScale):
                  tTypes.append(jr[y * self.downScale + j])
                  
            color = [0,0,0]
            cCount = 0
            poiFound = False
            
            for t in tTypes:
               if t not in locations.keys():
                  cCount += 1
                  for rgb in range(3):
                     color[rgb] += self.__colors[t][rgb]
               elif not poiFound:
                  if t != "MasterSword":
                     self.poiLocs.append((x,y))
                     poiFound = True
            
            for rgb in range(3):
               color[rgb] /= cCount
               
            area = Rect((x * self.drawSize, y * self.drawSize),
                        (self.drawSize, self.drawSize))
            draw.rect(self.__map, color, area)
            
      
      

   def draw(self, canvas, playerLocation, windowSize=(640,480)):
      
      self.canvas.blit(self.__map, (0,0))
      
      
      if self.__showPlayer:
         
         for poi in self.poiLocs:
            
            area = Rect((poi[0] * self.drawSize, poi[1] * self.drawSize),
                        (self.drawSize, self.drawSize))
            draw.rect(self.canvas, (0,0,0), area)
            
         area = Rect((int(playerLocation[0] / self.downScale) * self.drawSize,
                      int(playerLocation[1] / self.downScale) * self.drawSize),
                     (self.drawSize, self.drawSize))
         draw.rect(self.canvas, (255,0,0), area)
            
      
      canvas.blit(self.canvas, (windowSize[0] - (self.size[0] * self.drawSize),
                                windowSize[1] - (self.size[1] * self.drawSize)))
      
   
   def update(self, ticks):
      self.__blinkCount += self.__blinkSpeed * ticks
      
      if self.__blinkCount > 1:
         self.__blinkCount -= 1
         self.__showPlayer = not self.__showPlayer
   
   
   