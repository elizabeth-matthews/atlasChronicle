import pygame
from pygame.locals import *

class Panner(object):
    def __init__(self, maxX = -1, maxY = -1, screenX = -1, screenY = -1):
        self.mousePos = [0,0]
        self.offset = [0,0]
        self.mouseFlag = False
        self.maxX = maxX
        self.maxY = maxY
        self.screenX = screenX
        self.screenY = screenY
        
        self.centerX = self.screenX > self.maxX
        self.centerY = self.screenY > self.maxY
    
    def updateMax(self, maxX, maxY):
        self.maxX = maxX
        self.maxY = maxY
        
        self.centerX = self.screenX > self.maxX
        self.centerY = self.screenY > self.maxY
    
    def updateScreen(self, screenX, screenY):
        self.screenX = screenX
        self.screenY = screenY
        
        self.centerX = self.screenX > self.maxX
        self.centerY = self.screenY > self.maxY
    
    def handleEvent(self, event):
        if (not self.centerX) or (not self.centerY):
            if event.type == MOUSEBUTTONDOWN:
                self.mouseFlag = True
                self.mousePos = pygame.mouse.get_pos()
                
            elif event.type == MOUSEBUTTONUP:
                self.mouseFlag = False
                
                diff = self.mouseDiff()
                self.offset[0] += diff[0]
                self.offset[1] += diff[1]
                self.offset = self.capOffset(self.offset)
        
    def mouseDiff(self):
        currMouse = pygame.mouse.get_pos()
        return [currMouse[0] - self.mousePos[0],
                currMouse[1] - self.mousePos[1]] # Revserse to make sense
    
    def capOffset(self, off):
    
        if self.centerX:
            off[0] = ((self.screenX - self.maxX) / 2)
        else:
            off[0] = min(0, max(self.screenX - self.maxX, off[0]))
            
        if self.centerY:
            off[1] = ((self.screenY - self.maxY) / 2)
        else:
            off[1] = min(0, max(self.screenY - self.maxY, off[1]))
        
        return off
                
        
    def getOffset(self):
        off = [0,0]
        
        if self.mouseFlag:
            diff = self.mouseDiff()
            off = [self.offset[0] + diff[0], self.offset[1] + diff[1]]
        else:
            off = self.offset
            
        return self.capOffset(off)
        
        
    