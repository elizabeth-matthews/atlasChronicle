#!/usr/bin/python

import pygame
import background
import orb
import domex

class Manager(object):
  def __init__(self):
    gc = domex.GameConstants('xmlData/game.xml')
    self.WIDTH = gc.screenWidth
    self.HEIGHT = gc.screenHeight
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    pygame.display.set_caption("Moving red orbs Across the Screen")
    self.clock = pygame.time.Clock()

    self.background = background.Background('checkerboard.bmp') 
    self.orbs = pygame.sprite.Group()
    for index in range(0, gc.numberOrbs):
      self.orbs.add( orb.Orb('redball.png') )

  def runEventLoop(self):
    done = False
    while not done:
      self.clock.tick(40)
      for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE: done = True
      self.background.draw()
      self.orbs.draw(self.screen)
      self.orbs.update()
      pygame.display.flip()

if __name__ == "__main__":
  pygame.init()
  man = Manager()
  man.runEventLoop()
