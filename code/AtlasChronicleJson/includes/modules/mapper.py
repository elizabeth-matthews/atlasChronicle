import pygame
from pygame.locals import *
from ..helpers.defines import *
import random

class PhysicalSeedInfo(object):
   def __init__(self):
      self.N = None
      self.S = None
      self.E = None
      self.W = None
      self.R = []
      self.A = "landfill"
   
   def hasSeeds(self):
      return self.N or self.S or self.E or self.W or self.R
   
   def add(self, direction, t):
      if direction == "R" and len(self.R) <= 4:
         self.R.append(t)
      elif direction == "A":
         self.A = t
      elif direction == "N":
         self.N = t
      elif direction == "S":
         self.S = t
      elif direction == "E":
         self.E = t
      elif direction == "W":
         self.W = t
   
   def randomizeR(self):
      while len(self.R) < 4:
         self.R.append(self.A)
      random.shuffle(self.R)

class SeedTileInfo(object):
   def __init__(self, t, key, name, loc):
      self.type = t
      self.key = key
      self.name = name
      self.loc = loc
      
      self.pSeeds = PhysicalSeedInfo()

class Restriction(object):
   def __init__(self):
      self.typed = True
      self.first = (-1, -1)
      self.second = (-1, -1)
      self.firstKey = None
      self.secondKey = None

class Tile(object):
   def __init__(self, t="none", key=None, name=None):
      self.type = t
      self.key = key
      self.name = name

   def save(self):
      s = "["
      
      s += "'type' : " + str(self.type)
      
      s += "]"
      
      return s

