from math import ceil
from copy import deepcopy

class NQueens(object):
   def __init__(self, size):
      self.board = [0 for x in range(size)]
      self.size = size
      self.solutions = 0
      self.solutionBoards = []
      self.show = False
      self.unique = False
   
   def checkDuplicate(self):
      unique = True
      
      r1 = self.rotate(self.board)
      unique = not r1 in self.solutionBoards
      
      if unique:
         r2 = self.rotate(r1)
         unique = not r2 in self.solutionBoards
      
         if unique:
            r3 = self.rotate(r2)
            unique = not r3 in self.solutionBoards
            
            if unique:
               
               m = self.mirror(self.board)
               unique = not m in self.solutionBoards
               
               if unique:
                  m1 = self.rotate(m)
                  unique = not m1 in self.solutionBoards
                  
                  if unique:
                     m2 = self.rotate(m1)
                     unique = not m2 in self.solutionBoards
                     
                     if unique:
                        m3 = self.rotate(m2)
                        unique = not m3 in self.solutionBoards
     
      return unique
      
   
   def rotate(self, board):
      nb = [0 for x in range(self.size)]
      for row in range(self.size):
         nr = board[row]
         nc = self.size - row - 1
         nb[nr] = nc
      
      #self.showUnique(nb)
      
      return nb

   def mirror(self, board):
      nb = [0 for x in range(self.size)]
      for row in range(self.size):
         nc = self.size - board[row] - 1
         nb[row] = nc
      
      return nb
      
   
   def findSolutions(self):
      self.solutions = 0
      
      print "Finding queens..."
   
      self.setQueen(0)
      
      print "Total solutions:", self.solutions

      
   
   def setQueen(self, row):
      if row < self.size:
         # set queen
         cSize = self.size 
         if row == 0:
            cSize = int(ceil(cSize / 2.0))
         for col in range(cSize):
            self.board[row] = col
            collision = self.backCheck(row-1,col,col-1,col+1)
            
            if not collision:
               self.setQueen(row+1)
      else:
         #solution found!
         if not self.unique or self.checkDuplicate():
            self.solutions += 1
            self.solutionBoards.append(deepcopy(self.board))
            if self.show:
               self.showBoard(self.solutions)
      
   def backCheck(self, row, vert, diag, off):
      ret = False
      if row >= 0:
         currRow = self.board[row]
         vCheck = currRow == vert
         dCheck = False
         oCheck = False
         
         if diag >= 0 and diag < self.size:
            dCheck = currRow == diag
         if off >= 0 and off < self.size:
            oCheck = currRow == off
         
         ret = vCheck or dCheck or oCheck
         if not ret:
            ret = ret or self.backCheck(row-1, vert, diag-1, off+1)
         
      return ret
      
      
   
   def makeRow(self):
      s = "+"
      for y in range(self.size):
         s += "-+"
      print s
      
   
   def showBoard(self, solNum):
      print "Solution Number:", solNum
      for row in range(self.size):
         self.makeRow()
         
         s = "|"
         for col in range(self.size):
            if self.board[row] == col:
               s += "Q|"
            else:
               s += " |"
         print s
         
      self.makeRow()
      
      print ""

   def showUnique(self, board):
      for row in range(self.size):
         self.makeRow()
         
         s = "|"
         for col in range(self.size):
            if board[row] == col:
               s += "Q|"
            else:
               s += " |"
         print s
         
      self.makeRow()
      
      print ""
         
      
if __name__ == '__main__':
   s = int(raw_input("Enter num>"))
   nq = NQueens(s)
   nq.show = True
   
   nq.findSolutions()
   