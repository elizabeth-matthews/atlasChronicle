import os
from math import *
from euclid import *

# imports for others??
from pygame.locals import *
import random

#TILETYPES = ["none", "void", "mountain", "water", "landfill"]
RESTRICTEDTYPES = ["void", "mountain", "water"]

TERRAINTYPES = ["void","mountain","water","grassland","forest","plains","snow","desert"]

SPACESCALE = 2
MAPSCALE = 2
SELECTDISTANCE = 2

SCALEF = 8
SCALEC = 4
SCALEW = 2
FRICTIONF = 0.90
FRICTIONC = 0.70
FRICTIONW = 0.50
MINVELF = 0.5
MINVELC = 1.0
MINVELW = 5.0

SPRINGFACTOR1 = 15.0
SPRINGFACTOR2 = 1

DEBUG = True

SEED = 1337

COLORS = {
    'loi' : (255, 255, 255), 'subObj': (150, 150, 150), 'void' : (255, 0, 255),

    'landfill' : (100, 200, 150), 'none'  : ( 10,  10,  10),
    'mountain' : (117,  26,  12), 'water' : (  0,  30, 100),
        
    'jointT' : (150, 150, 255), 'joint' : (255, 150, 150),
    'springT': (  0,   0, 100), 'spring': (100,   0,   0),
 
    'red'   : (255,   0,   0), 'green'  : (  0, 255,   0), 'blue': (  0,   0, 255),
    'black' : (  0,   0,   0), 'white'  : (255, 255, 255), 'gray': (128, 128, 128),
    'yellow': (255, 255,   0), 'magenta': (255,   0, 255), 'cyan': (  0, 255, 255),
    'graylt': (192, 192, 192), 'graydk' : ( 64,  64,  64),

    'NA': (0,0,0)
}


INFINITY = 100000

#### SIMPLE FUNCTIONS ####
def dist(pt1, pt2):
    dx = pt1[0] - pt2[0]
    dy = pt1[1] - pt2[1]

    d = dx**2 + dy**2

    return sqrt(d)
