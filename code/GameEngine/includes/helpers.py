SCALE = 2

TILE_SIZE = 16 * SCALE
TRANSPARENT_COLOR = (0,255,255)

DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3

STILL = 0
MOVING = 1

DEBUG = False


locations = {
   "StarterTown"   : None, "DesertTown"    : None,
   "DesertPalace"  : None, "MountainTown"  : None,
   "PlainsVillage" : None, "MountainCave"  : None,
   "SnowyVillage"  : None, "ForestVillage" : None,
   "ThiefHideout"  : None, "PortTown"      : None,
   "FishingTown"   : None, "LakeTemple"    : None,
   "FinalPalace"   : None, "MasterSword"   : None
}

locTiles = {
   "StarterTown"   : "grassA",  "DesertTown"    : "desertB",
   "DesertPalace"  : "desertC", "MountainTown"  : "grassB",
   "PlainsVillage" : "plainsD", "MountainCave"  : "snowA",
   "SnowyVillage"  : "snowB",   "ForestVillage" : "forestA",
   "ThiefHideout"  : "forestD", "PortTown"      : "grassB",
   "FishingTown"   : "grassA",  "LakeTemple"    : "grassC",
   "FinalPalace"   : "forestC", "MasterSword"   : "forest"
}
