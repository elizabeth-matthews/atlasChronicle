#Rule.py - Written by James Reinebold (www.reinebold.com)

import random

class RuleSystem:
    """
        Class responsible for parsing a control file and building an l-system.
        Takes the rules and start string and replaces the start string
        a given number of times.  When finished, store the result.
    """

    def __init__(self, filepath):
        """
            Open and parse the file found at the provided file path.
        """
        f = open(filepath)
        lines = f.readlines()
        f.close()
        rules = []
        ruleCount = 0
        numIterations = 0
        #string will contain the final l-system string
        self.string = ""
        #config will contain directions to the turtle on how to draw
        self.config = {}
        #parse control file
        for index, line in enumerate(lines):
            if line.startswith("START"):
                #what to start the l system with
                self.string = lines[index + 1].strip()
            elif line.startswith("N="):
                #how many iterations
                parts = line.split("=")
                numIterations = int(parts[1])
            elif line.startswith("NUM_RULES"):
                #how many rules
                ruleCount = int(lines[index + 1])
            elif line.startswith("RULES"):
                #a list of rules
                for i in xrange(ruleCount):
                    rules.append(lines[index + i + 1].strip())
            elif line.startswith("SYMBOL"):
                #symbol definitions
                parts = line.split("=")
                self.config[parts[1].strip()] = parts[2].strip()
        f.close()

        #building the string
        #run N iterations, replacing the string as we go
        #now has support for stochastic l-systems
        for i in xrange(numIterations):
            result = ""
            for char in self.string:
                replaced = False
                acceptable = [] #will contain (after, [start, end]) for dice roll
                for rule in rules:
                    parts = rule.split("=")
                    before = parts[0]
                    after = parts[2]
                    chance = parts[1]
                    chance = chance.replace("(","")
                    chance = chance.replace(")","")
                    subparts = chance.split(",")
                    chanceS = subparts[0]
                    chanceE = subparts[1]
                    if char == before:
                        acceptable.append((after, [float(chanceS), float(chanceE)]))
                roll = random.random()
                #if len(acceptable) > 1:
                #    print(len(acceptable))
                for rule in acceptable:
                    if roll >= rule[1][0] and roll <= rule[1][1]:
                        result += rule[0]
                        replaced = True
                        break
                if replaced == False:
                    result += char
            self.string = result
