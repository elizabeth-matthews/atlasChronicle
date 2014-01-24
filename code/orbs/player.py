import pygame
import random
import helpers
import math

class Orb(pygame.sprite.Sprite):
  image = None
  def __init__(self, pic):
    pygame.sprite.Sprite.__init__(self) 
    self.screen = pygame.display.get_surface()
    self.image, self.rect = helpers.load_image(pic, -1)
    new_size = random.randint(5, self.rect.width)
    self.image = pygame.transform.scale(self.image, (new_size, new_size))
    self.rect = self.image.get_rect()

    self.x = random.randint(0, self.screen.get_width())
    self.y = random.randint(0, self.screen.get_height()-self.rect.height)
    self.rect.topleft = (self.x, self.y)
    self.speedy = self.speedx = random.uniform(0.1, 0.3)
    self.curr_ticks = pygame.time.get_ticks()

  def update(self):
    prev_ticks = self.curr_ticks
    self.curr_ticks = pygame.time.get_ticks()
    ticks = self.curr_ticks - prev_ticks
    # distance = rate * time
    self.x += self.speedx * ticks
    self.y += self.speedy * ticks
    if self.x <= 0: self.speedx = math.fabs(self.speedx)
    if self.x+self.image.get_width() >= self.screen.get_width(): 
      self.speedx = -math.fabs(self.speedx)
    if self.y <= 0: 
      self.speedy = math.fabs(self.speedy)
    if self.y+self.image.get_height() >= self.screen.get_height(): 
      self.speedy = -math.fabs(self.speedy)
    self.rect.topleft = (self.x, self.y)
