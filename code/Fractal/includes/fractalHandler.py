from pygame import Surface, display, init, time, event
from pygame.locals import *
import pygame

from helpers import FUNCTIONS

from math import sqrt, ceil

class ColorRange(object):
   def __init__(self, grain, width, height):
      self.__grain = grain
      self.__width = width
      self.__height = height
      self.__colorLocs = [0, self.__grain-1]
      self.__colors = [(0,0,0) for x in range(self.__grain)]
      self.__canvas = Surface((self.__width, self.__height))
      self.__canvas.fill((200,10,10))
      self.__purpleColorsRepeat()
      self.__redraw()
   
   def getColorAt(self, loc):
      return self.__colors[loc]
      
   def __defaultColors(self):
      colorList = [
         (0,255,150),(100,255,255),
         (0,130,80),(10,10,90),
         (0,90,60),(0,170,60)
         ]
   
      self.setColorsEqually(colorList)
      
   def __whiteBlackWhiteColors(self):
      colorList = [
         (255,255,255),(0,0,0),
         (255,255,255)
         ]
   
      self.setColorsEqually(colorList)
      
   def __lilacColors(self):
      colorList = [
         (85,50,70),(51,180,0),
         (170,102,170),(238,238,238),
         (204,136,221)
         ]
      
      self.setColorsEqually(colorList)
      
   def __fallColors(self):
      colorList = [
         (119,34,0),(255,102,0),
         (230,200,200),(85,51,17),
         (238,68,0),(255,204,119)
         ]
      
      self.setColorsEqually(colorList)
   def __purpleColorsRepeat(self):
      colorList = [
         (102,0,153),(204,153,255),
         (102,0,51),(255,102,255),
         (102,0,153)
         ]
      
      self.setColorsEqually(colorList)
      
   def __purpleColors(self):
      colorList = [
         (102,0,153),(180,200,200), 
         (0,0,102),(204,153,255),
         (102,0,51),(255,102,255),
         (51,0,51),(102,0,153)
         ]
      
      self.setColorsEqually(colorList)
      
   def __purpleColorsDouble(self):
   
      colorList = [
         (180,200,155), (  0,  0,102),
         (204,153,255), (102,  0, 51),
         (255,102,255), ( 51,  0, 51),
         (102,  0,153),
         (180,200,155), (  0,  0,102),
         (204,153,255), (102,  0, 51),
         (255,102,255), ( 51,  0, 51),
         (102,  0,153)
         ]
      
      self.setColorsEqually(colorList)
      
   def __rgbColors(self):
   
      colorList = [
         (255,  0,  0), (  0,255,  0),
         (  0,  0,  255)
         ]
      
      self.setColorsEqually(colorList)
      
   def __rainbowColors(self):
   
      colorList = [
         (255,  0,  0), (255,127,  0),
         (255,255,  0), (  0,255,  0),
         (  0,255,255),
         (  0,  0,255), ( 75,  0,130),
         (143,  0,255)
         ]
      
      self.setColorsEqually(colorList)
      
   def __rainbowColorsDouble(self):
   
      colorList = [
         (255,  0,  0), (255,127,  0),
         (255,255,  0), (  0,255,  0),
         (  0,255,255), (  0,  0,255),
         ( 75,  0,130), (143,  0,255),
         (255,  0,  0), (255,127,  0),
         (255,255,  0), (  0,255,  0),
         (  0,255,255), (  0,  0,255),
         ( 75,  0,130), (143,  0,255)
         ]
      
      self.setColorsEqually(colorList)
      
   def __rgbRainbowColorsDouble(self):
   
      colorList = [
         (255,  0,  0), (255,255,  0),
         (  0,255,  0), (  0,255,255),
         (  0,  0,255), (255,  0,255),
         (255,  0,  0), (255,255,  0),
         (  0,255,  0), (  0,255,255),
         (  0,  0,255), (255,  0,255)
         ]
      
      self.setColorsEqually(colorList)
       
   def draw(self, canvas, offset = (0,0)):
      canvas.blit(self.__canvas, offset)
      
   def __redraw(self):
      self.__canvas.fill((0,0,0))
      drawWidth = max(1,int(float(self.__width) / float(self.__grain))) + 1
      for c in range(self.__grain):
         drawPos = int(c * float(self.__width) / float(self.__grain))
         pygame.draw.rect(self.__canvas,
                          self.__colors[c],
                          Rect(drawPos,0,
                               drawWidth,self.__height))
   
   def doubleSize(self):
      self.__grain *= 2
      oldColors = [self.__colors[x] for x in self.__colorLocs]
      self.__colors *= 2
      self.setColorsEqually(oldColors)
      
   def doubleSizeRepeat(self):
      self.__grain *= 2
      self.__colors *= 2
      #oldColors = [self.__colors[x] for x in self.__colorLocs]
      self.__colorLocs = [int((float(x) / (len(self.__colors) - 1)) * self.__grain) for x in range(len(self.__colors))]
      self.__colorLocs[len(self.__colorLocs) - 1] = self.__grain - 1
      self.__redraw()
      #self.setColorsEqually(oldColors)
      
   def halveSizeRepeat(self):
      self.__grain /= 2
      self.__colors = self.__colors[0:self.__grain]
      self.__colorLocs = [int((float(x) / (len(self.__colors) - 1)) * self.__grain) for x in range(len(self.__colors))]
      self.__colorLocs[len(self.__colorLocs) - 1] = self.__grain - 1
      self.__redraw()
      #self.setColorsEqually(oldColors)
   
   def halveSize(self):
      self.__grain /= 2
      oldColors = [self.__colors[x] for x in self.__colorLocs]
      self.__colors = self.__colors[0:self.__grain]
      self.setColorsEqually(oldColors)
   
   def setColorsEqually(self, colors):
      
      self.__colorLocs = [int((float(x) / (len(colors) - 1)) * self.__grain) for x in range(len(colors))]
      self.__colorLocs[len(self.__colorLocs) - 1] = self.__grain - 1
      
      for l in range(len(self.__colorLocs)):
         self.__colors[self.__colorLocs[l]] = colors[l]
      
      for p in range(len(self.__colorLocs) - 1):
            
         self.__fillValues(self.__colorLocs[p], 
                           self.__colorLocs[p + 1])
      
      self.__redraw()
   
   def setColorsWeighted(self, colors):
      numColors = len(colors)
      
      self.__colorLocs = [x for x in range(numColors)]
      
      self.__colorLocs[numColors - 1] = self.__grain - 1
      currLoc = self.__grain
      
      
      for x in range(numColors - 2):
         currLoc = ceil(0.7 * currLoc)         
         self.__colorLocs[numColors - x - 2] = int(currLoc)
      
      
      
      for l in range(numColors):
         print l
         self.__colors[self.__colorLocs[l]] = colors[l]
      
      for p in range(len(self.__colorLocs) - 1):
            
         self.__fillValues(self.__colorLocs[p], 
                           self.__colorLocs[p + 1])
      
      self.__redraw()

   def setColorsAt(self, colors, locs):
      
      self.__colorLocs = locs
      
      for l in range(len(self.__colorLocs)):
         self.__colors[self.__colorLocs[l]] = colors[l]
      
      
      for p in range(len(self.__colorLocs) - 1):
            
         self.__fillValues(self.__colorLocs[p], 
                           self.__colorLocs[p + 1])
      
      self.__redraw()

   def setColorAt(self, color, loc):
      
      if not loc in self.__colorLocs:
         self.__colorLocs.append(loc)
         self.__colorLocs.sort()
      
      pos = self.__colorLocs.index(loc)
      self.__colors[loc] = color
      
      if pos - 1 >= 0:
         prev = self.__colorLocs[pos - 1]
         self.__fillValues(prev, loc)
      if pos + 1 < len(self.__colorLocs):
         post = self.__colorLocs[pos + 1]
         self.__fillValues(loc, post)
      
      self.__redraw()
      
   def delColorAt(self, loc):
      
      if len(self.__colorLocs) > 2:
         if loc in self.__colorLocs:
            ix = self.__colorLocs.index(loc)
            
            if ix != 0 and ix != len(self.__colorLocs)-1:
               prev = ix - 1
               self.__colorLocs.pop(ix)
               self.__fillValues(self.__colorLocs[prev],
                                 self.__colorLocs[ix])

      self.__redraw()
      
   def __fillValues(self, loc1, loc2):
      
      color1 = self.__colors[loc1]
      color2 = self.__colors[loc2]
      
      dr = float(color2[0] - color1[0])
      dg = float(color2[1] - color1[1])
      db = float(color2[2] - color1[2])
      
      steps = loc2 - loc1
      
      sdr = dr / steps
      sdg = dg / steps
      sdb = db / steps
      
      for s in range(steps):
         self.__colors[s + loc1] =(int(color1[0] + (sdr * s)),
                                   int(color1[1] + (sdg * s)),
                                   int(color1[2] + (sdb * s)))
      
