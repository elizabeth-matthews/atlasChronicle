
import json

if __name__ == '__main__':
   
   
   inFile = open("../data/surveyRedone.json", 'r')
   
   inp = json.load(inFile)
   
   inFile.close()
   
   outFile = open("../data/surveyRedone2.json", 'w')
   
   json.dump(inp,outFile,indent=3,sort_keys=True)
   
   outFile.close()