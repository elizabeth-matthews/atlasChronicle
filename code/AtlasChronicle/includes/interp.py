import pygame, sys, os
from pygame.locals import *
from scipy import interpolate
import numpy as np
import random
from climates import *
from defines import *
import time
from panner import Panner

if __name__ == '__main__':
   
   pygame.init()
   
   random.seed() #1337)
   
   testType = "ff6" # random, ff6R1, ff6R2 or ff6
   displayClimateMap = True
   displayClimates = True
   width = 1024
   height = 576
   factor = 1
   
   RUN = True
      
   pygame.init()
   pygame.display.init()
   pan = Panner()
      
   window = pygame.display.set_mode((width,height))
   pygame.display.set_caption("Interpolation")
   screen = pygame.display.get_surface()
  
   tbmD = TerrainBoundaryMap()
   tbmD.default()
   tbmD.fill()
   tbmD.drawSelf()
   tbmD.drawLines()
   tbmD.clipped = True
   
   tbmF = TerrainBoundaryMap()
   tbmF.ff6_small()
   tbmF.fill()
   tbmF.drawSelf()
   tbmF.drawLines()
   tbmF.clipped = True
   
   if testType == "default":
      cm = ClimateMap(50,50)
      cm.setTBM(tbmD)
      
      for i in range(10):
         x = random.randint(4,46)
         y = random.randint(4,46)
         t = max(0.2, min(0.8, random.random()))
         h = max(0.2, min(0.8, random.random())) 
         cm.addPoint(x, y, [t, h])
   else:
      cm = ClimateMap(120,200,'cubic', False, 4)
      cm.setTBM(tbmF)
      
      cm.addPoint(100,  6,(0.25,0.50)) # Narshe
      cm.addPoint( 50,130,(0.75,0.50)) # Figaro
      cm.addPoint( 70,165,(0.50,0.50)) # Cave of Figaro
      cm.addPoint(100, 52,(0.50,0.75)) # Forest
      cm.addPoint( 90, 75,(0.50,0.25)) # Plains
      
   cm.addEdges()
   cm.fill()
   cm.drawSelf()
   cm.redraw = True
   
   pan.updateMax(800,800)
   pan.updateScreen(width,height)
   
   if testType == "default":
      active = [tbmD, cm]
      default = True
   else:
      active = [tbmF, cm]
      default = False
      
   
   a = 0
   canvas = pygame.Surface((width,height))
   index = 0
   
        
   while RUN:
      canvas.fill(COLORS["gray"])
      size = active[a].getCanvas().get_size()
      pan.updateMax(size[0], size[1])
      off = pan.getOffset()
      canvas.blit(active[a].getCanvas(), off)
      screen.blit(canvas, (0,0))
               
      pygame.display.flip()
               
      for event in pygame.event.get():
           
         if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
               
            #Exit
            RUN = False
         
         if event.type == KEYDOWN:
            if event.key == K_s:
               pygame.image.save(active[a].getCanvas(),
                                 "images/climate" + str(index) + ".png")
               index += 1
            elif event.key == K_RETURN:
               a = (a + 1) % len(active)
            elif event.key == K_LSHIFT:
               if default:
                  active[1].changeTBM(tbmF)
                  active[0] = tbmF
               else:
                  active[1].changeTBM(tbmD)
                  active[0] = tbmD
               default = not default
         
         if active[a] == cm:
            cm.handleEvent(event)
         
         pan.handleEvent(event)