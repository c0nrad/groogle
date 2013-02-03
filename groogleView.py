# view.py
#
# The interface for the user interface and data storage method

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *

import groogle
import node
import analyzer

import math
import time
import pdb

class GroogleView(QtGui.QWidget):
    
    def __init__(self):
        super(GroogleView, self).__init__()
        self.NODES_PER_LEVEL = 4
        self.NODE_MAGNITUDE = 150

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
        n= self.addNode(self.SCENE_WIDTH / 2 , self.SCENE_HEIGHT / 2, name)
        self.mCenterNode = n
        return self.mCenterNode

    def addNode(self, x, y, name):
        print "\n[*] addNode \tname:", name, "\tX:", x, "\tY:", y
        sys.stdout.flush()
        mNode = node.Node(self)
        mNode.mName = name
        mNode.setPos(QPoint(x, y));
        self.mScene.addItem(mNode);
        mNode.setSelected(True);
        mNode.setVisible(True)
        self.mNodes.append(mNode);
        return mNode

    def findNode(self, name):
        for node in self.mNodes:
            if node.mName == name:
                return node

    # Returns the polar coord in relation to the center node 
    def getPolarCoord(self, node):
        vectorX = self.mCenterNode.x() - node.x()
        vectorY = self.mCenterNode.y() - node.y()
        
        angle = (math.atan2(vectorY, vectorX) * (180) / math.pi) % 360
        magnitude = math.sqrt(math.pow(vectorX, 2) + math.pow(vectorY, 2))
        return (magnitude, angle)

    def getCartCoord(self, mag, angle):
        print "\n[*] getCardCoord \tmag:", mag, "\tangle:", angle
        x = mag * math.cos(float(angle)/ 180 * math.pi)
        y = mag * math.sin(float(angle) / 180 * math.pi)
        return (round(x), round(y))

    # Level 0 = Center node
    # Level 1 = first circle of nodes
    def addNodes(self, words, level, baseNode = ""):
        assert level >= 1
        if baseNode == "":
            baseNode = self.mCenterNode
            
        baseNodeX = baseNode.x()
        baseNodeY = baseNode.y()         
        deltaAngle = 360 / math.pow(self.NODES_PER_LEVEL, level)
        
        if level == 1:
            angle = 45
        else:
            angle = 0
        for i in range(0, self.NODES_PER_LEVEL):

            (x, y) = self.getCartCoord(self.NODE_MAGNITUDE, angle)
            
            (nodeX, nodeY) = (x + baseNodeX, y + baseNodeY)
            self.addNode(nodeX, nodeY, words[i])
            
            angle += deltaAngle

def main():

    
    queries = groogle.buildQuery
    googleSearch = "\"raspberry pi\""    
    print "[*] Doing analysis on the google search:", googleSearch
    
    queries = groogle.buildQuery(googleSearch, 0)
    anal = analyzer.Analyzer(queries)
    topWords = anal.getTopWords(4)
    print "[*] Top words for", googleSearch,  ":", topWords

    app = QtGui.QApplication(sys.argv)
    groogleView = GroogleView() 
    center = groogleView.addCenterNode(googleSearch)
    groogleView.addNodes(topWords, 1)

    assert groogleView.getCartCoord(5, 0) == (5, 0)
    
    sys.exit(app.exec_())


def test():
    assert groogleView.getCartCoord(5, 0) == (5, 0)

if __name__ == '__main__':
    
    

    test()
    main()

    
