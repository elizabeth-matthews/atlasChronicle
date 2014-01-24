from includes.gameEngine import GameEngine
import sys


if __name__ == '__main__':
   
   #use: python run.py ['a' or 'b']
   # leaving out 'a' and 'b' runs the test once
   
   runsize = (640,480)
   # Check size on lab computers?
   
   if len(sys.argv) == 2:
      ### SURVEY ###
      
      if sys.argv[1] in ['a','A']:
         mapOrder = [0,0,0,0,0,0] #[0,0,0,1,2,3]
      else:
         mapOrder = [0,1,2,3,4,5] #[1,2,3,0,0,0]
   
      
      raw_input("Please make sure you've finished pages 1 and 2, then press enter.\n>")
      
      for m in range(len(mapOrder)):
         r = "r"
         while r != "":
            g = GameEngine("maps/surveyMap" + str(mapOrder[m]) + ".json", runsize)
            g.run()
            del g
            r = raw_input("Press enter for next game>")
            #r = raw_input("If you accidentially quit the game, type r and press enter.\n" + \
            #              "Otherwise, please fill out question number " + str(m + 4) + ", then press enter.\n" + \
            #              ">")
         
         
      
      raw_input("Please fill out the last page of the survey, then press enter.\n>")
      
      
   
   elif len(sys.argv) == 1:
      ### TESTING ###
      
      g = GameEngine("maps/surveyMap5.json", runsize)
      g.run()
      del g
   
   else:
      print "Use: python run.py [a/b]"