#from msvcrt import getch

#BLACK = 0
#BLUE = 1
#GREEN = 2
#CYAN = 3
#RED = 4
#MAGENTA = 5
#BROWN = 6
#LIGHTGRAY = LIGHTGREY = 7
#DARKGRAY = DARKGREY = 8
#LIGHTBLUE = 9
#LIGHTGREEN = 10
#LIGHTCYAN = 11
#LIGHTRED = 12
#LIGHTMAGENTA = 13
#YELLOW = 14
#WHITE = 15


#import sys
import WConio
import random

from things import HealthPack, Player, Zombie, SuperZombie, Drawable

class Spawner(object):
   def __init__(self, r):
      self.count = 0
      self.targetRange = r
      self.target = random.randint(*self.targetRange)
   
   def incr(self):
      spawn = False
      self.count += 1
      if self.count == self.target:
         self.target = random.randint(*self.targetRange)
         self.count = 0
         spawn = True
      
      return spawn

class WorldInfo(object):
   def __init__(self, x, y):
      self.size = (x,y)
      self.player = None
      self.zombies = []
      self.healthPacks = []
      self.collideWho = None
      
   def collision(self, pos):
      #empty = True
      self.collideWho = None
      if pos[0] < 0 or pos[0] >= self.size[0] or \
         pos[1] < 0 or pos[1] >= self.size[1]:
         self.collideWho = 1 #self.player
         #empty = False
      
      if self.player.pos == pos:
         #empty = False
         self.collideWho = self.player
      
      else:
         for z in self.zombies:
            if z.pos == pos:
               #empty = False
               self.collideWho = z
         
         if not self.collideWho:
            for h in self.healthPacks:
               if h.pos == pos:
                  #empty = False
                  self.collideWho = h
      
      return not self.collideWho  
      

class GameManager(object):
   def __init__(self):
      
      random.seed()
      WConio.setcursortype(0)  # 0 no cursor, 1 normal, 2 block
      self.__size = (20,20)
      
      self.__zombieSpawner = Spawner((9,14))
      self.__healthSpawner = Spawner((10,16))
      
      self.__maxZombies = 10
      self.__maxHealthPacks = 10
      
      self.__RUN = True
      self.__wallColor = WConio.LIGHTGRAY
      self.__HUDColor = WConio.WHITE
      
      self.__wallCharacter = "#"
      
      startX = 1
      startY = 1
      
      self.__worldInfo = WorldInfo(*self.__size)
      self.__worldInfo.player = Player(startX, startY)
      
      self.__kills = 0
      self.__turns = 0
      
      
      self.__walls = []
      
      for x in xrange(self.__size[0]+2):
         self.__walls.append(Drawable(x,0,self.__wallCharacter,self.__wallColor))
         self.__walls.append(Drawable(x,self.__size[1]+1, self.__wallCharacter,self.__wallColor))
      
      for y in xrange(1,self.__size[1]+1):
         self.__walls.append(Drawable(0,y,self.__wallCharacter,self.__wallColor))
         self.__walls.append(Drawable(self.__size[0]+1,y,self.__wallCharacter,self.__wallColor))
   
   def run(self):
      while self.__RUN:
         self.__draw()
         userInput = WConio.getch()
         
         self.__update(userInput)
         self.__turns += 1
         
         spawn = self.__zombieSpawner.incr()
         if spawn:
            self.__spawnThing()
         
         spawn = self.__healthSpawner.incr()
         if spawn:
            self.__spawnThing("h")
            
      
   def __spawnThing(self, thing="z"):
      if thing == "z":
         amount = len(self.__worldInfo.zombies)
         maxSize = self.__maxZombies
      elif thing == "h":
         amount = len(self.__worldInfo.healthPacks)
         maxSize = self.__maxHealthPacks
         
      if amount < maxSize:
         
         empty = False
         
         while not empty:
            empty = True
            target = (random.randint(0,self.__size[0]-1),
                     random.randint(0,self.__size[1]-1))
            
            if self.__worldInfo.player.pos == target:
               empty = False
            
            if empty:
               for z in self.__worldInfo.zombies:
                  if z.pos[0] == target:
                     empty = False
               if empty:
                  for h in self.__worldInfo.healthPacks:
                     if h.pos[0] == target:
                        empty = False
               
         if thing == "z":
            self.__worldInfo.zombies.append(Zombie(*target))
         elif thing == "h":
            size = random.randint(1,10)
            self.__worldInfo.healthPacks.append(HealthPack(*target,size=size))
      
      
   def __draw(self):
      WConio.clrscr()
      
      # make walls
      for i in xrange(len(self.__walls)):
         self.__walls[i].draw()
         
      self.__worldInfo.player.draw((1,1))
      for z in self.__worldInfo.zombies:
         z.draw((1,1))
      for h in self.__worldInfo.healthPacks:
         h.draw((1,1))
      
      self.__drawHUD()
         
      WConio.gotoxy(0,self.__size[1] + 2)
      
   
   def __drawHUD(self):
      
      WConio.textattr(self.__HUDColor)
      
      WConio.gotoxy(self.__size[0]+4,1)
      print "--------HUD--------"
      WConio.gotoxy(self.__size[0]+4,3)
      print " Player Health:", self.__worldInfo.player.health
      WConio.gotoxy(self.__size[0]+4,4)
      print "         Kills:", self.__kills
      WConio.gotoxy(self.__size[0]+4,5)
      print "         Turns:", self.__turns
      
   
   def __update(self, userInput=None):
      if userInput:
         if userInput[1] in ["q", "\x1b"]:
            self.__RUN = False
         
         else:
            self.__worldInfo.player.update(userInput, self.__worldInfo)
            for z in self.__worldInfo.zombies:
               z.update(self.__worldInfo)
               
      