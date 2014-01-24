from scipy import interpolate
import numpy
import noiselib
import pygame
from noiselib.modules.main import RescaleNoise
from pygame.locals import *

from ..helpers.defines import dist
from ..helpers.defines import COLORS

import copy

class NoiseStats(object):
    # Glorified struct to hold all the info about the noise fucntion and levels.
    def __init__(self, oct = 4, persist = 0.8, src = noiselib.simplex_noise3,
                 offsets=[10,20]):
        self.octaves = oct
        self.persist = persist
        self.source = src
        self.offsets = offsets
        self.scale = 3.0 #(400.0 / pow(2, oct))
        self.weight = .2


class Terrain(object):
    # Climate is an average humidity and temperature for a particular terrain.
    # Also given a terrain name (name) and color.
    def __init__(self, name="", t=0, h=0, c=(127,127,127)):
        self.name = name
        self.temperature = t
        self.humidity = h
        self.color = c

class TerrainBoundaryMap(object):
    # ClimateMap is for defining what climates are where based on humid/temp.
    # Humid and temp values go from 0..999
    # 0.199 and 800..999 should be reserved for buffer/extremes
    def __init__(self):
        self.w = 1000
        self.h = 1000
        self.clippedw = 600
        self.clippedh = 600
        self.canvas = pygame.Surface((1000, 1000))
        self.clippedCanvas = pygame.Surface((600, 600))
        self.t = 'nearest'
        self.terrainLocations = []
        
        self.gridX, self.gridY = numpy.mgrid[0:self.w, 0:self.h]
        self.grid = None
        
        self.clipped = True
    
    def getCanvas(self):
        if self.clipped:
            return self.clippedCanvas
        else:
            return self.canvas

    def drawSelf(self):
        for x in range(self.w):
            for y in range(self.h):
                ix = float(x)/float(self.w)
                iy = float(self.h-y-1)/float(self.h)
                color = self.getColor(ix,iy)
                pygame.draw.rect(self.canvas, color,
                                 Rect(x,y,2,2))
                if x >= 200 and x < 800 and y >= 200 and y < 800:
                    pygame.draw.rect(self.clippedCanvas, color,
                                     Rect(x-200,y-200,2,2))
    
    
    
    def drawLines(self, size = 0.1):
        incrs = []
        i = 0.0
        while i < 1.0:
            incrs.append(i)
            i += size
            
        for i in incrs:
            x = int(i * self.w)
            y = int(i * self.h)
            pygame.draw.line(self.canvas, (255,255,255),
                                (x,   0),
                                (x, 999))
            pygame.draw.line(self.canvas, (255,255,255),
                                (  0, y),
                                (999, y))
            
            if x >= 200 and x < 800 and y >= 200 and y < 800:
                pygame.draw.line(self.clippedCanvas, (255,255,255),
                                    (x - 200, 0),
                                    (x - 200, 599))
                pygame.draw.line(self.clippedCanvas, (255,255,255),
                                    (0, y - 200),
                                    (599, y - 200))
                

    def add(self, name="", t=0.0, h=0.0, c=(127,127,127)):
        # Add climate n at temp t and humidity h with color c.
        names = [x.name for x in self.terrainLocations]
        if name not in names:
            self.terrainLocations.append(Terrain(name, t, h, c))
        
    def change(self, name="", t=0, h=0, c=(127,127,127)):
        # Change climate n to new values.
        names = [x.name for x in self.terrainLocations]
        if name in names:
            self.terrainLocations.append(Terrain(name, t, h, c))
    
    def remove(self, name=""):
        # Remove climate n
        
        names = [x.name for x in self.terrainLocations]
        if name in names:
            i = self.terrainLocations.index(name)
            self.terrainLocations.pop(i)
            
    def default(self):
        # Default climates for ease of testing.
        self.add("tundra",  0.2, 0.2, (190, 255, 255))#TERRAINCOLORS["tundra"])
        self.add("snow",    0.2, 0.8, (190, 190, 255))#TERRAINCOLORS["snow"])
        self.add("forestC", 0.3, 0.5, (  0,  60,   0))#TERRAINCOLORS["forestC"])
    
        self.add("plains",    0.5, 0.2, (150, 150,  89))#TERRAINCOLORS["plains"])
        self.add("grassland", 0.5, 0.5, ( 38, 198,  79))#TERRAINCOLORS["grassland"])
        self.add("forestD",   0.5, 0.8, (100, 200, 160))# TERRAINCOLORS["forestD"])
    
        self.add("desert",  0.8, 0.2, (255, 255, 102))#TERRAINCOLORS["desert"])
        self.add("swamp",   0.7, 0.5, (100,   0,  80))#TERRAINCOLORS["swamp"])
        self.add("forestR", 0.8, 0.8, (  0,  80,  80))#TERRAINCOLORS["forestR"])
    
    def ff6_small(self):
        # Default climates for ease of testing.
        self.add("snow",      0.2, 0.5, (190, 190, 255))#TERRAINCOLORS["snow"])    
        self.add("plains",    0.5, 0.2, (150, 150,  89))#TERRAINCOLORS["plains"])
        self.add("grassland", 0.5, 0.5, ( 38, 198,  79))#TERRAINCOLORS["grassland"])
        self.add("forest",    0.5, 0.8, (  0,  58,   2))#TERRAINCOLORS["forest"])
        self.add("desert",    0.8, 0.5, (255, 255, 102))#TERRAINCOLORS["desert"])
    
    def ff6(self):
        # Default climates for ease of testing.
        self.add("tundra",    0.2, 0.2, (190, 255, 255))#TERRAINCOLORS["tundra"])
        self.add("snow",      0.2, 0.8, (190, 190, 255))#TERRAINCOLORS["snow"])
        self.add("plains",    0.5, 0.2, (150, 150,  89))#TERRAINCOLORS["plains"])
        self.add("grassland", 0.5, 0.5, ( 38, 198,  79))#TERRAINCOLORS["grassland"])
        self.add("forestC",   0.5, 0.8, (  0,  60,   0))#TERRAINCOLORS["forestC"])
        self.add("desert",    0.8, 0.2, (255, 255, 102))#TERRAINCOLORS["desert"])
        self.add("forestR",   0.8, 0.8, (  0,  80,  80))#TERRAINCOLORS["forestR"])
    
    def fill(self):
        # Costly.  Fill up the climate map based on key climates.
        # Don't call this unless absolutely needed!
        locs   = []
        vals   = []
        
        for i in range(len(self.terrainLocations)):
            vals.append(i)
            locs.append([int(self.terrainLocations[i].temperature * self.w),
                         int(self.terrainLocations[i].humidity * self.h)])
        
        locs = numpy.array(locs)
        vals = numpy.array(vals)
        
        self.grid = interpolate.griddata(locs, vals, (self.gridX, self.gridY), method=self.t, fill_value=-1)
    
    def getVal(self, x, y):
        # Get value.  Shouldn't be used, as this is just an indexing.
        if self.grid:
            return self.grid[x*self.w-1][y*self.h-1]
        
    def getName(self, x, y):
        # Get the name of the climate at location.
        #if self.grid:
        i = self.grid[x*self.w-1][y*self.h-1]
        return self.terrainLocations[i].name
        
    def getColor(self, x, y):
        # Get the color of the climate at location.
        if self.grid != None:
            i = self.grid[x*self.w-1][y*self.h-1]
            return self.terrainLocations[i].color

