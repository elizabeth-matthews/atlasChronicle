import pygame
import pymunk
from pygame.locals import *
from ..helpers.defines import *
import random
import time
import math

class SpaceObj(object):
   def __init__(self, name, width = 0, height = 0, oType = 'loi'):
        
      self.name = name
      self.type = oType
         
      if width == 0 or height == 0:
         mass       = 1
         radius     = 0.5
         inertia    = pymunk.moment_for_circle(mass, 0, radius)
         self.body  = pymunk.Body(mass, inertia)
         self.shape = pymunk.Circle(self.body, radius)
            
         self.dim   = (1,1)
      else:
         mass       = 1
         radius     = 0.5
         inertia   = pymunk.moment_for_box(mass, width, height)
         self.body  = pymunk.Body(mass, inertia)
         verts = [(-width/2,-height/2), (width/2,-height/2),
                   (width/2, height/2), (-width/2,height/2)]
         self.shape = pymunk.Poly(self.body,verts)
         self.shape.friction = 0.01
         self.shape.elasticity = 0.0
            
         self.dim   = (width,height)
         
    
   def draw(self, canvas, scale):
      pos = self.body.position
      
      color = COLORS[self.type]

      p = (int(pos[0] * scale), int(pos[1] * scale))
      
      if self.dim != (1,1):
         
         verts = [(x * scale) + p for x in self.shape.verts]
         
         pygame.draw.polygon(canvas, COLORS[self.type], verts)
      else:
         d = (max(2,self.dim[0] * scale), max(2,self.dim[1] * scale))
         rec = pygame.Rect(p, d)
      
         pygame.draw.rect(canvas, COLORS[self.type], rec)


class SpaceSubObj(object):
   def __init__(self, name):
        
      self.name = name
         
      mass       = 1
      radius     = 0.5
      inertia    = pymunk.moment_for_circle(mass, 0, radius)
      self.body  = pymunk.Body(mass, inertia)
      self.shape = pymunk.Circle(self.body, radius)
         
      self.dim   = (1,1)
         
    
   def draw(self, canvas, scale):
      pos = self.body.position
      
      color = COLORS["subObj"]

      p = (int(pos[0] * scale), int(pos[1] * scale))
      
      d = (max(2,self.dim[0] * scale), max(2,self.dim[1] * scale))
      rec = pygame.Rect(p, d)
   
      pygame.draw.rect(canvas, COLORS[self.type], rec)
        
        

# Should not be created by anything other than SlideSpring
class SlideJoint(object):
   def __init__(self, object1, object2, minLen, maxLen, 
                typed = True,
                center1 = (0,0), center2 = (0,0)):
      self.objects    = (object1, object2)
      self.dimensions = (minLen, maxLen)
      self.typed      = typed
      self.slide = pymunk.SlideJoint(object1.body, object2.body,
                                     center1, center2, minLen, maxLen)

   def draw(self, canvas, scale):
      body1 = self.objects[0].body
      body2 = self.objects[1].body
      p1 = body1.position * scale
      p1[0] += float(scale) * .5
      p1[1] += float(scale) * .5
      p2 = body2.position * scale
      p2[0] += float(scale) * .5
      p2[1] += float(scale) * .5
      
      color = COLORS['joint']
      if self.typed:
         color = COLORS['jointT']

      pygame.draw.line(canvas, color, p1, p2)
   
   def get(self):
      return self.slide
        
        
# Should not be created by anything other than SlideSpring
class Spring(object):
   def __init__(self, object1, object2, length, typed = True,
                center1 = (0,0), center2 = (0,0)):
       
      self.objects = (object1, object2)
      self.length  = length
      self.typed   = typed
      self.centers = (center1, center2)
      
      self.spring = pymunk.DampedSpring(object1.body, object2.body,
                                        center1, center2, length,
                                        SPRINGFACTOR1, SPRINGFACTOR2)
      
   
   def draw(self, canvas, scale):
      body1 = self.objects[0].body
      body2 = self.objects[1].body
      p1 = body1.position * scale
      p2 = body2.position * scale
      
      p1[0] += float(scale) * .5
      p1[1] += float(scale) * .5
      p2[0] += float(scale) * .5
      p2[1] += float(scale) * .5
      
      color = COLORS['spring']
      if self.typed:
         color = COLORS['springT']

      pygame.draw.line(canvas, color, p1, p2)
       
   def get(self):
      return self.spring