class FractalGenerator(object):
   def __init__(self, grain, func, size, colorHeight):
      self.__colorHeight = colorHeight
      self.__size = size
      self.__canvas = Surface(self.__size)
      self.__canvas.fill((100,100,100))
      self.__func = FUNCTIONS[func]
      
      self.__start = self.__func.start 
      self.__range = self.__func.range 
      self.__scaleX = self.__range[0] / self.__size[0]
      self.__scaleY = self.__range[1] / self.__size[1]
      self.__maxIter = grain
      self.__limit = self.__func.limit
      self.colors = ColorRange(self.__maxIter,
                               self.__size[0],
                               self.__colorHeight)
      

   def doubleIter(self):
      self.__maxIter *= 2
      print "Iters:", self.__maxIter
      self.colors.doubleSizeRepeat()
      
   def halveIter(self):
      self.__maxIter /= 2
      self.colors.halveSizeRepeat()

   def zoomOut(self):
      
      self.__range = (self.__range[0] * 2, self.__range[1] * 2)
      self.__scaleX = self.__range[0] / self.__size[0]
      self.__scaleY = self.__range[1] / self.__size[1]
      
      self.move((-0.25,-0.25))
      
      
   def setSize(self, mousePos, drawSize):
      startx = mousePos[0] * self.__scaleX + self.__start[0]
      starty = mousePos[1] * self.__scaleY + self.__start[1]
      
      endx = drawSize[0] * self.__scaleX + startx
      endy = drawSize[1] * self.__scaleY + starty
      
      if startx > endx:
         startx,endx = endx,startx
      if starty > endy:
         starty,endy = endy,starty
      
      self.__start = (startx, starty)
      self.__range = (endx - startx, endy - starty)
      self.__scaleX = self.__range[0] / self.__size[0]
      self.__scaleY = self.__range[1] / self.__size[1]
      

   def move(self, mv):
         
      startx = self.__start[0] + self.__range[0] * mv[0]
      starty = self.__start[1] + self.__range[1] * mv[1]
      self.__start = (startx, starty)
            
      
      
   def iterate(self, z, c):
      nz = z
      nc = c
      for n in range(self.__maxIter):
         if self.__func.zF:
            nz = self.__func.zF(nz,nc)
         if self.__func.cF:
            nc = self.__func.cF(nz,nc)
         if sqrt(nz.real * nz.real + nz.imag * nz.imag) > self.__limit:
            return n
      return None
   
   def iterateRecursive(self, z, c, n = 0):
      if n < self.__maxIter:
         if self.__func.zF:
            nz = self.__func.zF(z,c)
         else:
            nz = z
         if self.__func.cF:
            nc = self.__func.cF(z,c)
         else:
            nc = c
         if sqrt(nz.real * nz.real + nz.imag * nz.imag) > self.__limit:
            return n
         else:
            return self.iterate(nz, nc, n+1)
      else:
         return None
      
   
   def regenerate(self, here, there):
      size = here[0] - there[0]
      
      for x in range(here[0], there[0]):
         for y in range(here[1], there[1]):
            xy = complex(x * self.__scaleX + self.__start[0],
                        y * self.__scaleY + self.__start[1])
            if self.__func.zInit == "xy":
               z = xy
            else:
               z = self.__func.zInit
            if self.__func.cInit == "xy":
               c = xy
            else:
               c = self.__func.cInit
               
            n = self.iterate(z,c)
            if n or n==0:
               # valid color
               color = self.colors.getColorAt(n)
            else:
               color = (0,0,0)
            
            pygame.draw.rect(self.__canvas, color,
                             Rect(x,y,2,2))
      
      #print ""
   
   def draw(self, canvas, offset = (0,0)):
      
      self.colors.draw(canvas, (0, self.__size[1]))
      
      canvas.blit(self.__canvas, offset)

