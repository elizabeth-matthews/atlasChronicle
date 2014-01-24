from pygame import Surface, display, init, time, event
from pygame.locals import *

# Required here for textbox.
init()
display.init()

from textBox import BOXES
from world import World
from player import Player
from helpers import locations, TILE_SIZE, STILL
from miniMap import MiniMap

class GameEngine(object):
   def __del__(self):
      display.quit()
      
   def __init__(self, fInfo="../maps/surveyMap.json", size=(800,600)):

      #Pygame stuff      
      self.__initPython(size)
      self.__clock = time.Clock()
      
      self.__RUN = True
      self.__world = World(fInfo)
      self.__player = Player([locations["StarterTown"][0], locations["StarterTown"][1]-1])
      
      if fInfo:
         self.__miniMap = MiniMap(fInfo)
      else:
         self.__miniMap = None
      self.__worldOffset = [0,0]
      self.__dimensions = size
      self.__showMiniMap = True
      
      self.__textBox = None
      self.__currTileId = None
     
   def __initPython(self, windowSize):
      self.__windowSize = windowSize
      
      self.__window = display.set_mode(self.__windowSize)
      display.set_caption("Atlas Chronicle Game Engine")
      self.__screen = display.get_surface()
      
      self.__canvas = Surface(self.__windowSize)
     
   def run(self):

      self.__RUN = True
      intro = True
        
      while self.__RUN:
         
         timeSpent = self.__clock.tick(30)
         
         for e in event.get():
            self.__handleEvent(e)
            
         self.__update(timeSpent)
         self.__draw()
         
         if intro:
            self.__textBox = BOXES.getBox("Help")
            intro = False
            
         self.__screen.blit(self.__canvas, (0,0))          
         display.flip()
         
         self.__RUN = self.__RUN and not self.__player.inventory.private["gameFinished"]

   def __handleEvent(self, e):
      
      if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
      # Exit
         self.__RUN = False

      else:
      
         if self.__textBox:
            done = self.__textBox.handleEvent(e)
            if done:
               self.__textBox = None
               
               # teleport here for mountain pass
               if self.__currTileId == "MountainTown" and self.__player.inventory.tKey:
                  self.__player.location = locations["MountainCave"]
               elif self.__currTileId == "MountainCave":
                  self.__player.location = locations["MountainTown"]
               elif self.__currTileId == "FinalPalace":
                  if self.__player.inventory.cCourage and \
                     self.__player.inventory.cWisdom and \
                     self.__player.inventory.cPower:
                     if self.__player.inventory.private["finalVisit"]:
                        self.__player.inventory.private["gameFinished"] = True
                     else:
                        self.__player.inventory.private["finalVisit"] = True
               
               self.__currTileId = None
         else:
            if e.type == KEYDOWN and \
                       self.__textBox == None and \
                       self.__player.state == STILL and \
                       e.key in [K_SPACE, K_i, K_h, K_m, K_1, K_2, K_3, K_4]:
               
               if e.key == K_SPACE:
                  self.__currTileId = \
                        self.__world.tiles[int(self.__player.location[0])][int(self.__player.location[1])].info.key
                  self.__textBox = BOXES.getBox(self.__currTileId, self.__player.inventory)
               elif e.key == K_i:
                  BOXES.updateBox("Inventory", 0, str(self.__player.inventory))
                  self.__textBox = BOXES.getBox("Inventory")
               elif e.key == K_m:
                  self.__showMiniMap = not self.__showMiniMap
               elif e.key == K_h:
                  self.__textBox = BOXES.getBox("Help")
               else:
                  # cheat
                  if e.key == K_1:
                     self.__player.inventory.ship = True
                     self.__player.inventory.tKey = True
                  elif e.key == K_2:
                     self.__player.inventory.cCourage = True
                     self.__player.inventory.cWisdom = True
                     self.__player.inventory.cPower = True
                  elif e.key == K_3:   
                     self.__player.inventory.mSword = True
                  else:
                     self.__player.location = locations["FinalPalace"]
                  
            else:
               self.__player.handleEvent(e)

   def __update(self, ticks):
      if self.__miniMap != None:
         self.__miniMap.update(ticks)
      
      if not self.__textBox:
         self.__player.update(ticks, self.__world)
         self.__worldOffset = [(-self.__player.location[0] * TILE_SIZE) + (self.__windowSize[0] / 2) - (TILE_SIZE / 2),
                               (-self.__player.location[1] * TILE_SIZE) + (self.__windowSize[1] / 2) - (TILE_SIZE / 2)]
     
   def __draw(self):
      self.__world.draw(self.__canvas, self.__worldOffset, self.__windowSize)
      self.__player.draw(self.__canvas, self.__windowSize)
      if self.__showMiniMap and self.__miniMap != None:
         self.__miniMap.draw(self.__canvas, self.__player.location, self.__windowSize)
      
      if self.__textBox:
         self.__textBox.draw(self.__canvas, self.__windowSize)
         
      display.flip()
      display.update()
