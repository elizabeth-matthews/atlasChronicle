#PyFlora - Written by James Reinebold (www.reinebold.com)
#An l-system tool for rendering virtual plants.
#Based on the text Algorithmic Beauty of Plants
#See Redame.rtf for more details!

#imports
import pygame
import math
import sys
import os

from Turtle import Turtle
from Rule import RuleSystem

#constants
WIDTH = 800
HEIGHT = 600
running = True
BACKGROUND_COLOR = (33, 128, 184) #sky blue

#init pygame
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
clock = pygame.time.Clock()

def setupSimulation(turtles):
    """
        Create a little demo with six different types of flora.
    """
    #create rule systems - how the l-systme should operate
    fernRS = RuleSystem("examples" + os.sep + "fern.txt")
    bushRS = RuleSystem("examples" + os.sep + "bush.txt")
    treeRS = RuleSystem("examples" + os.sep + "tree.txt")
    fern2RS = RuleSystem("examples" + os.sep + "fern2.txt")
    typebRS = RuleSystem("examples" + os.sep + "typeb.txt")
    #create the turtles - flora drawing systems
    donatello = Turtle(fernRS, 150, 600, 90, False)
    leonardo = Turtle(fern2RS, 50, 600, 90, False)
    michaelangelo = Turtle(bushRS, 650, 600, 90, False)
    raphael = Turtle(treeRS, 350, 600, 90, False)
    bob = Turtle(typebRS, 450, 600, 90, False)
    #the stochastic plants will also blow in the wind
    for i in xrange(11):
        stoc = Turtle(RuleSystem("examples" + os.sep + "stochasticVine.txt"), i * 60, 600, 90, True)
        turtles.append(stoc)
    #append the turtles to the big list for animating/drawing
    turtles.append(donatello)
    turtles.append(leonardo)
    turtles.append(michaelangelo)
    turtles.append(raphael)
    turtles.append(bob)


def draw(actors):
    """
        Tell the turtles to draw.
    """
    display.fill(BACKGROUND_COLOR)
    pygame.draw.line(display, [0, 100, 0], [0, 596], [800, 596], 10)
    #do all tree drawing here
    for actor in actors:
        actor.draw(display)
    pygame.display.flip()

def handleEvents():
    """
        Listen to see if the user wants to quit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

def update(deltaT, actors):
    """
        Update the timestep for the growth animations.
        Also set the wind to be blowing from the left to right at strength 3.0
    """
    for actor in actors:
        #blow
        actor.setWind(3.0)
        #grow
        actor.grownPercentage = min(actor.grownPercentage + 0.005, 1.0)
        #animate
        actor.update(deltaT)


if __name__ == "__main__":
    #run script
    turtles = []
    setupSimulation(turtles)
    #gameloop
    while running:
        #FPS = 50
        elapsed = clock.tick(50)
        handleEvents()
        update(elapsed, turtles)
        draw(turtles)
            
