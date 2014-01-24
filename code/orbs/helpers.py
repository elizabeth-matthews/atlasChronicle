import sys, os, pygame
import pygame.locals

def load_image(name, colorkey=None):
  fullname = os.path.join('images', name)
  try:
    image = pygame.image.load(fullname)
  except pygame.error, message:
    print 'Cannot load image:', fullname
    raise SystemExit, message
  image = image.convert()
  if colorkey is not None:
    if colorkey is -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
  return image, image.get_rect()

if __name__ == '__main__': 
  if len(sys.argv) != 2:
    print "usage: ", sys.argv[0], " <file to load>"
    sys.exit()
  pygame.init()
  screen = pygame.display.set_mode((640, 480))
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill( (255, 255, 255) )
  screen.blit(background, (0, 0))
  image, rect = load_image(sys.argv[1])
  screen.blit(image, (100, 100))
  pygame.display.flip()
  print "Test successful: your image loaded successfully!"
