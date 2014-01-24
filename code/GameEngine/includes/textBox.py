from pygame import Surface, font, draw, Rect
from pygame.locals import *


class TextBox(object):
   def __init__(self, txt="Hello, World!"):
      self.text = txt
      self.__height = 15
      self.__width = self.__height * (12.0 / 20.0)
      self.__cols = 50
      self.__rows = 7
      self.__accentSize= 10
      self.__lineBuff = 2
      self.__lineHeight = self.__height + self.__lineBuff
      self.__buffer = (self.__accentSize + 4,self.__accentSize + 4)
      
      self.__size = ((self.__buffer[0] * 2) + self.__cols * self.__width  + 1,
                     (self.__buffer[1] * 2) + self.__rows * self.__lineHeight)
      
      self.__canvas = Surface(self.__size)
      self.__box = Surface(self.__size)      
      self.__myFont = font.SysFont("courier", self.__height)
      self.__color = (255,255,0)
      self.__bgColor = (0,0,100)
      self.__edgeColor = (255,255,200)
      self.__transparent = (255,0,255)
      self.__cursor = 0
      self.__nextCue = "(Press Space)"
      

      self.__canvas.set_colorkey(self.__transparent)
      self.__box.set_colorkey(self.__transparent)
      
      self.__preDrawBox()
   
   def reset(self):
      self.__cursor = 0
      self.__renderText()
   
   def __preDrawBox(self):
      # full of magic numbers... :(
      
      self.__box.fill(self.__transparent)
      boxExtra = 5
      
      area = Rect((self.__accentSize - 2, self.__accentSize - 2),
                  (self.__size[0] - self.__accentSize * 2 + 3, self.__size[1] - self.__accentSize * 2 + 3))
      draw.rect(self.__box, self.__edgeColor, area, 2)
      
      area = Rect(0,0,
                  self.__accentSize + boxExtra,
                  self.__accentSize + boxExtra)
      draw.rect(self.__box, self.__edgeColor, area, 2)
      area = Rect(self.__size[0]-self.__accentSize-1-boxExtra,0,
                  self.__accentSize + boxExtra,
                  self.__accentSize + boxExtra)
      draw.rect(self.__box, self.__edgeColor, area, 2)
      area = Rect(self.__size[0]-self.__accentSize-1-boxExtra,
                  self.__size[1]-self.__accentSize-1-boxExtra,
                  self.__accentSize + boxExtra,
                  self.__accentSize + boxExtra)
      draw.rect(self.__box, self.__edgeColor, area, 2)
      area = Rect(0,self.__size[1]-self.__accentSize-1-boxExtra,
                  self.__accentSize+boxExtra,
                  self.__accentSize+boxExtra)
      draw.rect(self.__box, self.__edgeColor, area, 2)
      
      
      
      area = Rect((self.__accentSize, self.__accentSize),
                  (self.__size[0] - (self.__accentSize * 2),
                   self.__size[1] - (self.__accentSize * 2)))
      draw.rect(self.__box, self.__bgColor, area)
      
      
      
      area = Rect(2,2,
                  self.__accentSize - 3 + boxExtra,
                  self.__accentSize - 3 + boxExtra)
      draw.rect(self.__box, self.__bgColor, area)
      area = Rect(self.__size[0]-self.__accentSize-1 + 2 - boxExtra,2,
                  self.__accentSize - 3 + boxExtra,
                  self.__accentSize - 3 + boxExtra)
      draw.rect(self.__box, self.__bgColor, area)
      area = Rect(self.__size[0]-self.__accentSize-1 + 2 - boxExtra,
                  self.__size[1]-self.__accentSize-1 + 2 - boxExtra,
                  self.__accentSize - 3 + boxExtra,
                  self.__accentSize - 3 + boxExtra)
      draw.rect(self.__box, self.__bgColor, area)
      area = Rect(2,self.__size[1]-self.__accentSize-1 + 2 - boxExtra,
                  self.__accentSize - 3 + boxExtra,
                  self.__accentSize - 3 + boxExtra)
      draw.rect(self.__box, self.__bgColor, area)
      
      
   def __renderText(self):
      self.__canvas.fill(self.__transparent)
      self.__canvas.blit(self.__box, (0,0))
      pageDone = False
      y = 0
      
      while not pageDone:
         
         skip = 1
         
         nextCursor = self.__cursor + self.__cols
         while nextCursor < len(self.text) and self.text[nextCursor] not in [' ', '\n', '\t']:
            nextCursor -= 1
         if nextCursor >= len(self.text):
            nextCursor = len(self.text)-1
         
         nIx = self.text[self.__cursor:nextCursor+1].find('\n')
         tIx = self.text[self.__cursor:nextCursor+1].find('\t')
         
         
         if tIx != -1:
            nextCursor = tIx + self.__cursor
            pageDone = True
            skip = 0
         elif nIx != -1:
            nextCursor = nIx + self.__cursor
            skip = 0
         elif self.text[nextCursor] == ' ':
            skip = 0
            
            
         rendered = self.__myFont.render(self.text[self.__cursor:nextCursor+skip], 1, self.__color, self.__bgColor)
         self.__canvas.blit(rendered, (self.__buffer[0],
                                       self.__buffer[1] + y * self.__lineHeight))
         
         self.__cursor = nextCursor +1
         y += 1
         
         if y >= self.__rows - 1:
            pageDone = True
            
   
      rendered = self.__myFont.render(" " * (self.__cols - len(self.__nextCue)) + self.__nextCue,
                                      1, self.__color, self.__bgColor)
      self.__canvas.blit(rendered, (self.__buffer[0],
                                    self.__buffer[1] + (self.__rows - 1) * self.__lineHeight))
         
   
   def handleEvent(self, e):
      done = False
      if e.type == KEYDOWN and e.key == K_SPACE:
         if self.__cursor >= len(self.text) - 2:
            done = True
            self.reset()
         else:
            self.__renderText()
         
      
      return done
   

   
   def draw(self, canvas, location):
      center = (location[0] / 2) - (self.__size[0] / 2)
      
      canvas.blit(self.__canvas, (center,5))



