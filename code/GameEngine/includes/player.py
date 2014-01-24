from pygame.locals import *

from helpers import SCALE, TILE_SIZE, UP, DOWN, LEFT, RIGHT, STILL, MOVING
from inventory import Inventory
from frameManager import FRAMES
from functions import aligned


class Player(object):
   def __init__(self, startLoc = [0,0]):
      self.__walkKey = "sprites/terra.png"
      self.__shipKey = "sprites/ship.png"
      self.__walkFrame = 4
      self.__shipFrame = 2
      self.__walkSize = (16 * SCALE, 24 * SCALE)
      self.__shipSize = (TILE_SIZE, TILE_SIZE)
      
      self.__frameKey = self.__walkKey
      self.maxFrame = self.__walkFrame
      self.size = self.__walkSize
      
      self.__dir = 0
      self.inventory = Inventory()
      self.location = startLoc
      self.__moveIndex = 0
      self.__frame = 0
      self.__keyCount = 0
      
      self.__frameRate = 80.0
      self.__mSpeed = 1.0 / (self.__frameRate * 2)
      self.__moveSpeed = 0.005
      self.__stopping = False
      self.__frameCount = 0
      
      self.__face = DOWN
      self.state = STILL
      
      self.__isShip = False
      
      FRAMES.loadFrames(self.__walkKey, self.__walkSize)
      FRAMES.loadFrames(self.__shipKey, self.__shipSize)
      

   def handleEvent(self, e):
      if e.type == KEYDOWN:

         if e.key == K_DOWN:
            self.state = MOVING
            self.__stopping = False
            self.__keyCount += 1
            self.__dir += 1
         elif e.key == K_UP:
            self.state = MOVING
            self.__stopping = False
            self.__keyCount += 1
            self.__dir += 2
         elif e.key == K_RIGHT:
            self.state = MOVING
            self.__stopping = False
            self.__keyCount += 1
            self.__dir += 4
         elif e.key == K_LEFT:
            self.state = MOVING
            self.__stopping = False
            self.__keyCount += 1
            self.__dir += 8
            
      elif e.type == KEYUP:
         if e.key == K_DOWN:
            self.__keyCount -= 1
            self.__dir -= 1
         elif e.key == K_UP:
            self.__keyCount -= 1
            self.__dir -= 2
         elif e.key == K_RIGHT:
            self.__keyCount -= 1
            self.__dir -= 4
         elif e.key == K_LEFT:
            self.__keyCount -= 1
            self.__dir -= 8
         
         if self.__keyCount == 0:
            self.__stopping = True
            self.__dir = 0

   def update(self, ticks, world):
      if self.state == MOVING:
         moveDistance = self.__moveSpeed * ticks
         dest = [self.location[0], self.location[1]]
         
         # update facing
         if self.__dir != 0:
            if self.__dir % 2 == 1:
               intendedFace = DOWN
            elif self.__dir % 4 == 2:
               intendedFace = UP
            elif self.__dir % 8 == 4:
               intendedFace = RIGHT
            elif self.__dir % 16 == 8:
               intendedFace = LEFT
            else:
               intendedFace = self.__face
         else:
            intendedFace = self.__face
         
         
         if aligned(self.location):
            self.__face = intendedFace
            if self.__dir != 0:
               self.__stopping = False
         elif intendedFace != self.__face:
            self.__stopping = True
         
         if self.__face == DOWN:
            # down
            if self.__stopping:
               moveDistance = min([moveDistance, 1 - (self.location[1] % 1)])
            dest[1] += moveDistance
               
         if self.__face == UP:
            # up
            if self.__stopping:
               moveDistance = min([moveDistance, self.location[1] % 1])
            dest[1] -= moveDistance
            
         if self.__face == RIGHT:
            # right
            if self.__stopping:
               moveDistance = min([moveDistance, 1 - (self.location[0] % 1)])
            dest[0] += moveDistance

         if self.__face == LEFT:
            # left
            if self.__stopping:
               moveDistance = min([moveDistance, (self.location[0] % 1)])
            dest[0] -= moveDistance
                
         if (self.__dir == 0 and (moveDistance == 0 or aligned(self.location))):
            self.state = STILL
            self.__frame = 0
         elif not self.__stopping and world.collision(dest, self.__face, self.inventory.ship):
            self.state = STILL
            self.__frame = 0
         
         if self.state == MOVING:
            self.__frameCount += ticks
            if self.__frameCount > self.__frameRate:
               self.__frame = (self.__frame + 1) % self.maxFrame
               self.__frameCount = 0
               
            if self.__face == DOWN:
               self.location[1] += moveDistance 
               if self.location[1] >= world.size[1]:
                  self.location[1] -= world.size[1]
            elif self.__face == UP:
               self.location[1] -= moveDistance 
               if self.location[1] < 0:
                  self.location[1] += world.size[1]
            if self.__face == RIGHT:
               self.location[0] += moveDistance 
               if self.location[0] >= world.size[0]:
                  self.location[0] -= world.size[0]
            elif self.__face == LEFT:
               self.location[0] -= moveDistance 
               if self.location[0] < 0:
                  self.location[0] += world.size[0]  
      
      else:
         # still
         self.location[0] = int(round(self.location[0]))
         self.location[1] = int(round(self.location[1]))
         
   
      
      if self.inventory.ship and \
             world.getType(self.location[0],self.location[1]) == "water":
         if not self.__isShip:
            self.maxFrame = self.__shipFrame
            self.__frameKey = self.__shipKey
            self.__frame %= self.maxFrame
            self.size = self.__shipSize
            self.__isShip = True
      else:
         if self.__isShip:
            self.maxFrame = self.__walkFrame
            self.__frameKey = self.__walkKey
            self.__frame %= self.maxFrame
            self.size = self.__walkSize
            self.__isShip = False
         
   
   def draw(self, canvas, windowSize=(640,480)):
      canvas.blit(FRAMES.getFrame(self.__frameKey, self.__frame, self.__face),
                  [windowSize[0]/2 - (TILE_SIZE / 2), # - (self.size[0] / 2),
                   windowSize[1]/2 - (self.size[1] - TILE_SIZE) - (TILE_SIZE / 2)]) #- (self.size[1] - TILE_SIZE) - (self.size[1] / 2)])   

