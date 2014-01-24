import pygame, sys, os
from pygame.locals import *

from panner import Panner


if __name__ == '__main__':
    
    pygame.init()
    
    width  = 500
    height = 500
    fullWidth  = 1000
    fullHeight = 1000
    
    pan = Panner(1000, 1000, 500, 500)
    
        
    screenCanvas = pygame.Surface((width, height))
    fullCanvas = pygame.Surface((fullWidth, fullHeight))
    
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Interpolation")
    screen = pygame.display.get_surface()
    
    screenCanvas.fill((20,0,0))
    
    for x in range(fullWidth / 10):
        for y in range(fullHeight / 10):
            color = (100,100,100)
            if ((x / 10) + (y / 10)) % 2 == 0:
                color = (200,200,200)
            pygame.draw.rect(fullCanvas, color,
                             Rect(int(x*10),int(y*10),10,10))
    
    print pan.getOffset()
    
    RUN = True
    while RUN:
        screenCanvas.blit(fullCanvas, pan.getOffset())
        screen.blit(screenCanvas, (0,0))
                
        pygame.display.flip()
                
        for event in pygame.event.get():
            
            pan.handleEvent(event)
            
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                
                # Exit
                    RUN = False
    

                    
    pygame.quit()