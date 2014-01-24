prettyInv = {
   "ship"     : "  Ship                   ",
   "tKey"     : "Tunnel Key\n",
   "cWisdom"  : "  Crystal of Wisdom      ",
   "cCourage" : "Crystal of Courage\n",
   "cPower"   : "  Crystal of Power       ",
   "mSword"   : "Master Sword\n",
   "empty"    : "                        "
}

invOrder = ["ship", "tKey",
            "cWisdom", "cCourage",
            "cPower", "mSword"]


class Inventory(object):
   def __init__(self):
      self.cWisdom  = False
      self.cCourage = False
      self.cPower   = False
      self.mSword   = False
      self.tKey     = False
      self.ship     = False
      self.private  = {
         "starterVisit"  : False,
         "desertVisit"   : False,
         "desertVisit2"  : False,
         "mountainVisit" : False,
         "snowyVisit"    : False,
         "forestVisit"   : False,
         "thiefVisit"    : False,
         "fishingVisit"  : False,
         "finalVisit"    : False,
         "gameFinished"  : False
         }
   
   def __str__(self):
      s = "---------------------INVENTORY--------------------\n"
      for k in invOrder:
         if self.__dict__[k]:
            s += prettyInv[k]
         else:
            s += prettyInv["empty"]
            if k in ["tKey", "cCourage", "mSword"]:
               s+= "\n"
      
      return s
   

