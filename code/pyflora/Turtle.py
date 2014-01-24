#Turtle.py - Written by James Reinebold (www.reinebold.com)



#imports
import math
import pygame
import random

#constants
DEGREES2RADIANS = 0.01745

class Branch:
    """
        One part of the plant.
        Has children so it can be animated properly in the wind.
    """

    def __init__(self, myStart, myEnd, myLength, angleDrawn, windOffset):
        self.start = myStart
        self.end = myEnd
        self.children = []
        self.canMove = 5
        self.hasMoved = 0
        self.length = myLength
        self.angle = angleDrawn
        self.windOffset = windOffset

class Fruit:
    """
        Class not implemented yet.  TODO!
    """

    def __init__(self, myStart, myColor, myRadius):
        """
            Class not implemented yet.  TODO!
        """
        self.start = myStart
        self.radius = myRadius
        self.color = myColor

class Turtle:
    """
        Turtle drawing class for Pygame.
        Renders the l-system string by parsing it as a series of commands.
        All drawing is done from the perspective of the turtle.
        See http://en.wikipedia.org/wiki/L-system for more information.
    """

    def __init__(self, rules, myX, myY, myAngle, isDynamic):
        """
            Create a new turtle.

            Rules - must contain a control string
            Rules - must contain a dictionary that explains how to draw:
            The config dictionary is a lookup table where the keys are the characters
            and the values are turtle drawing commands (see pyflora documentation).
           
            myX - initial x position on screen for turtle
            myY - initial y position on screen for turtle
            myAngle - initial degree facing for turtle (90 is up)
            isDynamic = whether or not this turtle will blow in the wind


            Only up to a certain percentage of the branches will be drawn.
            Only up to a certain percentage of the grown branches are green (rest are brown).
            Build the entire tree and have it sway in the wind in the constructor.
        """
        self.string = rules.string
        self.x = myX
        self.y = myY
        self.startX = self.x
        self.startY = self.y
        self.watered = False
        self.angle = myAngle
        self.stack = []
        self.config = rules.config
        self.current = 0
        self.doneLines = []
        self.healthyColor = [0, 100, 0]
        self.badColor = [139, 69, 19]
        self.lineCount = 0
        self.waterLevel = 1.0
        self.waterCounter = 100
        self.bad = 0
        self.wind = 0
        self.root = None
        self.currentBranch = None
        self.grownPercentage = 0.0
        self.totalLength = 0.0
        self.turbulenceCounter = 100
        self.angleOffset = 0
        self.turbulence = 0
        self.turboV = 0
        self.currentLineCount = 0
        self.dynamic = isDynamic
        self.buildTree()


    def buildTree(self):
        """
            Parse the string and build the complete l-system
        """
        self.root = None
        self.currentBranch = None
        self.doneLines = []
        self.current = 0
        self.stack = []
        self.x = self.startX
        self.y = self.startY
        self.lineCount = 0
        self.totalLength = 0.0
        while self.current < len(self.string):
            char = self.string[self.current]
            action = self.config[char]
            change = self.handleAction(action)
            self.current += 1

    def setWind(self, vx):
        """
            Set the wind to be some turbulence + the value supplied.
        """
        self.turbulence += self.turboV
        if self.turbulence > 1.0:
            self.turbulence = 1.0
        elif self.turbulence < -1.0:
            self.turbulence = -1.0
        self.wind = vx + self.turbulence
        self.angleOffset = self.wind * -10.0
        self.angle = (self.wind * -10.0) + 90.0

    def update(self, dt):
        """
            Update the logic for the tree.
        """
        #change turbulence wind velocity every so often.
        self.turbulenceCounter -= dt
        if self.turbulenceCounter <= 0:
            self.turbulenceCounter = random.randint(500, 1000)
            self.turboV = (random.random() - 0.5) / 10.00
        #make all the branches sway in the wind correspondingly to their parents, starting from root
        if self.root != None and self.dynamic:
            self.adjustChildrenForWind(self.root)
        #clear the watered bit to be set/not set next frame
        self.watered = False

    def adjustChildrenForWind(self, node):
        """
            Recursive method for making the supplied node and all of its children sway in the wind.
        """
        #adjust starting ending position for line segment based on wind
        newO = self.angleOffset - node.windOffset
        node.angle += newO
        node.windOffset = self.angleOffset
        node.end[0] = node.start[0] + math.cos(node.angle * DEGREES2RADIANS) * node.length
        node.end[1] = node.start[1] + math.sin(node.angle * DEGREES2RADIANS) * -1 * node.length
        #start where parent ends
        for child in node.children:
            child.start = node.end
            self.adjustChildrenForWind(child)
        
            

    def draw(self, display):
        """
            Draw to the screen based on the grown percentage and the healty/not healthy percentages
        """
        #water of 0.9 means 90% of the lines are healthy colored
        #so color i=0:bad as green
        toDraw = self.grownPercentage * self.totalLength
        toDrawGreen = toDraw * self.waterLevel
        drawingGreen = True
        for i in xrange(self.lineCount):
            active = self.doneLines[i]
            disp = active.length
            
            if toDrawGreen <= 0:
                drawingGreen = False
            if drawingGreen:
                #healthy green
                pygame.draw.aaline(display, self.healthyColor, active.start, active.end)
            else:
                #not healthy
                pygame.draw.aaline(display, self.badColor, active.start, active.end)
            if disp > toDraw:
                disp = toDraw
            #we have drawn a line, so subtract that from what we have left to do
            toDraw -= disp
            toDrawGreen -= disp
            if toDraw <= 0:
                #once we have nothing left to draw, break from the loop
                break
            
    def handleAction(self, action):
        """
            Handle one character of the string.  See pyflora documentation for details.
        """
        if action.startswith("PUSH"):
            #push to the stack
            self.stack.append((self.currentBranch, self.angle))
            return True
        elif action.startswith("POP"):
            #pop from the stack
            data = self.stack.pop()
            self.currentBranch = data[0]
            self.x = self.currentBranch.end[0]
            self.y = self.currentBranch.end[1]
            #self.x = data[0].end[0]
            #self.y = data[0].end[1]
            self.angle = data[1]
            return True
        elif action.startswith("NULL"):
            #do nothing
            return True
        elif action.startswith("TURN"):
            #turn the facing of the turtle
            parts = action.split()
            otherAngle = float(parts[1])
            self.angle += otherAngle
            return True
        elif action.startswith("CIRCLE"):
            parts = action.split()
            color = parts[1]
            radius = parts[2]
        elif action.startswith("DRAW"):
            #draw straight along the direction the turtle is facing
            #keep track of heirarchy of tree
            parts = action.split()
            distance = float(parts[1])
            compX = math.cos(self.angle * DEGREES2RADIANS) * distance
            compY = math.sin(self.angle * DEGREES2RADIANS) * -1.0 * distance
            newX = compX + self.x
            newY = compY + self.y
            b = Branch([self.x, self.y], [newX, newY], distance, self.angle, self.angleOffset)
            self.totalLength += b.length
            self.doneLines.append(b)
            if self.root == None:
                self.root = b
            else:
                self.currentBranch.children.append(b)
            self.currentBranch = b
            self.x = newX
            self.y = newY
            self.lineCount += 1
