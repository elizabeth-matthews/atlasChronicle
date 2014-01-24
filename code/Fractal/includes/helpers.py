
from math import cos, sin, log, cosh, sinh
from math import acos, asin, tanh, tan, acosh, asinh, exp, sqrt, atan

class functionInfo(object):
   def __init__(self,zf=None, cf=None,
                zi="xy", ci=complex(-.7,.27015),
                r=(3.0,3.0), s=(-1.5,-1.5), l=2.0):
      self.zF = zf
      self.cF = cf
      self.zInit = zi
      self.cInit = ci
      self.range = r
      self.start = s
      self.limit = l

def complexF(c,f):
   return complex(f(c.real), f(c.imag))

def juliaFunc(z,c):
   return z * z + c

def randomZ(z,c):
   return complexF(z, sin) + z
def randomC(z,c):
   return complexF(c, tanh) * c * c + z


FUNCTIONS = {
   "julia"  : functionInfo(juliaFunc),
   "mandel" : functionInfo(juliaFunc,None,
                           complex(0),"xy",
                           (2.0,2.0),(-1.5,-1.0)),
   "random" : functionInfo(randomZ, randomC,
                           "xy","xy")
}