# Used to represent restrictions
class SlideSpring(object):
   def __init__(self, object1, object2, minLen, maxLen,
                typed = True,
                center1 = (0,0), center2 = (0,0)):
   
      self.objects = (object1, object2)
      self.typed   = typed
      self.centers = (center1, center2)
      self.minLength = minLen
      self.maxLength = maxLen
      
      self.smallSpring = Spring(object1, object2, minLen, typed,
                                center1, center2)
      self.largeSpring = Spring(object1, object2, maxLen, typed,
                                center1, center2)
      self.midSlide    = SlideJoint(object1, object2, minLen, maxLen,
                                    typed, center1, center2)
      
      self.active = "mid"
      self.update()
      self.changed = False
   
   def update(self):
      # updates active state and returns current length
      pos1 = self.objects[0].body.position
      pos2 = self.objects[1].body.position
      currLen = dist(pos1, pos2)
      
      if currLen < self.minLength:
         if self.active != "small":
            self.changed = True
            self.prev = self.active
         self.active = "small"
      elif currLen > self.maxLength:
         if self.active != "large":
            self.changed = True
            self.prev = self.active
         self.active = "large"
      else:
         if self.active != "mid":
            self.changed = True
            self.prev = self.active
         self.active = "mid"
          
   
   def draw(self, canvas, scale):
      if self.active == "small":
         self.smallSpring.draw(canvas, scale)
      elif self.active == "mid":
         self.midSlide.draw(canvas, scale)
      elif self.active == "large":
         self.largeSpring.draw(canvas, scale)
   
   def get(self):
       
      if self.active == "small":
         ret = self.smallSpring.get()
      elif self.active == "mid":
         ret = self.midSlide.get()
      elif self.active == "large":
         ret = self.largeSpring.get()
           
       
      if self.changed:
         if self.prev == "small":
            prev = self.smallSpring.get()
         elif self.prev == "mid":
            prev = self.midSlide.get()
         elif self.prev == "large":
            prev = self.largeSpring.get()
      else:
         prev = None
       
      self.changed = False
       
      return ret, prev
       


