from xml.dom.minidom import parse, parseString, Document, Node, Comment

class DimensionStats(object):
   def __init__(self):
      self.widthMin = -1
      self.widthMax = -1
      self.heightMin = -1
      self.heightMax = -1
      self.areaMin = -1
      self.areaMax = -1
      self.rigid = False
      self.aspect = "none"
   
   def __str__(self):
      s = "Dimension:\n"
      if (self.widthMin != -1 and self.widthMax != -1):
         s += "w " + str(self.widthMin) + "/" + str(self.widthMax) + "\n"
      if (self.heightMin != -1 and self.heightMax != -1):
         s += "h " + str(self.heightMin) + "/" + str(self.heightMax) + "\n"
      if (self.areaMin != -1 and self.areaMax != -1):
         s += "a " + str(self.areaMin) + "/" + str(self.areaMax) + "\n"
      s += "rigid " + str(self.rigid) + " aspect " + str(self.aspect) + "\n"
   
      return s
   
class ClimateStats(object):
   def __init__(self):
      self.temperature = -1.0
      self.humidity = -1.0
   
   def __str__(self):
      s = "Climate: "
      
      s += "t: " + str(self.temperature) + " h: " + str(self.humidity) + "\n"
      
      return s
      
class ColorStats(object):
   def __init__(self):
      self.r = 0.0
      self.g = 0.0
      self.b = 0.0
   
   def __str__(self):
      s = "Color: "
      
      s += "r: " + str(self.r) + " g: " + str(self.g) + " b: " + str(self.b) + "\n"
      
      return s

class TerrainStats(object):
   def __init__(self):
      self.name = "none"
      self.climate = ClimateStats()
      self.color = ColorStats()
   
   def __str__(self):
      s = "Terrain: " + str(self.name) + "\n"
      s += str(self.climate)
      s += str(self.color)
      
      return s

class PhysicalSeedStats(object):
   def __init__(self):
      self.A = []
      self.N = []
      self.S = []
      self.E = []
      self.W = []
      self.R = []
   
   def empty(self):
      return not(self.A or self.N or self.S or self.E or self.W or self.R)
   def __str__(self):
      s = ""
      if self.N or self.S or self.E or self.W or self.R:
         s += "Physical Seed Stats:\n"
         if self.N:
            s += "N: " + str(self.N[0]) + " "
         if self.S:
            s += "S: " + str(self.S[0]) + " "
         if self.E:
            s += "E: " + str(self.E[0]) + " "
         if self.W:
            s += "W: " + str(self.W[0]) + " "
         
         if self.R:
            s += "R: "
            for r in self.R:
               s += str(r) + " "
         s += "\n"
      return s

class WorldStats(object):
   def __init__(self):
      self.dimensions = DimensionStats()
      self.terrains = {}
      self.climate = ClimateStats()
   
   def __str__(self):
      s = "----World Stats----\n"
      s += str(self.dimensions)
      
      s += "--Terrains--\n"
      for t in self.terrains:
         s += str(t)
      
      s += "----\n"
      s += str(self.climate)
      
      return s
      
class ContinentStats(object):
   def __init__(self):
      self.dimensions = DimensionStats()
   
   def __str__(self):
      s = "----Continent Stats----\n"
      s += str(self.dimensions)
      return s

class FieldStats(object):
   def __init__(self):
      self.dimensions = DimensionStats()
   
   def __str__(self):
      s = "----Field Stats----\n"
      s += str(self.dimensions)
      return s
      
class RestrictionHolder(object):
   def __init__(self):
      self.key = None
      self.first = None
      self.second = None
      self.min = -1
      self.max = -1
      self.typed = True
      self.sections = 1
      
   def __str__(self):
      s = "Restriction: " + str(self.key) + "\n"
      
      s += str(self.first) + ", " + str(self.second) + "\n"
      s += "min: " + str(self.min) + ", max: " + str(self.max) + ", t: " + str(self.typed) + "\n"
      if self.sections > 1:
         s += "sections: " + str(self.sections) + "\n"
         
      return s

class WorldHolder(object):
   def __init__(self):
      self.stats = WorldStats()
      self.nodes = {}
      self.restrictions = {}
   
   def __str__(self):
      s = "World:\n"
      s += str(self.stats)
      s += "----Nodes----\n"
      for n in self.nodes:
         s += str(self.nodes[n])
      s += "----Restrictions----\n"
      for r in self.restrictions:
         s += str(self.restrictions[r])
      
      return s
      
class ContinentHolder(object):
   def __init__(self):
      self.key = ""
      self.stats = ContinentStats()
      self.nodes = {}
      self.restrictions = {}
   
   def __str__(self):
      s = "Continent: " + str(self.key) + "\n"
      s += str(self.stats)
      s += "----Nodes----\n"
      for n in self.nodes:
         s += str(self.nodes[n])
      s += "----Restrictions----\n"
      for r in self.restrictions:
         s += str(self.restrictions[r])
      
      return s
   