class ClimateMap(object):
    def __init__(self, w, h, t='linear', noisy=True, scale=8, nVals=2):
        # Width and height should be world coordinates, not pixels.
        # t indicates the type of interpolation.  Linear is default and fastest.
        # n is boolean for noise to be added
        # nVals is for if a map needs to be created with more than two values
        #  (More than just humidity, temperature.)  Not fully implemented yet.
        self.width = w
        self.height = h
        self.scale = scale
        
        self.grid_x, self.grid_y = numpy.mgrid[0:w, 0:h]
        self.locations   = []
        
        self.vals = []
        for n in range(nVals):
            self.vals.append([])
        
        self.type = t
        self.noisy = noisy
        self.noiseStat = NoiseStats()
        
        #if self.noisy:
        noiselib.init(256) # Don't touch this!
                
        self.noises = noiselib.fBm(self.noiseStat.octaves,
                                        self.noiseStat.persist,
                                        self.noiseStat.source)
        
        self.filled = False
        self.canvas = pygame.Surface((self.width * self.scale,
                                      self.height * self.scale))
    
        self.drawClimate = True
        self.tbm = None
        self.redraw = False
        self.defaultClimate = (0.5, 0.5)
        self.averageClimate = False
        self.drawType = 0 # "loi", "edges", "climate" or "terrain"
        self.drawSequence = ["loi", "edges", "climate", "terrain"]
        
        self.loi = []
        self.edges = []
    
    def handleEvent(self, e):
        ret = False
        if e.type == KEYDOWN:
            if e.key == K_END:
               self.changeNoisy()
               ret = True
            elif e.key == K_RSHIFT:
               self.changeDraw()
               ret = True
            elif e.key == K_UP:
               self.increaseNoisy()
               ret = True
            elif e.key == K_DOWN:
               self.decreaseNoisy()
               ret = True
        
        return ret
            
               
    
    def setTBM(self, tbm):
        self.tbm = tbm
    
    def changeTBM(self, tbm):
        self.tbm = tbm
        if self.redraw:
            self.drawSelf()
    
    def getCanvas(self):
        return self.canvas
    
    def changeNoisy(self):
        self.noisy = not self.noisy
        if self.redraw:
            self.drawSelf()
    
    def increaseNoisy(self):
        self.noiseStat.weight += 0.01
        if self.redraw:
            self.drawSelf()
    
    def decreaseNoisy(self):
        self.noiseStat.weight -= 0.01
        if self.redraw:
            self.drawSelf()
    
    def changeDraw(self):
        self.drawType = (self.drawType + 1) % len(self.drawSequence)
        print self.drawSequence[self.drawType]
        #self.drawClimate = not self.drawClimate
        if self.redraw:
            self.drawSelf()
    
    def drawSelf(self):
        self.canvas.fill((255,255,255))
        for x in range(self.width):
            for y in range(self.height):
                dType = self.drawSequence[self.drawType]
                if dType == "terrain" or dType == "climate" or \
                  (dType == "edges" and \
                   ([x,y] in self.edges or [x,y] in self.loi)) or \
                  (dType == "loi" and [x,y] in self.loi):
                
                    vals = self.getVals(x, y)
                    tempVal = float(vals[0])
                    humidVal = float(vals[1])
                    midVal = 0
                    
                    if dType != "terrain":
                        #if tempVal == 1.0 and humidVal == 1.0:
                        #    midVal = 255
                        color = (tempVal*255, midVal, humidVal*255)
                    else:
                        color = self.tbm.getColor(tempVal, humidVal)
                        
                    pygame.draw.rect(self.canvas, color,
                                     Rect(int(x*self.scale),
                                          int(y*self.scale),
                                          max(2,self.scale),
                                          max(2,self.scale)))
                    
        
    def addPoint(self, x, y, vals):        
        self.locations.append([x, y])
        self.loi.append([x,y])
        for i in range(len(vals)):
            self.vals[i].append(vals[i])
        
    def addPoints(self, xs, ys, vals):
        for i in range(len(xs)):
            self.addPoint(xs[i], ys[i], vals)
    
    def addEdges(self):
        # only call after all points are added.
        # Adds averages to points:
        #      1
        #  0 _____ 2
        #   |     |
        # 7 |     | 3
        #   |_____|
        #  6   5   4
        #
        # Based on distance, but it's tricky because it is based on wrapping.
        # Things in the area of 0,0 are closer to pt 5 than pt 1.
        
        # point = [locx, locy, [temp, humid]]
        pt0 = [0,            0]
        pt1 = [self.width/2, 0]
        pt2 = [self.width-1, 0]
        pt3 = [self.width-1, self.height/2]
        pt4 = [self.width-1, self.height-1]
        pt5 = [self.width/2, self.height-1]
        pt6 = [0,            self.height-1]
        pt7 = [0,            self.height/2]
        points = [pt0, pt1, pt2, pt3, pt4, pt5, pt6, pt7]
        
        
        avgVal = self.defaultClimate
        
        if self.averageClimate:
            avgVal = [0,0]    
            for l in range(len(self.locations)):
                avgVal[0] += self.vals[0][l] 
                avgVal[1] += self.vals[1][l] 
                           
            avgVal[0] /= len(self.locations)
            avgVal[1] /= len(self.locations)
            
        for pt in points:
            self.addPoint(pt[0], pt[1], avgVal)
            self.edges.append(pt)
        
        self.loi = [x for x in self.loi if x not in self.edges]
            
     
    def fill(self):
        self.filled = True
        locs   = numpy.array(self.locations)
        vals   = []
        for i in range(len(self.vals)):
            vals.append(numpy.array(self.vals[i]))
        self.grids = []
        for i in range(len(self.vals)):
            self.grids.append(interpolate.griddata(locs, vals[i], (self.grid_x, self.grid_y), method=self.type, fill_value=0))
        
    def getVals(self, x, y):
        ret = []
        if self.filled:
            for i in range(len(self.vals)):
                extra = 0.0
                if self.noisy:
                    extra = ((self.noises([float(x)/self.noiseStat.scale,
                                           float(y)/self.noiseStat.scale,
                                           i]))) * self.noiseStat.weight
                                           #float(self.noiseStat.offsets[i])]))) * self.noiseStat.weight
                ret.append(max(min(self.grids[i][x][y] + extra, 1.0), 0.0))
        else:
            for l in range(len(self.locations)):
                if self.locations[l][0] == x and self.locations[l][1] == y:
                    ret = [self.vals[0][l], self.vals[1][l]]
            if len(ret) == 0.0:
                ret = [1.0,1.0]
                
                
        return ret
        
    def clear(self):
        self.locations   = []
        self.vals  = []
    