class Mapper(object):
   def __init__(self):
      self.x = -1
      self.y = -1
      self.map = []
      self.defaultType = "none"
      self.fillRatio = 0.5 # larger values means fill is more eager
      
      self.canvas = None
      self.canvasSize = (-1, -1)
      self.tileSize = MAPSCALE
      
      self.voidEdges = []
      self.fillEdges = []
      self.restrictedTiles = []
      self.updated = []
      
      self.restrictions = []
      self.restrictedDist = 2
      self.padding = 2
      
      self.animate = True
      self.pause = True
      self.identify = False
   
      self.done = False
      
      self.restrictedTypes = RESTRICTEDTYPES
      self.seedTiles = []
      
      self.minFilledX = 0
      self.minFilledY = 0
      self.maxFilledX = 0
      self.maxFilledY = 0
   
   def save(self):
      sOut = {
         "size"  : [self.x, self.y],
         "tiles" : []
      }
      
      for x in range(self.x):
         sOut["tiles"].append([])
         for y in range(self.y):
            tileInfo = self.map[x][y]
            if tileInfo.type not in TERRAINTYPES:
               t = tileInfo.key
            else:
               t = tileInfo.type
            sOut["tiles"][x].append(t)
      
      return sOut
      
   def getCanvas(self):
      return self.canvas

   def setMaxFilled(self, loc):
      if loc[0] > self.maxFilledX:
         self.maxFilledX = loc[0]
      elif loc[0] < self.minFilledX:
         self.minFilledX = loc[0]
      
      if loc[1] > self.maxFilledY:
         self.maxFilledY = loc[1]
      elif loc[1] < self.minFilledY:
         self.minFilledY = loc[1]

   def getMinDim(self):
      dim = ((self.maxFilledX - self.minFilledX) + 2,
             (self.maxFilledY - self.minFilledY) + 2)
   
      return dim

   def getMinOffset(self):
      return (self.minFilledX - 1, self.minFilledY - 1)

   def setUpdatedSize(self):
      # dummy for ease
      x = 0
   
   def getUpdatedSize(self):
      return False

   def setDefaultType(self, t="water"):
      self.defaultType = t
   
   def isDone(self):
      return self.done
   
   def setRestrictedTypes(self, types):
      self.restrictedTypes = types

   def distPointLine(self, pt, first, second):
      #from wikipedia
      lineLength = math.hypot(second[0]-first[0], second[1]-first[1])
      distance = abs((pt[0] - first[0]) * (second[1] - first[1]) - \
         (pt[1] - first[1]) * (second[0] - first[0])) / lineLength
   
      return distance
   
   def setSize(self, x, y):
      self.x = x + (self.padding * 2)
      self.y = y + (self.padding * 2)
      self.canvasSize = (self.x*self.tileSize,self.y*self.tileSize)
      self.canvas = pygame.Surface(self.canvasSize)
      self.initMap()
   
   def resetMap(self):
      self.map = [[Tile(self.defaultType) for y in range(self.y)] for x in range(self.x)]
      self.voidEdges = []
      self.fillEdges = []
      self.updated = []
      self.done = False
      self.minFilledX = self.x
      self.minFilledY = self.y
      self.maxFilledX = 0
      self.maxFilledY = 0
      self.setVoids()
      self.setSeedTiles()
      self.drawAll()
      
   def initMap(self):
      self.map = [[Tile(self.defaultType) for y in range(self.y)] for x in range(self.x)]
      self.voidEdges = []
      self.fillEdges = []
      self.seedTiles = []
      self.restrictedTiles = []
      self.updated = []
      self.restrictions = []
      self.done = False
      self.minFilledX = self.x
      self.minFilledY = self.y
      self.maxFilledX = 0
      self.maxFilledY = 0
      
   def setSeedTiles(self):
      for s in self.seedTiles:
         self.addTile(s.type, s.key, s.name, s.loc)
         locList = [[s.loc[0]-1, s.loc[1]],
                     [s.loc[0],   s.loc[1]-1],
                     [s.loc[0]+1, s.loc[1]],
                     [s.loc[0],   s.loc[1]+1]]
         if s.pSeeds.hasSeeds():
            s.pSeeds.randomizeR()
            for i in range(4):
               t = s.pSeeds.R[i]
               self.addTile(t, s.key, s.name, locList[i])
         elif s.type == "loi":
            for i in range(4):
               self.addTile("landfill", s.key, s.name, locList[i])
   
   def setup(self):
      self.setVoids()
      self.setRestrictedTiles()
      self.setSeedTiles()
      for x in range(self.x):
        for y in range(self.y):
            color = COLORS[self.map[x][y].type]
            pygame.draw.rect(self.canvas, color,
                             Rect(int(x*self.tileSize),
                                  int(y*self.tileSize),
                                  self.tileSize,
                                  self.tileSize))
   
   def setVoids(self):
      if len(self.seedTiles) != 0:
         for x in range(self.x):
            self.setVoidTile((x,0))
            self.setVoidTile((x,self.y-1))
            
         for y in range(self.y):
            self.setVoidTile((0,y))
            self.setVoidTile((self.x-1,y))
      else:
         for x in range(self.x):
            for y in range(self.y):
               self.setTile((x,y))
               self.done = True

   def setVoidTile(self, loc):
      self.setTile(loc)
      self.voidEdges.append(loc)
   
   def setTile(self, loc, t="void", key="void", name="void"):
      self.map[loc[0]][loc[1]].type = t
      self.map[loc[0]][loc[1]].key  = key
      self.map[loc[0]][loc[1]].name = name
   
   def addTile(self, t, key, name, loc):
      loc = (loc[0] + self.padding, loc[1] + self.padding)
      if t in RESTRICTEDTYPES or t == 'loi':
         self.setTile(loc,t,key,name)
      else:
         self.setTile(loc,'landfill',key,name)
         
      self.updated.append(loc)
      if t != 'loi':
         self.fillEdges.append(loc)
   
   def addSeedTile(self, t, key, name, loc, pSeeds = None):
      
      self.seedTiles.append(SeedTileInfo(t, key, name, loc))
      if pSeeds:
         # add different pSeeds
         ix = len(self.seedTiles) - 1
         for dr in pSeeds.keys():
            if dr != "R":
               self.seedTiles[ix].pSeeds.add(dr, pSeeds[dr])
            else:
               size = len(pSeeds["R"])
               for p in range(size):
                  self.seedTiles[ix].pSeeds.add("R", pSeeds["R"][p])
   
   def addRestriction(self, first, second, typed):
      r = Restriction()
      r.first = (first[0] + self.padding, first[1] + self.padding)
      r.second = (second[0] + self.padding, second[1] + self.padding)
      r.typed = typed
      self.restrictions.append(r)
   
   def setRestrictedTiles(self):      
      for x in range(self.x):
         for y in range(self.y):
            for r in self.restrictions:
               if r.typed:
                  dist = self.distPointLine((x, y), r.first, r.second)
                  if abs(dist) < self.restrictedDist:
                     #check distance to midpoint
                     midPoint = ((r.first[0] + r.second[0]) / 2, (r.first[1] + r.second[1]) / 2)
                     midDist = distance(midPoint, (x, y))
                     lineSize = distance(r.first, r.second)
                     if midDist < (lineSize / 2):
                        self.restrictedTiles.append((x,y))
         
      
   def draw(self):
      for u in self.updated:
         color = COLORS[self.map[u[0]][u[1]].type]
         pygame.draw.rect(self.canvas,color,
                          Rect(int(u[0]*self.tileSize),
                               int(u[1]*self.tileSize),
                               self.tileSize,
                               self.tileSize))
      
      self.updated = []
   
   def drawAll(self):
      for x in range(self.x):
         for y in range(self.y):
            color = COLORS[self.map[x][y].type]
            pygame.draw.rect(self.canvas,color,
                             Rect(int(x*self.tileSize),
                                  int(y*self.tileSize),
                                  self.tileSize,
                                  self.tileSize))
         
      
      self.updated = []
      
   def update(self):
      if not self.pause:
         if self.animate:
            self.floodFill()
         else:
            while not self.done:
               self.floodFill()
            
   def handleEvent(self, e, offset=None):
      
      if e.type == KEYDOWN:
         if e.key == K_1:
            self.pause = True
            if DEBUG:
               print "Paused Mapper"
         elif e.key == K_2:
            self.animate = not self.animate
            if DEBUG:
               print "Animate toggled:", self.animate
         elif e.key == K_3:
            self.identify = not self.identify
            if DEBUG:
               print "Identify toggled:", self.identify
         elif e.key == K_4:
            self.pause = False
            if DEBUG:
               print "Unpaused Mapper"
         elif e.key == K_RETURN:
            self.resetMap()
         
      elif e.type == MOUSEBUTTONDOWN:
         if self.identify:
            loc = pygame.mouse.get_pos()
            loc = (int(float(loc[0] - offset[0]) / float(self.tileSize)),
                   int(float(loc[1] - offset[1]) / float(self.tileSize)))
            
            print self.map[loc[0]][loc[1]].name

      
   def floodFill(self):
      
      if not self.done:
         split = random.random()
         coin = int(self.fillRatio < split)
         if coin == 0 and not self.fillEdges:
            coin = 1
         elif coin != 0 and not self.voidEdges:
            coin = 0
         if coin == 0:
            # pick randomly from fill edges
            index = random.randint(0, len(self.fillEdges)-1)
            pick = self.fillEdges[index]
         else:
            index = random.randint(0, len(self.voidEdges)-1)
            pick = self.voidEdges[index]
            
         viable = []
         fillType = self.map[pick[0]][pick[1]].type
         
         for ix in range(-1, 2):
            for iy in range(-1, 2):
               x = pick[0] + ix
               y = pick[1] + iy
               if abs(ix) != abs(iy) and \
                  x >= 0 and x < self.x and \
                  y >= 0 and y < self.y and \
                  self.map[x][y].type == "none" and \
                  ((x,y) not in self.restrictedTiles or fillType not in self.restrictedTypes):
                  # also check for reserved types
                  viable.append((x,y))
                  
         
         if viable:
            fill = random.randint(0,len(viable)-1)
            loc = viable[fill]
            
            pickTile = self.map[pick[0]][pick[1]]
            t = pickTile.type 
            key = pickTile.key 
            name = pickTile.name
            
            if not name.endswith(", fill"):
               name += ", fill"
            self.setTile(loc, t, key, name)
            
            if loc[0] < self.minFilledX:
               self.minFilledX = loc[0]
            if loc[0] > self.maxFilledX:
               self.maxFilledX = loc[0]
            if loc[1] < self.minFilledY:
               self.minFilledY = loc[1]
            if loc[1] > self.maxFilledY:
               self.maxFilledY = loc[1]
               
            self.updated.append(loc)
            
            if coin == 0:
               self.fillEdges.append(loc)
            else:
               self.voidEdges.append(loc)
            
         else:
            if coin == 0:
               self.fillEdges.remove(pick)
            else:
               self.voidEdges.remove(pick)
               
            self.done = not (self.fillEdges or self.voidEdges)
            