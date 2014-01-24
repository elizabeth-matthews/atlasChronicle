import pygame, sys, os
from pygame.locals import *
from defines import *

if __name__ == '__main__':
    
    pygame.init()
    width = 1000
    height = 700
    font = pygame.font.Font(None, 36)
    
    fullCanvas = pygame.Surface((width, height))
    
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("MapKey")
    screen = pygame.display.get_surface()
    
            
    fullCanvas.fill(COLORS["graydk"])
    spot = [5,5]
    size = 25
    cols = ["loi","landfill","grassland","snow","forest","mountain","joint","jointT",
            "none","void","","desert","plains","water","spring","springT"]
    #cols.sort()
    for color in cols:
        if color != "":
            pygame.draw.rect(fullCanvas, COLORS[color], Rect(spot[0],
                             spot[1], size, size))
            text = font.render(color, 1, (255,255,255))
            fullCanvas.blit(text,(spot[0]+30, spot[1]))
        spot[1] = spot[1] + 25
        if color == "jointT":
            spot = [160, 5]
            
    
    RUN = True
    while RUN:
        screen.blit(fullCanvas, (0,0))
                
        pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                
                # Exit
                    RUN = False
                
    pygame.quit()