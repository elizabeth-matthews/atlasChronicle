#import pygame, sys, os
from pygame.locals import *

from helpers.xmlParser import XmlParser
from helpers.panner import Panner
from helpers.defines import *

from modules.mapper import Mapper
from modules.space import SpaceManager
from modules.climates import TerrainBoundaryMap

from levels.field import Field
from levels.continent import Continent
from levels.world import World

from copy import deepcopy
import pygame.display
import json


class AtlasChronicle(object):
   
   def __del__(self):
      pygame.display.quit()
   
   def __init__(self, saveStart=0):
      self.RUN = True
      self.DEBUG = False
      
      pygame.init()
      pygame.display.init()
      random.seed()#1337)
      
      self.parser = XmlParser()
      self.panner = Panner()
      
      self.mapper = None
      
      self.imageSaveIndex = saveStart
      self.mapSaveIndex = saveStart
      
      self.next = False
   
   def run(self, fileName="../data/worldDataFF6.xml", windowSize=(724,576)):
      
      self.readInput(fileName)
      self.initPython(windowSize)
      self.initWorld()
      
      while self.RUN:
         
         for event in pygame.event.get():
            self.handleEvent(event)
            
         self.update()
         self.draw()
         
         self.screen.blit(self.canvas, (0,0))          
         pygame.display.flip()
         
   
   def draw(self):
      self.canvas.fill(COLORS["gray"])
      if self.active:
         offset = self.panner.getOffset()
         
         self.active.draw()
         
         self.canvas.blit(self.active.getCanvas(), offset)
      
         
   
   def update(self):
      if self.active:
         self.active.update()
         if self.active.getUpdatedSize():
            size = self.active.getCanvas().get_size()
            self.panner.updateMax(size[0], size[1])
            self.active.setUpdatedSize()
      else:
         x = 0


   def readInput(self, file):
      self.parser.read(file)
      
         
   def initPython(self, windowSize):
      self.windowSize = windowSize
      self.panner.updateScreen(windowSize[0], windowSize[1])
      
      self.window = pygame.display.set_mode(self.windowSize)
      pygame.display.set_caption("Atlas Chronicle")
      self.screen = pygame.display.get_surface()
      
      self.canvas = pygame.Surface(windowSize)
   
   def initWorld(self):
      info = self.parser.world
      self.active = World(info)
      
      
      size = self.active.getCanvas().get_size()
      self.panner.updateMax(size[0], size[1])
         
   def saveActiveImage(self):
      pygame.image.save(self.active.getCanvas(), "../images/active" + "{0:03d}".format(self.imageSaveIndex) + ".png")
      self.imageSaveIndex += 1
      
   
   def saveActiveMap(self):
      output = open("../maps/map" + "{0:03d}".format(self.mapSaveIndex) + ".json", "w")
      mapInfo = self.active.save()
      json.dump(mapInfo,output) #output.write(s)
      output.close()
      self.mapSaveIndex += 1
      
   def handleEvent(self, e):
      
      if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
      # Exit
         self.RUN = False
         
      elif e.type == KEYDOWN:
         if e.key == K_s:
            if self.active:
               self.saveActiveImage()
         if e.key == K_a:
            if self.active:
               self.saveActiveMap()
               print "Map saved"
      
      if self.active:
         self.panner.handleEvent(e)
         off = self.panner.getOffset()
         self.active.handleEvent(e, off)
   