# view.py
#
# The interface for the user interface and data storage method

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *

import groogle
import node
import link
import analyzer


import math
import time
import pdb

class GroogleView(QtGui.QWidget):
    
    def __init__(self):
        super(GroogleView, self).__init__()
        self.NODES_PER_LEVEL = 4
        self.NODE_MAGNITUDE = 200

        self.SCENE_HEIGHT = 600
        self.SCENE_WIDTH = 900
    
        self.mScene =  QGraphicsScene(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT)
        self.mView = QGraphicsView(self.mScene)
        self.mNodes = []
        self.mLinks = []
        self.initUI()        

    def initUI(self):      
        adjust = 200
        self.setGeometry(adjust, adjust, self.SCENE_WIDTH +adjust, self.SCENE_HEIGHT + adjust)
        self.setWindowTitle('Groogle')
        layout = QVBoxLayout()
        layout.addWidget(self.mView)
        self.setLayout(layout)
        self.show()


    def addCenterNode(self, name):
        self.mScene.clear()
        n = self.addNode(self.SCENE_WIDTH / 2 , self.SCENE_HEIGHT / 2, name)
        self.mCenterNode = n
        return self.mCenterNode

    def addNode(self, x, y, name):
        print "\n[*] addNode \tname:", name, "\tX:", x, "\tY:", y
        sys.stdout.flush()
        mNode = node.Node(self)
        mNode.mName = name
        mNode.setPos(QPoint(x, y));
#        mNode.setSelected(True);
        mNode.setVisible(True)
        self.mScene.addItem(mNode);
        self.mNodes.append(mNode);
        return mNode

    def findNode(self, name):
        for node in self.mNodes:
            if node.mName == name:
                return node

    def getPolarCoord(self, node, fromNode = ""):
        if fromNode == "":
            fromNode = self.mCenterNode

        vectorX = fromNode.x() - node.x()
        vectorY = fromNode.y() - node.y()
        
        angle = (math.atan2(vectorY, vectorX) * (180) / math.pi) % 360
        magnitude = math.sqrt(math.pow(vectorX, 2) + math.pow(vectorY, 2))
        return (magnitude, angle)

    def getCartCoord(self, mag, angle, pos):
        print "\n[*] getCardCoord \tmag:", mag, "\tangle:", angle
        x = mag * math.cos(float(angle)/ 180 * math.pi)
        y = mag * math.sin(float(angle) / 180 * math.pi)

        if node == "":
            nodeX = 0
            nodeY = 0
        else:
            nodeX = pos[0]
            nodeY = pos[1]
        
        return (round(x + nodeX), round(y + nodeY))

    # Level 0 = Center node
    # Level 1 = first circle of nodes
    def addNodes(self, words, level, baseNode = ""):
        assert level >= 1
        if baseNode == "":
            baseNode = self.mCenterNode

        deltaAngle = 360 / math.pow(2, level + 1)
        print "deltaAngle:", deltaAngle
        
        if level == 1:
            angle = 45
        else:
            angle = self.getPolarCoord(self.mCenterNode, baseNode)[1]
            angle -= 60
            print self.getPolarCoord(self.mCenterNode, baseNode)

        for i in range(0, self.NODES_PER_LEVEL):
            (nodeX, nodeY) = self.getCartCoord(self.NODE_MAGNITUDE, angle, (baseNode.x(), baseNode.y()))      

            newNode = self.addNode(nodeX, nodeY, words[i])
            l = link.Link(newNode, baseNode)
            self.mScene.addItem(l)
            self.mNodes.append(newNode)
            angle += deltaAngle
 
 
def main():

    # Set Google Query
    googleSearch = "\"raspberry pi\""    
    print "[*] Doing analysis on the google search:", googleSearch
    
    # Scrape and do analysis
    queries = groogle.buildQuery(googleSearch, 0)
    anal = analyzer.Analyzer(queries)
    topWords = anal.getTopWords(4)
    print "[*] Top words for", googleSearch,  ":", topWords

    # Start the viewer
    app = QtGui.QApplication(sys.argv)
    groogleView = GroogleView() 
    center = groogleView.addCenterNode(googleSearch)
    groogleView.addNodes(topWords, 1)

    time.sleep()
    # Let the app run
    sys.exit(app.exec_())

def test():
    googleSearch = "groogle"
    app = QtGui.QApplication(sys.argv)
    groogleView = GroogleView() 
    center = groogleView.addCenterNode(googleSearch)

    words = ["LOL", "IMAGOAT", "NOWAI", "H4X0RZ"]
    groogleView.addNodes(words, 1)

    words2 = ["LOL2", "LOLIMAGOAT", "METWO!!", "GTFO"]
    n = groogleView.findNode("LOL")
    groogleView.addNodes(words2, 2, n)

    m = groogleView.findNode("IMAGOAT")
    groogleView.addNodes(words2, 2, m)

    o = groogleView.findNode("NOWAI")
    groogleView.addNodes(words2, 2, o)

    p = groogleView.findNode("H4X0RZ")
    groogleView.addNodes(words2, 2, p)

    

    sys.exit(app.exec_())


if __name__ == '__main__':
    
    

    test()

#    main()

    
