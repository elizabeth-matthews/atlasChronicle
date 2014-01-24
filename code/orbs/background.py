import pygame
import helpers

class Background(pygame.sprite.Sprite):
  def __init__(self, pic):
    pygame.sprite.Sprite.__init__(self) 
    self.image, self.rect = helpers.load_image(pic, None)
    self.screen = pygame.display.get_surface()
    self.area = self.screen.get_rect()
    self.rect.topleft = (0, 0)
  def draw(self):
    self.screen.blit(self.image, (0, 0))
  def update(self): pass
