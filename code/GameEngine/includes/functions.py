CARDINALP = 0.1

def aligned(location):
   return (location[0] % 1 == 0 and location[1] % 1 == 0)

def debug(s):
   if DEBUG:
      out = ""
      for x in s:
         out += str(x) + ", "
      print out

def cardinal(loc1, loc2):
   # determine a cardinal direction
   dX = loc2[0] - loc1[0]
   dY = loc2[1] - loc1[1]
   
   if dX == 0:
      proportion = 0
   elif dY == 0:
      proportion = 1
   else:
      proportion = abs(float(dX) / float(dY))
      if proportion > 1:
         proportion = 1 / proportion
   
   
   if proportion < CARDINALP:
      if dY > 0:
         ret = "SOUTH"
      else:
         ret = "NORTH"
   elif proportion > 1.0 - CARDINALP:
      if dX > 0:
         ret = "EAST"
      else:
         ret = "WEST"
   else:
      if dY > 0:
         ret = "SOUTH"
      else:
         ret = "NORTH"
      
      if dX > 0:
         ret += "EAST"
      else:
         ret += "WEST"
   
   
   return ret

   
def longitude(loc1, loc2):
   # determine a cardinal direction
   dX = loc2[0] - loc1[0]
   if dX > 0:
      ret = "EAST"
   else:
      ret = "WEST"
   
   return ret, abs(dX)
      
def latitude(loc1, loc2):
   # determine a cardinal direction
   dY = loc2[1] - loc1[1]
   if dY > 0:
      ret = "SOUTH"
   else:
      ret = "NORTH"
   
   return ret, abs(dY)
