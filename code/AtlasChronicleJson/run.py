from includes.atlas import AtlasChronicle

if __name__ == '__main__':
   # Testing of Atlas
   
   run = True
   inc = 0
   
   
   while run:
      ac = AtlasChronicle(inc)
      ac.run("../data/surveyJsonFinal.json")
      # that is all that should be needes
      del ac
      inc += 1
      
      run = raw_input("Run again (y/n)? ") in ['y','Y']