class TextBoxManager(object):
   def __init__(self):
      # Holds textboxes
      self.__boxes = {
         "Help"           : [TextBox("---------------------Controls---------------------\n" +
                                     "SPACE:      Interact with current tile.\n" +
                                     "ARROW KEYS: Move around.\n" +
                                     "I:          View inventory.\n" +
                                     "H:          View this help page again.\n" +
                                     "M:          Show/Hide minimap.")],
         "StarterTown"    : [TextBox("No one in Starter Town has much to say."),
                             TextBox("Welcome to Starter Town! A npc greets you.\n\n" +
                                     " \"Hello, good adventurer! Let's skip to the chase:" +
                                     " In order to defeat the evil gaining power at Final" +
                                     " Palace, You must search the world for the three" +
                                     " crystals of the triforce! Where are they? How" +
                                     " should I know?! I'm just the first NPC. Why don't" +
                                     " you try the town nearby in the desert to the {0}?" +
                                     " Come back here when you've gotten them all.\""),
                             TextBox("\"Ah, you've gotten them all! Now maybe you should" +
                                     " try to find the final dungeon. Or maybe look for" +
                                     " that secret weapon I'd heard rumors about. Did you" +
                                     " try searching the Thief Hideout again?\""),
                             TextBox("\"Ah, you've gotten them all! And you've found the" +
                                     " secret weapon as well! Now maybe you should" +
                                     " try to find the final dungeon.\"")],
         "DesertTown"     : [TextBox("No one in Desert Town has much to say."),
                             TextBox("Upon reaching Desert Town, another NPC finds you." +
                                     "  \"Looking for the first Crystal? I heard there's" +
                                     " a palace to the {0} in the desert that only" +
                                     " the COURAGEOUS can enter. Seems like a clue," +
                                     " give it a shot!\""),
                             TextBox("Now that you have the Crystal of Courage," +
                                     " someone else in Desert Town mentions the" +
                                     " next way to go. \"Try the mountains nearby to the {0}!\"" +
                                     " they say."),
                             TextBox("People here seem a bit surprised that you" +
                                     " already have the Crystal of Courage," +
                                     " but they tell you the" +
                                     " next way to go anyway. \"Try the mountains nearby to the {0}!\"" +
                                     " they say.")],
         "DesertPalace"   : [TextBox("There doesn't seem to be much in the Desert Palace."),
                             TextBox("You have found the Desert Palace. After an" +
                                     " exciting adventure within, you defeat the" +
                                     " giant snake boss and recieve the Crystal" +
                                     " of Courage!"),
                             TextBox("You have found the Desert Palace despite not" +
                                     " knowing where you were going. After an" +
                                     " exciting adventure within, you defeat the" +
                                     " giant snake boss and recieve the Crystal" +
                                     " of Courage!")],
         "MountainTown"   : [TextBox("No one in Mountain Town has much to say."),
                             TextBox("The people of Mountain Town welcome you," +
                                     " and inform you the way to the next crystal" +
                                     " is through a nearby cave. However, you first" +
                                     " need to obtain the key from the nearby" +
                                     " village in the plains to the {0}."),
                             TextBox("Now that you have the key, you travel" +
                                     " through the tunnel to the other side of" +
                                     " the mountain range.")],
         "PlainsVillage"  : [TextBox("No one in Plains Village has much to say."),
                             TextBox("Since you are obviously the heroes of" +
                                     " this world, the people of Plains Village" +
                                     " give you the key to the tunnel with no" +
                                     " questions asked. Or maybe a mini-boss fight."),
                             TextBox("Though you should have no idea why you needed" +
                                     " it, you ask random strangers for a key to the" +
                                     " mountain pass until someone gives it to you.")],
         "MountainCave"   : [TextBox("The mountain cave passage takes you back to Mountain Town.")],
         "SnowyVillage"   : [TextBox("No one in Snowy Village has much to say."),
                             TextBox("People here help you stock back up in supplies" +
                                     " and mention that the Forest Village to the" +
                                     " {0} has a shrine to the Wisdom Crystal.")],
         "ForestVillage"  : [TextBox("No one in Forest Village has much to say."),
                             TextBox("The people working at the shrine come to" +
                                     " you in tears! Someone has stolen the crystal" +
                                     " and ran off to the Thief Hideout. No one knows" +
                                     " exactly where the Thief Hideout is, but it" +
                                     " has to be close."),
                             TextBox("The people at the shrine can't help much more," +
                                     " they suggest looking in the local forest for" +
                                     " the thief that took the Crystal of Wisdom.")],
         "ThiefHideout"   : [TextBox("No one in Thief Hideout has much to say."),
                             TextBox("You find the thief who stole the Crystal" +
                                     " of Wisdom here. After a brief timed chase" +
                                     " event, you catch the thief, and he hands over" +
                                     " the crystal. As you leave, he mutters something" +
                                     " about how you'll never find the ULTIMATE treasure."),
                             TextBox("There's someone who catches your eye. She" +
                                     " says that if you come back after you get" +
                                     " the last crystal, she'll give you a hint" +
                                     " as to the whereabouts of a legendary weapon."),
                             TextBox("{0} steps {1}, {2} steps {3}. Try looking there.")],
         "PortTown"       : [TextBox("No one in Port Town has much to say."),
                             TextBox("Now that you have the Crystal of Wisdom," +
                                     "someone here sells you a ship.")],
         "FishingTown"    : [TextBox("No one in Fishing Town has much to say."),
                             TextBox("Welcome to Fishing Town! A helpful NPC" +
                                     " points you {0} to find the last crystal:" +
                                     " the Crystal of Power!")],
         "LakeTemple"     : [TextBox("There's nothing left in the Lake Temple."),
                             TextBox("You've found the Lake Temple. After some" +
                                     " sliding puzzles and an aquatic-themed boss," +
                                     " you get the Crystal of Power! Time to beat" +
                                     " the game, unless you want to try and find the" +
                                     " hidden item...")],
         "FinalPalace"    : [TextBox("The barrier around the Final Palace keeps" +
                                     " you from getting close. You need all three" +
                                     " crystals to proceed into the final dungeon!"),
                             TextBox("The barrier is destroyed by the Crystals!" +
                                     " This is the final dungeon, there's no turning" +
                                     " back after this! If there's anything you still" +
                                     " want to search for- such as the secret" +
                                     " weapon- look for it now! Otherwise, search" +
                                     " this area once more to end the game."),
                             TextBox("You" +
                                     " enter the Final Palace and confront the Final" +
                                     " Boss. After a long fight, the Final Boss is" +
                                     " defeated! You win!\t" +
                                     "--------------------------------------------------\n" +
                                     "                 CONGRATULATIONS!                 \n" +
                                     "              THANK YOU FOR PLAYING               \n" +
                                     "            You got the NORMAL ending             \n" +
                                     "--------------------------------------------------\n"),
                             TextBox("You" +
                                     " enter the Final Palace and confront the Final" +
                                     " Boss. You've also found the secret weapon before" +
                                     " coming here, so you defeat the Final Boss with ease!" +
                                     " You win, and have gotten the 'TRUE ENDING', with" +
                                     " a bonus scene after the credits that hints at a" +
                                     " sequel.\t" +
                                     "--------------------------------------------------\n" +
                                     "                 CONGRATULATIONS!                 \n" +
                                     "              THANK YOU FOR PLAYING               \n" +
                                     "             You got the TRUE ending              \n" +
                                     "--------------------------------------------------\n")],
         "MasterSword"    : [None,
                             TextBox("Congratulations, you've found the Master" +
                                     " Sword! It's the only secret in the game," +
                                     " so you can stop looking now.")],
         "Inventory"      : [TextBox()]
      }
   
   
   def updateBox(self, titleId, index, text):
      if titleId in self.__boxes.keys() and index < len(self.__boxes.keys()):
         box = self.__boxes[titleId][index]
         self.__boxes[titleId][index].text = text
            
   def formatBox(self, titleId, index, *inp):
      if titleId in self.__boxes.keys() and index < len(self.__boxes.keys()):
         self.__boxes[titleId][index].text = self.__boxes[titleId][index].text.format(*inp)
   
   def getBox(self, tileId, playerInv=None):
      # retrieve text box by tileId and playerInv.
      
      ret = None
      i = 0
      if tileId in self.__boxes.keys():
         if playerInv:
            if tileId == "StarterTown":
               if not playerInv.private["starterVisit"]:
                  i = 1
               elif playerInv.cCourage and playerInv.cWisdom and playerInv.cPower:
                  if playerInv.mSword:
                     i = 3
                  else:
                     i = 2
            elif tileId == "DesertTown":
               if not playerInv.private["starterVisit"]:
                  playerInv.private["starterVisit"] = True
                  
               if playerInv.cCourage:
                  if not playerInv.private["desertVisit"]:
                     i = 3
                     playerInv.private["desertVisit"] = True
                     #playerInv.private["desertVisit2"] = True
                  if not playerInv.private["desertVisit2"]:
                     i = 2
                     #playerInv.private["desertVisit2"] = True
               elif not playerInv.private["desertVisit"]:
                  i = 1
