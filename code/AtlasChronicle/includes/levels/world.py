from ..modules.climates import TerrainBoundaryMap
from ..modules.space import SpaceManager
from ..modules.mapper import Mapper

from ..helpers.defines import COLORS, SCALEW, FRICTIONW, MINVELW

from continent import Continent

import random
import pygame
from pygame.locals import *

class World(object):
   def __init__(self, info):
      self.key = "world_key"
      self.widthSizes = (info.stats.dimensions.widthMin, info.stats.dimensions.widthMax)
      self.heightSizes = (info.stats.dimensions.heightMin, info.stats.dimensions.heightMax)
      self.rigid = info.stats.dimensions.rigid
      self.aspect = info.stats.dimensions.aspect
      self.x = -1
      self.y = -1
      
      self.active = None
      self.activeIndex = -1
      
      self.mapper = None
      self.space = None
      
      self.sizeUpdated = True
      
      self.tbm = TerrainBoundaryMap()
      for t in info.stats.terrains:
         tInfo = info.stats.terrains[t]
         COLORS[t] = (tInfo.color.r * 255,
                      tInfo.color.g * 255,
                      tInfo.color.b * 255)
         
         self.tbm.add(t,
                      tInfo.climate.temperature,
                      tInfo.climate.humidity,
                      COLORS[t])
         
      
      self.tbm.fill()
      
      self.randomizeSize()
      
      self.continents = {}
      self.restrictions = {}
      
      for c in info.nodes:
         self.continents[c] = Continent(info.nodes[c])
         self.continents[c].setTerrainBoundaryMap(self.tbm)
      
      for r in info.restrictions:
         self.restrictions[r] = info.restrictions[r]
   
      self.activeIndex = 0
      self.setupContinent()
   
   def save(self):
      if self.active:
         return self.active.save()
   
   def getCanvas(self):
      return self.active.getCanvas()
   
   
   def draw(self):
      if self.active:
         self.active.draw()
   
   def update(self):
      if self.active:
         self.active.update()
         
         self.sizeUpdated = self.sizeUpdated or self.active.getUpdatedSize()
   
   def handleEvent(self, e, offset=None):               
      if self.active:
         self.active.handleEvent(e, offset)
         
         if (e.type == KEYDOWN):
            if e.key == K_SPACE:
               if self.active.isDone():
                  self.nextActive()
                  print "NEXTACTIVE"
      
   def nextActive(self):
      if self.active:
         if self.activeIndex < len(self.continents)-1:
            self.activeIndex += 1
            self.setupContinent()
         elif self.active == self.mapper:
            self.active = None
         elif self.active == self.space:
            self.active = self.mapper
            self.sizeUpdated = True
            self.setupMap()
         else:
            self.active = self.space
            self.sizeUpdated = True
            self.setupSpace()
   
   def setupSpace(self):
      for c in self.continents:
         size = self.continents[c].mapper.getMinDim()
         x = size[0] #self.continents[c].mapper.x
         y = size[1] #self.continents[c].mapper.y
         self.space.addObject(c, c, x, y)
   
      for r in self.restrictions:
         rInfo = self.restrictions[r]
         self.space.addSSpring(r, rInfo.first, rInfo.second,
                               (rInfo.min, rInfo.max), rInfo.typed)
      
   
   def setupContinent(self):
      key = self.continents.keys()[self.activeIndex]
      self.active = self.continents[key]
      self.sizeUpdated = True
      
   def setupMap(self):
      for c in self.continents:
         pos = self.space.findObject(c)
         p = (int(pos[0]), int(pos[1]))
         cInfo = self.continents[c]
         cOffset = cInfo.mapper.getMinOffset()
         cSize = cInfo.mapper.getMinDim()
         topLeft = (int(pos[0] - (cInfo.x / 2)), int(pos[1] - (cInfo.y / 2)))
         for ix in range(cSize[0]):
            for iy in range(cSize[1]):
               tileInfo = cInfo.mapper.map[ix + cOffset[0]][iy + cOffset[1]]
               if tileInfo.type != "void":
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].type = \
                                  tileInfo.type
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].key = \
                                  tileInfo.key
                  self.mapper.map[ix + topLeft[0]][iy + topLeft[1]].name = \
                                  tileInfo.name
                  
                  self.mapper.setMaxFilled((ix + topLeft[0], iy + topLeft[1]))
      self.mapper.drawAll()

   
   def randomizeSize(self):
      self.x = random.randint(self.widthSizes[0], self.widthSizes[1])
      self.y = random.randint(self.heightSizes[0], self.heightSizes[1])
   
      self.mapper = Mapper(self.key)
      self.mapper.setDefaultType("water")
      self.mapper.tileSize = SCALEW
      self.mapper.setSize(self.x, self.y)
      
      self.space = SpaceManager(self.key)
      self.space.spaceScale = SCALEW
      self.space.friction = FRICTIONW
      self.space.minVelocity = MINVELW
      self.space.setSize(self.x, self.y)
      
   def setUpdatedSize(self):
      if self.active:
         self.active.setUpdatedSize()
      self.sizeUpdated = False
      
   def getUpdatedSize(self):
      ret = self.sizeUpdated
      if self.active and self.active != self.space and self.active != self.mapper:
         ret = ret or self.active.getUpdatedSize()
      return ret
