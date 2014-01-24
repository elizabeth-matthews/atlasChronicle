import json
from pygame import Surface

from helpers import TILE_SIZE, locations, locTiles, DOWN, LEFT, RIGHT, UP
from functions import longitude, latitude, cardinal
from frameManager import FRAMES
from textBox import BOXES
from tile import Tile




class World(object):
   def __init__(self, info=None, size=(100,100)):
      
      FRAMES.loadFrames("tiles/FinalFantasy6/ff6MapMinimal.png")
      
      if info == None:
         self.size = size
         
         self.tiles = [[Tile((x,y), "grass") for y in range(size[1])] for x in range(size[0])]
         self.__canvas = Surface((TILE_SIZE * size[0], TILE_SIZE * size[1]))
         
         self.__setTile(0,0, "water")
         self.__setTile(0,2, "water")
         self.__setTile(2,0, "water")
         self.__setTile(2,2, "water")
         
         locations["StarterTown"]   = [3,0]
         locations["DesertTown"]    = [5,0]
         locations["DesertPalace"]  = [7,0]
         locations["MountainTown"]  = [9,0]
         locations["PlainsVillage"] = [11,0]
         locations["MountainCave"]  = [3,2]
         locations["SnowyVillage"]  = [5,2]
         locations["ForestVillage"] = [7,2]
         locations["ThiefHideout"]  = [9,2]
         locations["PortTown"]      = [11,2]
         
         locations["FishingTown"]   = [3,4]
         locations["LakeTemple"]    = [5,4]
         
         locations["FinalPalace"]   = [11,4]
         locations["MasterSword"]   = [13,4]
         
         self.__setTile(locations["StarterTown"][0], locations["StarterTown"][1], "grassA", "StarterTown")
         self.__setTile(locations["DesertTown"][0], locations["DesertTown"][1], "desertB", "DesertTown")
         self.__setTile(locations["DesertPalace"][0], locations["DesertPalace"][1], "desertC", "DesertPalace")
         self.__setTile(locations["MountainTown"][0], locations["MountainTown"][1], "grassB", "MountainTown")
         self.__setTile(locations["PlainsVillage"][0], locations["PlainsVillage"][1], "plainsD", "PlainsVillage")
         
         self.__setTile(locations["MountainCave"][0], locations["MountainCave"][1], "grassA", "MountainCave")
         self.__setTile(locations["SnowyVillage"][0], locations["SnowyVillage"][1], "snowB", "SnowyVillage")
         self.__setTile(locations["ForestVillage"][0], locations["ForestVillage"][1], "forestA", "ForestVillage")
         self.__setTile(locations["ThiefHideout"][0], locations["ThiefHideout"][1], "forestD", "ThiefHideout")
         self.__setTile(locations["PortTown"][0], locations["PortTown"][1], "grassB", "PortTown")
         
         self.__setTile(locations["FishingTown"][0], locations["FishingTown"][1], "grassA", "FishingTown")
         self.__setTile(locations["LakeTemple"][0], locations["LakeTemple"][1], "grassC", "LakeTemple")
         
         self.__setTile(locations["FinalPalace"][0], locations["FinalPalace"][1], "forestC", "FinalPalace")
         self.__setTile(locations["MasterSword"][0], locations["MasterSword"][1], "forest", "MasterSword")
       
         for i in range(5,10):
            for j in range(5,10):
               self.__setTile(i, j, "desert")
         for i in range(3,8):
            for j in range(90,98):
               self.__setTile(i, j, "plains")
         for i in range(12,22):
            for j in range(5,12):
               self.__setTile(i, j)
         for i in range(7,15):
            for j in range(20,29):
               self.__setTile(i, j, "mountain")
         for i in range(86,98):
            for j in range(77,99):
               self.__setTile(i, j, "forest")
         for i in range(86,98):
            for j in range(0,10):
               self.__setTile(i, j, "snow")
         
         
         
      
      else:
         
         fp = open(info, 'r')
         
         jInfo = json.load(fp)
         
         fp.close()
         
         self.size = jInfo["size"]

         self.__canvas = Surface((TILE_SIZE * self.size[0], TILE_SIZE * self.size[1]))
         
         self.tiles = []
         for x in range(self.size[0]):
            jRow = jInfo["tiles"][x]
            self.tiles.append([])
            for y in range(self.size[1]):
               tType = jRow[y]
               if tType not in locations.keys():
                  self.tiles[x].append(Tile((x,y), tType))
               else:
                  self.tiles[x].append(Tile((x,y),locTiles[tType],tType))
                  locations[tType] = [x,y]
                  
         
      BOXES.formatBox("StarterTown",1,cardinal(locations["StarterTown"], locations["DesertTown"]))
      BOXES.formatBox("DesertTown",1,cardinal(locations["DesertTown"], locations["DesertPalace"]))
      BOXES.formatBox("DesertTown",2,cardinal(locations["DesertTown"], locations["MountainTown"]))
      BOXES.formatBox("DesertTown",3,cardinal(locations["DesertTown"], locations["MountainTown"]))
      BOXES.formatBox("MountainTown",1,cardinal(locations["MountainTown"], locations["PlainsVillage"]))
      BOXES.formatBox("SnowyVillage",1,cardinal(locations["SnowyVillage"], locations["ForestVillage"]))
      BOXES.formatBox("FishingTown",1,cardinal(locations["FishingTown"], locations["LakeTemple"]))
      ns, nsSteps = latitude(locations["ThiefHideout"],locations["MasterSword"])
      ew, ewSteps = longitude(locations["ThiefHideout"],locations["MasterSword"])
      BOXES.formatBox("ThiefHideout", 3, nsSteps, ns, ewSteps, ew)
         
      self.__initDraw()
   
   def __setTile(self, x, y, t="water", n="None"):
      self.tiles[x][y] = Tile((x,y), t, n)
      
      
   
   def __initDraw(self):
      for x in range(len(self.tiles)):
         for y in range(len(self.tiles[x])):
            self.tiles[x][y].draw(self.__canvas, (x * TILE_SIZE, y * TILE_SIZE))
            
   def draw(self, canvas, offset=(0,0), windowSize=(640,480)):
      canvas.blit(self.__canvas, offset)
      
      if offset[0] > 0:
         canvas.blit(self.__canvas, (offset[0] - (self.size[0] * TILE_SIZE), offset[1]))
      if offset[1] > 0:
         canvas.blit(self.__canvas, (offset[0], offset[1] - (self.size[1] * TILE_SIZE)))
      if offset[0] > 0 and offset[1] > 0:
         canvas.blit(self.__canvas, (offset[0] - (self.size[0] * TILE_SIZE),
                                     offset[1] - (self.size[1] * TILE_SIZE)))
         
      if offset[0] + (self.size[0] * TILE_SIZE) < windowSize[0]:
         canvas.blit(self.__canvas, ((self.size[0] * TILE_SIZE) + offset[0], offset[1]))
      if offset[1] + (self.size[1] * TILE_SIZE) < windowSize[1]:
         canvas.blit(self.__canvas, (offset[0], (self.size[1] * TILE_SIZE) + offset[1]))
      if offset[0] + (self.size[0] * TILE_SIZE) < windowSize[0] and \
         offset[1] + (self.size[1] * TILE_SIZE) < windowSize[1]:
         canvas.blit(self.__canvas, ((self.size[0] * TILE_SIZE) + offset[0],
                                         (self.size[1] * TILE_SIZE) + offset[1]))
         
         
      if offset[0] > 0 and offset[1] + (self.size[1] * TILE_SIZE) < windowSize[1]:
         canvas.blit(self.__canvas, (offset[0] - (self.size[0] * TILE_SIZE),
                                     (self.size[1] * TILE_SIZE) + offset[1]))
      if offset[0] + (self.size[0] * TILE_SIZE) < windowSize[0] and offset[1] > 0:
         canvas.blit(self.__canvas, ((self.size[0] * TILE_SIZE) + offset[0],
                                          offset[1] - (self.size[1] * TILE_SIZE)))
         
         
   
   def collision(self, d, direction, hasShip):
      # determines if there's a colliable item at location
      checkTypes = ["mountain"]
      if not hasShip:
         checkTypes.append("water")
         
      addX = 0
      addY = 0
      if direction == DOWN:
         addY = 1
      if direction == RIGHT:
         addX = 1
         
      locX = (int(d[0]) + addX) % self.size[0]
      locY = (int(d[1]) + addY) % self.size[1]
      
      
      return self.getType(locX, locY) in checkTypes

   def getType(self, locX, locY):
      # determines if there's a colliable item at location
         
      return self.tiles[int(locX)][int(locY)].type