class FractalHandler(object):
   def __del__(self):
      display.quit()
      
   def __init__(self, grain=100, func="mandel", size=(600,600), colorHeight=50):

      #Pygame stuff
      self.__windowSize = (size[0], size[1] + colorHeight)
      self.__size = size
      self.__colorHeight = colorHeight
      
      self.__initPython(self.__windowSize)
      self.__clock = time.Clock()
      self.__gen = FractalGenerator(grain, func, size, colorHeight)
      
      self.__RUN = True
      self.__generating = True
      self.__genSize = 50
      self.__genSpot = (0,0)
      
      self.__mouseDown = False
      self.__mouseDownPos = None
      self.__mouseCurrPos = None
      self.__highlightColor = (250,250,250)
      
      self.__dotCount = 0
      totalSections = (self.__size[0] / self.__genSize)
      totalSections *= totalSections
      
      self.__dotSize = totalSections / 10
      
      
      print "Generating",
     
   def __initPython(self, windowSize):
      self.__windowSize = windowSize
      
      self.__window = display.set_mode(self.__windowSize)
      display.set_caption("Fractal Engine")
      self.__screen = display.get_surface()
      
      self.__canvas = Surface(self.__windowSize)
      self.__canvas.fill((100,100,100))
     
   def run(self):

      self.__RUN = True
        
      while self.__RUN:
         
         timeSpent = self.__clock.tick(30)
         
         for e in event.get():
            self.__handleEvent(e)
            
         self.__update(timeSpent)
         self.__draw()
         
         self.__screen.blit(self.__canvas, (0,0))          
         display.flip()
         
 
   def __handleEvent(self, e):
      
      if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
      # Exit
         self.__RUN = False
      else:
         if not self.__generating:
            update = False
            if e.type == MOUSEBUTTONDOWN:
               if e.button == 1:
                  self.__mouseDown = True
                  self.__mouseDownPos = e.pos 
                  self.__mouseCurrPos = e.pos
            elif self.__mouseDown == True and e.type == MOUSEMOTION:
               self.__mouseCurrPos = e.pos 
            elif e.type == MOUSEBUTTONUP:
               if e.button == 1:
                  self.__gen.setSize(self.__mouseDownPos,self.__drawSize)
                  update = True
                  self.__mouseDown = False
               if e.button == 3:
                  self.__gen.zoomOut()
                  update = True
            elif e.type == KEYDOWN:
               if e.key == K_RIGHT:
                  self.__gen.move((0.5,0))
                  update = True
               elif e.key == K_LEFT:
                  self.__gen.move((-0.5,0))
                  update = True
               elif e.key == K_UP:
                  self.__gen.move((0,-0.5))
                  update = True
               elif e.key == K_DOWN:
                  self.__gen.move((0,0.5))
                  update = True
               elif e.key == K_PAGEUP:
                  print "Max Iterations Increased"
                  self.__gen.doubleIter()
                  update = True
               elif e.key == K_PAGEDOWN:
                  print "Max Iterations Increased"
                  self.__gen.halveIter()
                  update = True
                  
            
            if update:
               print "Regenerating",
               self.__generating = True
            

 
   def __update(self, ticks):
      if self.__generating:
         self.__dotCount += 1
         nextSpot = (self.__genSpot[0] + self.__genSize, self.__genSpot[1] + self.__genSize)
         self.__gen.regenerate(self.__genSpot, nextSpot)
         
         if nextSpot[0] >= self.__size[0]:
            nextSpot = (0,nextSpot[1])
         else:
            nextSpot = (nextSpot[0], nextSpot[1] - self.__genSize)
            
         if nextSpot[1] >= self.__size[1]:
            self.__generating = False
            self.__genSpot = (0,0)
            self.__dotCount = 0
            print "\nDone"
         else:
            if self.__dotCount % self.__dotSize == 0:
               print ".",
            self.__genSpot = nextSpot
      
   def __draw(self):
      
      self.__gen.draw(self.__canvas)
      
      
      if self.__mouseDown:
         diffX = self.__mouseCurrPos[0] - self.__mouseDownPos[0] 
         diffY = self.__mouseCurrPos[1] - self.__mouseDownPos[1]
         
         if diffX > 0 and diffY > 0:
            sizeX = max([diffX, diffY])
            sizeY = sizeX
         elif diffX > 0:
            sizeX = max([abs(diffX), abs(diffY)])
            sizeY = -sizeX
         elif diffY > 0:
            sizeY = max([abs(diffX), abs(diffY)])
            sizeX = -sizeY
         else:
            sizeX = min([diffX, diffY])
            sizeY = sizeX
         
            
         self.__drawSize = (sizeX, sizeY)
         
         pygame.draw.rect(self.__canvas, self.__highlightColor,
                          Rect(self.__mouseDownPos, self.__drawSize), 1)
      
      
      display.flip()
      display.update()