#                  playerInv.private["desertVisit"] = True
               
            elif tileId == "DesertPalace":
               if not playerInv.private["desertVisit"]:
                  playerInv.private["desertVisit"] = True
                  
               if not playerInv.cCourage:
                  if playerInv.private["desertVisit"]:
                     i = 1
                  else:
                     i = 2
                  playerInv.cCourage = True
                  
            elif tileId == "MountainTown":
               if not playerInv.private["desertVisit2"]:
                  playerInv.private["desertVisit2"] = True
                  
               if playerInv.cCourage:
                  if not playerInv.tKey:
                     i = 1
                     playerInv.private["mountainVisit"] = True
                  else:
                     i = 2
                     #playerInv.private["desertVisit2"] = True
                     
            elif tileId == "PlainsVillage":
               if not playerInv.tKey and playerInv.cCourage:
                  if playerInv.private["mountainVisit"]:
                     i = 1
                  else:
                     i = 2
                     
                  playerInv.tKey = True
                  
            elif tileId == "SnowyVillage":
               if not playerInv.private["snowyVisit"]:
                  if playerInv.cWisdom:
                     playerInv.private["snowyVisit"] = True
                  else:
                     i = 1
                  #playerInv.private["snowyVisit"] = True
                  
            elif tileId == "ForestVillage":
               if not playerInv.private["snowyVisit"]:
                  playerInv.private["snowyVisit"] = True
                  
               if not playerInv.private["forestVisit"]:
                  if playerInv.cWisdom:
                     i = 0
                  else:
                     i = 1
                  #playerInv.private["forestVisit"] = True
               elif not playerInv.cWisdom:
                  i = 2
                  
            elif tileId == "ThiefHideout":
               if not playerInv.private["forestVisit"]:
                  playerInv.private["forestVisit"] = True
                  
               if not playerInv.cWisdom:
                  i = 1
                  playerInv.cWisdom = True
               elif not playerInv.private["thiefVisit"]:
                  i = 2
                  playerInv.private["thiefVisit"] = True
               elif playerInv.cWisdom and playerInv.cPower and \
                    playerInv.cCourage and not playerInv.mSword:
                  i = 3
                  
            elif tileId == "PortTown":
               if not playerInv.ship and playerInv.cWisdom:
                  i = 1
                  playerInv.ship = True
            
            elif tileId == "FishingTown":
               if not playerInv.private["fishingVisit"]:
                  i = 1
                  playerInv.private["fishingVisit"] = True
                  
            elif tileId == "LakeTemple":
               if not playerInv.cPower:
                  i = 1
                  playerInv.cPower = True
                  
            elif tileId == "FinalPalace":
               if playerInv.cPower and playerInv.cCourage and playerInv.cWisdom:
                  if not playerInv.private["finalVisit"]:
                     i = 1
                  else:
                     if playerInv.mSword:
                        i = 3
                     else:
                        i = 2
               
            elif tileId == "MasterSword":
               if not playerInv.mSword:
                  i = 1
                  playerInv.mSword = True
                  
         ret = self.__boxes[tileId][i]
      elif tileId != "None":
         print "unknown!", tileId
      
      if ret != None:
         ret.reset()
         
      return ret 

BOXES = TextBoxManager()