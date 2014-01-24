from ..modules.mapper import Mapper
from ..modules.space import SpaceManager

from ..helpers.defines import *

#import pygame, sys, os
#from pygame.locals import *

class Field(object):
   def __init__(self, info):
      self.key = info.key
      self.widthSizes = (info.stats.dimensions.widthMin, info.stats.dimensions.widthMax)
      self.heightSizes = (info.stats.dimensions.heightMin, info.stats.dimensions.heightMax)
      self.rigid = info.stats.dimensions.rigid
      self.aspect = info.stats.dimensions.aspect
      self.x = -1
      self.y = -1
      
      self.active = None
      
      self.mapper = None
      self.space = None
      
      self.sizeUpdated = False
      
      self.loi = {}
      self.restrictions = {}
      
      for l in info.nodes:
         self.loi[l] = info.nodes[l]
      
      for r in info.restrictions:
         self.restrictions[r] = info.restrictions[r]
      
      self.randomizeSize()
      
      self.setupSpace()
   
   def save(self):
      if self.active:
         return self.active.save()
   
   def getCanvas(self):
      return self.active.getCanvas()
   
   def getUpdatedSize(self):
      return self.sizeUpdated
   
   def setUpdatedSize(self):
      self.sizeUpdated = False

   def setupSpace(self):
      for l in self.loi:
         self.space.addObject(l, self.loi[l].name)
   
      for r in self.restrictions:
         rInfo = self.restrictions[r]
         self.space.addSSpring(r, rInfo.first, rInfo.second,
                               (rInfo.min, rInfo.max), rInfo.typed)
   
   def setupMap(self):
      for l in self.loi:
         loiInfo = self.loi[l]
         loc = self.space.findObject(l)         
         x, y = int(loc[0]), int(loc[1])
         
         if loiInfo.terrain:            
            self.mapper.addSeedTile(loiInfo.terrain, l, loiInfo.name, (x, y))
         
         else:
            self.mapper.addSeedTile("loi", l, loiInfo.name, (x, y),
                                    loiInfo.physicalSeeds)
            
      for r in self.restrictions:
         rInfo = self.restrictions[r]
         locFirst = self.space.findObject(rInfo.first)
         locFirst[0] = int(locFirst[0])
         locFirst[1] = int(locFirst[1])
         locSecond = self.space.findObject(rInfo.second)
         locSecond[0] = int(locSecond[0])
         locSecond[1] = int(locSecond[1])
         self.mapper.addRestriction(locFirst, locSecond, rInfo.typed)
      
      self.mapper.setup()

   def randomizeSize(self):
      self.x = random.randint(self.widthSizes[0], self.widthSizes[1])
      self.y = random.randint(self.heightSizes[0], self.heightSizes[1])
   
      self.mapper = Mapper(self.key)
      self.mapper.tileSize = SCALEF
      self.mapper.setSize(self.x, self.y)
      
      self.space = SpaceManager(self.key)
      self.space.spaceScale = SCALEF
      self.space.friction = FRICTIONF
      self.space.minVelocity = MINVELF
      self.space.setSize(self.x, self.y)
      
      self.active = self.space
   
   def isDone(self):
      return (self.mapper.done and self.space.done and not self.active)
   
   def update(self):
      
      if self.active:
         self.active.update()
   
   def draw(self):
      if self.active:
         self.active.draw()
   
   def nextActive(self):
      if self.active == self.space:
         self.active = self.mapper
         self.canvas = self.active.canvas
         self.sizeUpdated = True
         self.setupMap()
      else:
         self.active = None

   def handleEvent(self, e, offset=None):
      if e.type == KEYDOWN:
         if e.key == K_SPACE:
            if self.active and self.active.done:
               self.nextActive()
         elif e.key == K_BACKSPACE:
            self.previousActive()
      if self.active:
         self.active.handleEvent(e, offset)

   def previousActive(self):
      # go back in active states
      if self.active == self.mapper:
         self.active = self.space
         self.canvas = self.active.canvas
         self.sizeUpdated = True
         self.mapper.initMap()