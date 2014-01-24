

applications   = [662,810,862,863,865,877]
computingF     = [828,838,839,840,940]
graphics       = [604,605,805,817,819]
interactive    = [611,614,831]
software       = [870,871,872,873,875]
systems        = [606,820,822,827,829,830,851,855]

class Course(object):
   def __init__(self, n, s, y, c=3):
      self.number   = n
      self.semester = s
      self.year     = y
      self.credits  = c
      
myCourses = [
   Course(838,'fall',2009),
   Course(881,'fall',2009, 2),
   Course(888,'fall',2009),
   Course(950,'fall',2009, 1),
   
   Course(681,'spring',2010),
   Course(840,'spring',2010),
   Course(888,'spring',2010),
   
   Course(870,'fall',2010),
   Course(888,'fall',2010),
   Course(950,'fall',2010),
   Course(991,'fall',2010),
   
   Course(605,'spring',2011),
   Course(827,'spring',2011),
   Course(950,'spring',2011,1),
   Course(991,'spring',2011),
   
   Course(805,'fall',2011),
   Course(873,'fall',2011),
   Course(950,'fall',2011,1),
   Course(991,'fall',2011),
   
   Course(809,'spring',2012),
   Course(881,'spring',2012),
   Course(950,'spring',2012,1),
   Course(991,'spring',2012),
   
   Course(991,'fall',2012,18)
   
]

def countApplicable():
   count = 0
   unapp = []
   for c in myCourses:
      if c.number in applications:
         count += 1
      elif c.number in computingF:
         count += 1
      elif c.number in graphics:
         count += 1
      elif c.number in interactive:
         count += 1
      elif c.number in software:
         count += 1
      elif c.number in systems:
         count += 1
      else:
         unapp.append(c.number)
         
   print unapp
   
   return count

if __name__ == '__main__':
   print "Number applicable:", countApplicable()