

class NQueens(object):
   def __init__(self, size):
      self.board = [[False for y in range(size)] for x in range(size)]
      self.size = size
      self.solutions = 0
      self.show = False
   
   def findSolutions(self):
      self.solutions = 0
      
      print "Finding queens..."
   
      self.setQueen(0)
      
      print "Total solutions:", self.solutions

      
   
   def setQueen(self, row):
      if row < self.size:
         # set queen
         for col in range(self.size):
            self.board[row][col] = True
            collision = self.backCheck(row-1,col,col-1,col+1)
            
            if not collision:
               self.setQueen(row+1)
            self.board[row][col] = False
      else:
         #solution found!
         self.solutions += 1
         if self.show:
            self.showBoard(self.solutions)
      
   def backCheck(self, row, vert, diag, off):
      ret = False
      if row >= 0:
         currRow = self.board[row]
         vCheck = currRow[vert]
         dCheck = False
         oCheck = False
         
         if diag >= 0 and diag < self.size:
            dCheck = currRow[diag]
         if off >= 0 and off < self.size:
            oCheck = currRow[off]
         
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
            if self.board[row][col]:
               s += "Q|"
            else:
               s += " |"
         print s
         
      self.makeRow()
      
      print ""
         
      
if __name__ == '__main__':
   nq = NQueens(10)
   
   nq.findSolutions()
   