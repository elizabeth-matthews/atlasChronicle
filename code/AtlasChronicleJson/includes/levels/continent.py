import pygame, sys, os
from pygame.locals import *

from field import Field

from ..modules.space import SpaceManager
from ..modules.mapper import Mapper
from ..modules.climates import ClimateMap

from ..helpers.defines import *

class Continent(object):
   def __init__(self, info):
      self.widthSizes = (info["dimensions"]["width"]["min"],
                         info["dimensions"]["width"]["max"])
      self.heightSizes = (info["dimensions"]["height"]["min"],
                          info["dimensions"]["height"]["max"])
      self.rigid = info["dimensions"]["rigid"]
      self.aspect = info["dimensions"]["aspect"]
      self.x = -1
      self.y = -1
      self.drawClimate = False
      self.active = None
      self.activeIndex = 0
      
      self.mapper = None
      self.space = None
      
      self.done = False
      self.sizeUpdated = False
      
      self.climateMap = None
      self.tbm = None
      self.combined = False
      self.climated = False
      
      self.fields = {}
      
      for f in info["nodes"].keys():
         self.fields[f] = Field(info["nodes"][f])
   
      if "restrictions" in info.keys():
         self.restrictions = info["restrictions"]
      else:
         self.restrictions = {}
         
      self.randomizeSize()
      self.setupField()
   
   def save(self):
      if self.active:
         return self.active.save()
   
   def getCanvas(self):
      if self.drawClimate and self.climateMap:
         self.climateMap.drawSelf()
         self.climateMap.drawType = 2
         self.climateMap.scale = 4
         return self.climateMap.canvas
      else:
         return self.active.getCanvas()
   
   
   def setTerrainBoundaryMap(self, tbm):
      self.tbm = tbm
   
   def handleEvent(self, e, offset=None):
      if self.active:
         self.active.handleEvent(e, offset)
         redraw = self.climateMap.handleEvent(e)
         if redraw:
            self.redoTerrains()
            self.mapper.drawAll()
         
         if (e.type == KEYDOWN):
            if e.key == K_SPACE:
               if self.active.isDone():
                  self.nextActive()
            elif e.key == K_b:
               if self.climateMap:
                  self.climateMap.tbm = self.tbm
               self.drawClimate = not self.drawClimate
         
         
         
   
   def isDone(self):
      done = True
      for f in self.fields:
         done = done and self.fields[f].isDone()
      
      done = done and self.mapper.done and self.space.done and not self.active
   
      return done
 
   def update(self):      
      if self.active:
         self.active.update()

   def nextActive(self):
      if self.active:
         if self.activeIndex < len(self.fields)-1:
            self.activeIndex += 1
            self.setupField()
         
         else:
            self.activeIndex = len(self.fields)
            if self.climated:
               self.active = None
            elif self.combined:
               self.setClimates()
               
            elif self.active == self.mapper:
               self.combineMapField()
               
            elif self.active == self.space:
               self.active = self.mapper
               self.sizeUpdated = True
               self.setupMap()
               
            else:
               self.active = self.space
               self.sizeUpdated = True
               self.setupSpace()
   
   def previousActive(self):
      if self.active == self.mapper:
         self.active = self.space
         self.canvas = self.active.canvas
         self.sizeUpdated = True
         self.mapper.initMap()
      elif self.active == self.space:
         # go back to fields.
         # clean space up
         #################################
         self.activeIndex -= 1
         self.setupField()
      
   def draw(self):
      if self.active:
         self.active.draw()
      
   def setupField(self):
      key = self.fields.keys()[self.activeIndex]
      self.active = self.fields[key]
      self.sizeUpdated = True
   
   def setupSpace(self):
      for f in self.fields:
         size = self.fields[f].mapper.getMinDim()
         x = size[0] 
         y = size[1] 
         self.space.addObject(f, f, x, y)
   
      for r in self.restrictions:
         self.space.addSSpring(r, self.restrictions[r]) 
      
   def setupMap(self):
      halfway = True
      self.mapper.initMap()
      self.mapper.fillRatio = 0.3
      
      if not halfway:
         for f in self.fields:
            pos = self.space.findObject(f)
            p = (int(pos[0]), int(pos[1]))
            self.mapper.addSeedTile('mountain', f, f, p)
      
      for r in self.restrictions:
         rInfo = self.restrictions[r]
         firstP = self.space.findObject(rInfo["first"])
         secondP = self.space.findObject(rInfo["second"])
         self.mapper.addRestriction(firstP, secondP, rInfo["typed"])
         if halfway and rInfo["typed"]:
            p = (int((firstP[0] + secondP[0]) / 2),
                 int((firstP[1] + secondP[1]) / 2))
            self.mapper.addSeedTile('mountain', rInfo["first"] + "+" + rInfo["second"],
                                    rInfo["first"] + "+" + rInfo["second"], p)
  
      self.mapper.setup()
   
   def combineMapField(self):
      for f in self.fields:
         pos = self.space.findObject(f)
         fInfo = self.fields[f]
         topLeft = (int(pos[0] - (fInfo.x / 2)), int(pos[1] - (fInfo.y / 2)))
         fOffset = fInfo.mapper.getMinOffset()
         fSize = fInfo.mapper.getMinDim()
         for ix in range(fSize[0]):
            for iy in range(fSize[1]):
               tileInfo = fInfo.mapper.map[ix + fOffset[0]][iy + fOffset[1]]
               if tileInfo.type != "void":
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].type = \
                                  tileInfo.type
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].key = \
                                  tileInfo.key
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].name = \
                                  tileInfo.name
                  self.mapper.updated.append((ix + topLeft[0], iy + topLeft[1]))
                  self.mapper.setMaxFilled((ix + topLeft[0], iy + topLeft[1]))
      
      self.combined = True
   
   def redoTerrains(self):
      #setting terrains
      for x in range(self.mapper.x):
         for y in range(self.mapper.y):
            if self.mapper.map[x][y].type not in ['mountain','water','void','loi','node']:
               climate = self.climateMap.getVals(x,y)
               terrain = self.tbm.getName(climate[0], climate[1])
               self.mapper.map[x][y].type = terrain
               self.mapper.updated.append((x, y))
      
      
      self.climated = True
   
   def setClimates(self):
      for f in self.fields:
         fInfo = self.fields[f]
         fPos = self.space.findObject(f)
         fOffset = fInfo.mapper.getMinOffset()
         topLeft = (int(fPos[0] - (fInfo.x / 2)), int(fPos[1] - (fInfo.y / 2)))
         for loi in fInfo.loi:
            loiInfo = fInfo.loi[loi]
            if "climate" in loiInfo.keys():
               climate = loiInfo["climate"]
               if climate["temperature"] != -1 and climate["humidity"] != -1:
                  lPos = fInfo.space.findObject(loi)
                  location = (lPos[0] + topLeft[0] + fOffset[0] + self.mapper.padding,
                              lPos[1] + topLeft[1] + fOffset[1] + self.mapper.padding)
                  self.climateMap.addPoint(location[0], location[1],
                                           (climate["temperature"],
                                            climate["humidity"]))

      self.climateMap.addEdges()
      self.climateMap.fill()
      
      #setting terrains
      for x in range(self.mapper.x):
         for y in range(self.mapper.y):
            if self.mapper.map[x][y].type == 'landfill':
               climate = self.climateMap.getVals(x,y)
               terrain = self.tbm.getName(climate[0], climate[1])
               self.mapper.map[x][y].type = terrain
               self.mapper.updated.append((x, y))
      
      
      self.climated = True
   
   def randomizeSize(self):
      self.x = random.randint(self.widthSizes[0], self.widthSizes[1])
      self.y = random.randint(self.heightSizes[0], self.heightSizes[1])
   
      self.mapper = Mapper()
      self.mapper.tileSize = SCALEC
      self.mapper.setSize(self.x, self.y)
      self.mapper.setRestrictedTypes(["water", "void", "landfill"])
      
      self.space = SpaceManager()
      self.space.spaceScale = SCALEC
      self.space.friction = FRICTIONC
      self.space.minVelocity = MINVELC
      self.space.setSize(self.x, self.y)
      
      self.climateMap = ClimateMap(self.mapper.x, self.mapper.y)
      
         
   def setUpdatedSize(self):
      if self.active:
         self.active.sizeUpdated = False
      self.sizeUpdated = False
      
   def getUpdatedSize(self):
      ret = self.sizeUpdated
      if self.active:
         ret = ret or self.active.sizeUpdated
      return ret
   