class SpaceManager(object):
   def __init__(self, key, animate=True, pause=False):
      self.x = -1
      self.y = -1
      self.key = key
      
      self.canvas = None
      
      self.animate = animate
      self.pause = pause
      
      self.done = False
      self.selected = None
      
      self.clock         = pygame.time.Clock()
      self.space         = pymunk.Space()
      self.simStep       = 50
      self.friction      = 0.90
      self.minVelocity   = 0.2
      self.space.gravity = (0,0)
      self.spaceScale = SPACESCALE
      
      self.objects    = {}
      self.subObjects = {}
      self.sSprings   = {}
      
      self.state = "simulate"
      
      self.offset = None
   
   def save(self):
      return "Space"
   
   def getCanvas(self):
      return self.canvas
   
   def setUpdatedSize(self):
      # dummy for ease
      return
   
   def getUpdatedSize(self):
      return False
   
   def isDone(self):
      return self.done
   
   def setSize(self, x, y):
      self.x = x
      self.y = y
      self.canvasSize = (self.x * self.spaceScale, self.y * self.spaceScale)
      self.canvas = pygame.Surface(self.canvasSize)
  
   def draw(self):
      self.canvas.fill(COLORS["graydk"])
        
      for obj in self.objects:
         self.objects[obj].draw(self.canvas, self.spaceScale)
         
      for subObj in self.subObjects:
         self.subjObjects[subObj].draw(self.canvas, self.spaceScale)
         
      for ss in self.sSprings:
         self.sSprings[ss].draw(self.canvas, self.spaceScale)
   
   def simulate(self):
      for ss in self.sSprings:
         self.sSprings[ss].update()
         if self.sSprings[ss].changed:
            add,rem = self.sSprings[ss].get()
            self.space.remove(rem)
            self.space.add(add)
            
      self.space.step(1/float(self.simStep))
      self.clock.tick(self.simStep)
      
      minX = INFINITY
      minY = INFINITY
      maxX = 0
      maxY = 0
      
      self.done = True
      
      for obj in self.objects:
         
         body = self.objects[obj].body
         
         # rotation fix
         body.angle = 0
         body.angular_velocity = 0
         
         pos = body.position
         vel = body.velocity
         dims = self.objects[obj].dim
         
         if dims == (1,1):
            halfX = 0
            halfY = 0
         else:
            halfX = dims[0] / 2
            halfY = dims[1] / 2
          
         # Adjust location
         if minX > pos[0] - halfX:
            minX = pos[0] - halfX
         if minY > pos[1] - halfY:
            minY = pos[1] - halfY
         if maxX < pos[0] + halfX:
            maxX = pos[0]-1 + halfX
         if maxY < pos[1] + halfY:
            maxY = pos[1]-1 + halfY
              
         if pos[0] < halfX:
            pos[0] = halfX
         elif pos[0] > self.x - halfX:
            pos[0] = self.x - halfX - 1
          
         if pos[1] < halfY:
            pos[1] = halfY
         elif pos[1] > self.y - halfY:
            pos[1] = self.y - halfY - 1
         
         body.position = pos
      
         # apply friction
         if body.velocity.x < self.minVelocity and \
            body.velocity.y < self.minVelocity:
            body.velocity = 0,0
         else:
            body.velocity *= self.friction
          

         # Check for settled
         if abs(vel[0]) > self.minVelocity or abs(vel[1]) > self.minVelocity:
            self.done = False
      

      # This must be separate from the other update
          
      w = maxX - minX
      h = maxY - minY

      halfW = w / 2.0
      halfH = h / 2.0
      
      # Center every object
      for obj in self.objects:
         pos = self.objects[obj].body.position
         if len(self.objects) == 1:
            pos[0] = self.x / 2.0
            pos[1] = self.y / 2.0
            
         else:
            pos[0] = pos[0] - minX - halfW + (self.x / 2.0)
            pos[1] = pos[1] - minY - halfH + (self.y / 2.0)
 
   def update(self):
      if self.state == "simulate":
         self.simulate()
      elif self.state == "manual" and self.selected:
         
         loc = pygame.mouse.get_pos()
         loc = (float(loc[0] - self.offset[0]) / float(self.spaceScale),
                float(loc[1] - self.offset[1]) / float(self.spaceScale))
         self.objects[self.selected].body.position = loc  
   
   def handleEvent(self, e, offset=None):
      
      if e.type == KEYDOWN:
         if e.key == K_RETURN and self.state == "simulate":
            self.randomize()
         elif e.key == K_1:
            self.state = "paused"
            if DEBUG:
               print "Space State is PAUSED"
         elif e.key == K_2:
            self.state = "manual"
            self.done = False
            if DEBUG:
               print "Space State is MANUAL"
         elif e.key == K_3:
            self.state = "identify"
            if DEBUG:
               print "Space State is IDENTIFY"
         elif e.key == K_4:
            self.state = "simulate"
            if DEBUG:
               print "Space State is SIMULATE"
               
      elif e.type == MOUSEBUTTONDOWN:
         if self.state == "identify" or self.state == "manual":
            self.offset = offset
            loc = pygame.mouse.get_pos()
            loc = (float(loc[0] - offset[0]) / float(self.spaceScale),
                   float(loc[1] - offset[1]) / float(self.spaceScale))
            
            self.selected = None
            
            for obj in self.objects:
               distance = dist(loc, self.objects[obj].body.position)
               if distance < SELECTDISTANCE:
                  self.selected = obj
                  break
            
            
            if self.selected:
               print self.objects[self.selected].name
            
      elif e.type == MOUSEBUTTONUP:   
         self.selected = None

   def randomize(self):
      for obj in self.objects:
         x = random.randrange(0, self.x)
         y = random.randrange(0, self.y)
         self.objects[obj].body.position = x, y
         
      self.done = False

   def addObject(self, key, name, width = 0, height = 0):
      obj = SpaceObj(name, width, height)
        
      x = random.randrange(0, self.x)
      y = random.randrange(0, self.y)
      
        
      obj.body.position = x, y
      self.space.add(obj.body, obj.shape)
      self.objects[key] = obj
   
   def addSSpring(self, key, first, second, dim, typed=True):
        
      ss = SlideSpring(self.objects[first], self.objects[second],
                        dim[0], dim[1], typed)
      s, trash, = ss.get()
        
      # Force the initial addition, rest is handled in update.
      self.space.add(s)
      self.sSprings[key] = ss
    
   def findObject(self, key):
      # find the key object's location
        
      obj = self.objects[key]
        
      return obj.body.position

   #def reset(self):
   #   # reset, remove all objects.
   #   