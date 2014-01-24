#!/usr/bin/env python

import sys
import xml.dom.minidom

class GameConstants(object):
  def __init__(self, configFileName):
    f = open(configFileName)
    doc = xml.dom.minidom.parse(f)
  
    self.screenWidth = int(doc.getElementsByTagName('screenWidth')[0].firstChild.nodeValue)
    self.screenHeight = int(doc.getElementsByTagName('screenHeight')[0].firstChild.nodeValue)
    self.numberOrbs = int(doc.getElementsByTagName('numberOrbs')[0].firstChild.nodeValue)


if __name__ == '__main__':
  gc = GameConstants('xmlData/game.xml')
  print 'Screen Width:   ', gc.screenWidth
  print 'Screen Height:  ', gc.screenHeight
  print 'Number of Orbs: ', gc.numberOrbs