class FieldHolder(object):
   def __init__(self):
      self.key = ""
      self.stats = FieldStats()
      self.nodes = {}
      self.restrictions = {}
   
   def __str__(self):
      s = "Field: " + str(self.key) + "\n"
      s += str(self.stats)
      s += "----Nodes----\n"
      for n in self.nodes:
         s += str(self.nodes[n])
      s += "----Restrictions----\n"
      for r in self.restrictions:
         s += str(self.restrictions[r])
      
      return s

class LOIStats(object):
   def __init__(self):
      self.key = ""
      self.name = ""
      self.climate = ClimateStats()
      self.physicalSeeds = PhysicalSeedStats()
      self.terrain = None
   
   def __str__(self):
      s = "LOI: " + str(self.key) + " " + str(self.name) + "\n"
      if self.terrain:
         s += "terrain:" + str(self.terrain) + "\n"
      else:
         s += str(self.climate)
         s += str(self.physicalSeeds)
         
      return s
   
class XmlParser(object):
   def __init__(self):
      self.world = WorldHolder()
      self.poiCount = 0
      self.fieldCount = 0
      self.continentCount = 0
   
   def getInt(self, node):
      return int(node.childNodes[0].data)
      
   def getFloat(self, node):
      return float(node.childNodes[0].data)
      
   def getString(self, node):
      return str(node.childNodes[0].data)
      
   def getBool(self, node):
      return bool((node.childNodes[0].data).lower() == "true")
        
   def read(self, fileName):
      f = open(fileName)
      rawData = f.read()
      f.close()
      s = "".join([x.strip() for x in rawData.split("\n")])
      self.parsed = parseString(s)
      for node in self.parsed.childNodes:
         if node.nodeType != Comment.nodeType:
            self.readWorld(node)
         
      
   def readWorld(self, world):
      stats = [s for s in world.getElementsByTagName("statistics") if s in world.childNodes]
      if stats:
         stats = stats[0]
         
      nodes = [n for n in world.getElementsByTagName("nodes") if n in world.childNodes]
      if nodes:
         nodes = nodes[0].childNodes
         
      restrictions = [r for r in world.getElementsByTagName("restrictions") if r in world.childNodes]
      if restrictions:
         restrictions = restrictions[0].childNodes
      
      dimensions = stats.getElementsByTagName("dimensions")
      if dimensions:         
         self.world.stats.dimensions = self.readDimensions(dimensions[0])
      
      terrains = stats.getElementsByTagName("terrain-types")
      if terrains:
         terrains = terrains[0].childNodes
      
      for t in terrains:
         terr = TerrainStats()
         
         terr.name = self.getString(t.getElementsByTagName("name")[0])
         
         terr.climate = self.readClimate(t.getElementsByTagName("climate")[0])
         
         col = t.getElementsByTagName("color")[0]
         terr.color.r = self.getFloat(col.getElementsByTagName("red")[0])
         terr.color.g = self.getFloat(col.getElementsByTagName("green")[0])
         terr.color.b = self.getFloat(col.getElementsByTagName("blue")[0])
         
         self.world.stats.terrains[terr.name] = terr
      
      climate = stats.getElementsByTagName("climate") 
      if climate:
         self.world.stats.climate = self.readClimate(climate[0])
         
      for n in nodes:
         cont = self.readContinent(n)
         self.world.nodes[cont.key] = cont
      
   
      for r in restrictions:
         restrict = self.readRestriction(r)
         self.world.restrictions[restrict.key] = restrict
   
   def readContinent(self, cont):
      c = ContinentHolder()
      
      c.key = str(cont.attributes["key"].value)
      
      stats = [s for s in cont.getElementsByTagName("statistics") if s in cont.childNodes]
      if stats:
         stats = stats[0]
 
      nodes = [n for n in cont.getElementsByTagName("nodes") if n in cont.childNodes]
      if nodes:
         nodes = nodes[0].childNodes
      
      
      restrictions = [r for r in cont.getElementsByTagName("restrictions") if r in cont.childNodes]
      if restrictions:
         restrictions = restrictions[0].childNodes
         
         
      c.stats.dimensions = self.readDimensions(stats.getElementsByTagName("dimensions")[0])
      
      for n in nodes:
         field = self.readField(n)
         c.nodes[field.key] = field
         
      for r in restrictions:
         restrict = self.readRestriction(r)
         c.restrictions[restrict.key] = restrict
      
      return c
   
   
   def readField(self, field):
      f = FieldHolder()
      
      f.key = str(field.attributes["key"].value)
      
      stats = [s for s in field.getElementsByTagName("statistics") if s in field.childNodes]
      if stats:
         stats = stats[0]
 
      nodes = [n for n in field.getElementsByTagName("nodes") if n in field.childNodes]
      if nodes:
         nodes = nodes[0].childNodes
      
      restrictions = [r for r in field.getElementsByTagName("restrictions") if r in field.childNodes]
      if restrictions:
         restrictions = restrictions[0].childNodes
         
      f.stats.dimensions = self.readDimensions(stats.getElementsByTagName("dimensions")[0])
      
      for n in nodes:
         poi = self.readLOI(n)
         f.nodes[poi.key] = poi
      
      for r in restrictions:
         restrict = self.readRestriction(r)
         f.restrictions[restrict.key] = restrict
         
      
      return f

   def readLOI(self, poi):
      l = LOIStats()
      
      l.key = str(poi.attributes["key"].value)
      
      name = poi.getElementsByTagName("name")
      climate = poi.getElementsByTagName("climate")
      physicalSeeds = poi.getElementsByTagName("physical-seeds")
      terrain = poi.getElementsByTagName("terrain")
      
      if name:
         l.name = self.getString(name[0])
      
      if terrain:
         l.terrain = self.getString(terrain[0])
         if l.terrain in self.world.stats.terrains.keys():
            l.climate = self.world.stats.terrains[l.terrain].climate
            
      
      if climate:
         l.climate = self.readClimate(climate[0])
         
      if physicalSeeds:
         l.physicalSeeds = self.readPhysicalSeeds(physicalSeeds[0])
      
      return l
   
   def readClimate(self, climate):
      c = ClimateStats()
      
      c.temperature = self.getFloat(climate.getElementsByTagName("temperature")[0])
      c.humidity = self.getFloat(climate.getElementsByTagName("humidity")[0])
      
      return c
   
   def readPhysicalSeeds(self, pSeeds):
      ps = PhysicalSeedStats()
      
      a = pSeeds.getElementsByTagName("A")
      n = pSeeds.getElementsByTagName("N")
      s = pSeeds.getElementsByTagName("S")
      e = pSeeds.getElementsByTagName("E")
      w = pSeeds.getElementsByTagName("W")
      r = pSeeds.getElementsByTagName("R")
      
      if a:
         seed = self.getString(a[0])
         ps.A.append(seed)
      if n:
         seed = self.getString(n[0])
         ps.N.append(seed) 
      if s:
         seed = self.getString(s[0])
         ps.S.append(seed) 
      if e:
         seed = self.getString(e[0])
         ps.E.append(seed) 
      if w:
         seed = self.getString(w[0])
         ps.W.append(seed)
      if r:
         for rS in r:
            seed = self.getString(rS)
            ps.R.append(seed) 
      
      return ps
   
   def readRestriction(self, rest):
      r = RestrictionHolder()
      r.key = str(rest.attributes["key"].value)
      
      r.typed = self.getBool(rest.getElementsByTagName("typed")[0])
      
      r.first = self.getString(rest.getElementsByTagName("first")[0])
      r.second = self.getString(rest.getElementsByTagName("second")[0])
      dimensions = rest.getElementsByTagName("dimensions")[0]
      r.min = self.getInt(dimensions.getElementsByTagName("min")[0])
      r.max = self.getInt(dimensions.getElementsByTagName("max")[0])

      sections = rest.getElementsByTagName("sections")
      if sections:
         r.sections = self.getInt(sections[0])
         print r.sections
      
      return r
   
   
   def readDimensions(self, d):
      dimensions = DimensionStats()
      
      widths = d.getElementsByTagName("width")[0]
      heights = d.getElementsByTagName("height")[0]
      areas = d.getElementsByTagName("area")
      
      dimensions.widthMin = self.getInt(widths.getElementsByTagName("min")[0])
      dimensions.widthMax = self.getInt(widths.getElementsByTagName("max")[0])
      dimensions.heightMin = self.getInt(heights.getElementsByTagName("min")[0])
      dimensions.heightMax = self.getInt(heights.getElementsByTagName("max")[0])
      if areas:
         areas = areas[0]
         dimensions.areaMin = self.getInt(areas.getElementsByTagName("min")[0])
         dimensions.areaMax = self.getInt(areas.getElementsByTagName("min")[0])
      
      dimensions.rigid = (d.attributes['rigid'].value.lower() == "true")
      dimensions.aspect = str(d.attributes['aspect'].value)
   
      return dimensions
      

      
   def __str__(self):
      return str(self.world)
      
      
if __name__ == '__main__':
   xp = XmlParser()
   xp.read("data/worldDataFF6.xml")
   print xp
   