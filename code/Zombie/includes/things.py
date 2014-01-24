
import WConio
import random

class Drawable(object):
   def __init__(self, x, y, char="?", color=WConio.WHITE):
      self.pos = (x,y)
      self.char = char
      self.color = color
   
   def draw(self, offset=(0,0)):
      WConio.textcolor(self.color)
      WConio.gotoxy(self.pos[0] + offset[0],
                    self.pos[1] + offset[1])
      print self.char

class HealthPack(Drawable):
   def __init__(self, x, y, size, littleChar="h", bigChar="H", color=WConio.LIGHTRED):
      if size < 5:
         char = littleChar
      else:
         char = bigChar
      
      super(HealthPack, self).__init__(x,y,char,color)
      self.size = size
      
      
   
class Healthy(Drawable):
   def __init__(self, x, y, health, attack, accuracy,
                char="?", color=WConio.WHITE):
      super(Healthy,self).__init__(x,y,char,color)
      self.health = health
      self.attack = attack
      self.accuracy = accuracy
      self.intendedDir = (0,0)
   
   def update(self, worldInfo):
      if self.intendedDir != (0,0):
         pos = (self.pos[0] + self.intendedDir[0],
                self.pos[1] + self.intendedDir[1])
         worldInfo.collision(pos)
         if not worldInfo.collideWho:
            self.pos = pos
         

class Zombie(Healthy):
   def __init__(self, x, y, health=10, attack=1, accuracy=70,
                lifespan=10, char="Z", color=WConio.GREEN):
      super(Zombie,self).__init__(x,y,health,attack,accuracy,char,color)
      self.lifespan=10
   
   def update(self, worldInfo):
      coin = random.randint(0,5)
      
      if coin == 0:
         self.intendedDir = (0,1)
      elif coin == 1:
         self.intendedDir = (0,-1)
      elif coin == 2:
         self.intendedDir = (1,0)
      elif coin == 3:
         self.intendedDir = (-1,0)
      else:
         self.intendedDir = (0,0)
      
      super(Zombie,self).update(worldInfo)

class SuperZombie(Zombie):
   def __init__(self, x, y, health=12, attack=2, accuracy=85,
                lifespan=20, char="S", color=WConio.GREEN):
      super(SuperZombie,self).__init__(x,y,health,attack,accuracy,lifespan,char,color)
      self.__smartRatio = 50
   
   def update(self, worldInfo):
      
      super(Zombie,self).update(worldInfo)

class Player(Healthy):
   def __init__(self, x, y, health=20, attack=2, accuracy=90,
                char="@", color=WConio.WHITE):
      super(Player,self).__init__(x,y,health,attack,accuracy,char,color)
   
   
   def update(self, userInput, worldInfo):
      
      if userInput[1] in ["w", "W"]:
         self.intendedDir = (0,-1)
      elif userInput[1] in ["s", "S"]:
         self.intendedDir = (0,1)
      elif userInput[1] in ["a", "A"]:
         self.intendedDir = (-1,0)
      elif userInput[1] in ["d", "D"]:
         self.intendedDir = (1,0)
      else:
         self.intendedDir = (0,0)
      
      super(Player,self).update(worldInfo)
   
      if worldInfo.collideWho:
         if isinstance(worldInfo.collideWho,HealthPack):
            self.health += worldInfo.collideWho.size
       