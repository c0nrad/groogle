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
import model
from debug import *

import math
import time
import pdb

class GroogleView(QtGui.QWidget):
    
    def __init__(self):
        super(GroogleView, self).__init__()
        self.NODES_PER_LEVEL = 6
        self.NODE_MAGNITUDE = 200

        self.SCENE_HEIGHT = 600
        self.SCENE_WIDTH = 900
    
        self.mScene =  QGraphicsScene(0, 0, self.SCENE_WIDTH, self.SCENE_HEIGHT)
        self.mView = QGraphicsView(self.mScene)
        self.mNodes = []
        self.mLinks = []
        self.initUI()        

        googleSearch = "Microsoft"
        self.mModel = model.Model(self)

    def initUI(self):      
        adjust = 200
        self.setGeometry(adjust, adjust, self.SCENE_WIDTH +adjust, self.SCENE_HEIGHT + adjust)
        self.setWindowTitle('Groogle')
        layout = QVBoxLayout()
        layout.addWidget(self.mView)
        self.setLayout(layout)
        self.show()

    def addCenterNode(self, name):
        goodMessage("groogleView::addCenterNode: ", name)
        self.mScene.clear()
        n = self.addNode(self.SCENE_WIDTH / 2 , self.SCENE_HEIGHT / 2, name)
        self.mCenterNode = n
        return self.mCenterNode

    def addNode(self, x, y, name):
        goodMessage("addNode name: ", name, "X: ", x, "Y: ", y)
        sys.stdout.flush()
        mNode = node.Node(self)
        mNode.mName = name
        mNode.setPos(QPoint(x, y));
        mNode.setVisible(True)
        self.mScene.addItem(mNode);
        self.mNodes.append(mNode);

        # Fragile, fix it
        self.connect(mNode, SIGNAL("doubleClickEvent"), self.handleDoubleClick)

        return mNode

    def handleDoubleClick(self, n):
        infoMessage("Double click signal recieved from: ", n.mName)
        self.mModel.generateQueries(n.mName, n.mName + " " + n.mParent.mName, 0)

    def findNode(self, name):
        for node in self.mNodes:
            if name.lower() == node.mName.lower():
                return node
        return ""

    def getPolarCoord(self, node, fromNode = ""):
#        if not type(node) is node.Node:
#            errorMessage("googleView::getPolarCoord: node isn't of type node")

        if fromNode == "":
            fromNode = self.mCenterNode

        vectorX = fromNode.x() - node.x()
        vectorY = fromNode.y() - node.y()
        
        angle = (math.atan2(vectorY, vectorX) * (180) / math.pi) % 360
        magnitude = math.sqrt(math.pow(vectorX, 2) + math.pow(vectorY, 2))
        return (magnitude, angle)

    def getCartCoord(self, mag, angle, pos):
        x = mag * math.cos(float(angle)/ 180 * math.pi)
        y = mag * math.sin(float(angle) / 180 * math.pi)

        if node == "":
            nodeX = 0
            nodeY = 0
        else:
            nodeX = pos[0]
            nodeY = pos[1]
        
        return (round(x + nodeX), round(y + nodeY))

    def removeNode(self, node):
#        if not type(node) is node.Node:
#            errorMessage("googleView::removeNode: node isn't of type node")

        infoMessage("Removing node: ", node.mName)
 
        for child in node.mChildren:
            self.removeChildren(child)

        for link in node.mLinks:
            self.mScene.removeItem(link)
        node.mLinks = []
            
        if node in self.mScene.items():
            self.mScene.removeItem(node)
        else:
            errorMessage("groogleView::removeNode: removing item not in scene!")
            
        if node in self.mNodes:
            self.mNodes.remove(node)
        else:
            errorMessage("groogleView::removeNode: removing item not in mNodes!")

    def removeChildren(self, node):
        for child in node.mChildren:
            self.removeNode(child)
            
        node.mChildren = []

    # Level 0 = Center node
    # Level 1 = first circle of nodes
    def addNodes(self, centerWord, words):
        centerNode = self.findNode(centerWord)
        if centerNode == "":
            errorMessage("groogleView::addNodes: The center node doesn't exist: ", centerNode)
        
        if len(words) == 0:
            warningMessage("groogleView::addNodes: no words to be added?")

        if centerWord in words:
            warningMessage("groogleView::addNodes: attempting to re-add the center node")

        self.removeChildren(centerNode)
        deltaAngle = 360 / math.pow(self.NODES_PER_LEVEL, 1)
        angle = 45
        centerNodePos = (centerNode.x(), centerNode.y())
        nodeCount = 0

        for wordItem in words:
            if (nodeCount >= self.NODES_PER_LEVEL):
                break

            word = wordItem[0]
            
            existingNode = self.findNode(word)
            if not existingNode == "":
                self.addLink(existingNode, centerNode)
                continue

            (nodeX, nodeY) = self.getCartCoord(self.NODE_MAGNITUDE, angle, centerNodePos)      

            newNode = self.addNode(nodeX, nodeY, word)
            newNode.mParent = centerNode
            centerNode.mChildren.append(newNode)
            self.addLink(newNode, centerNode)
            self.mNodes.append(newNode)
                    
            angle += deltaAngle 
            nodeCount += 1

    def addLink(self, nodeA, nodeB):
        if (nodeA == nodeB):
            errorMessage("groogleView::addLink: nodes can't be the same")
            return
        
        l = link.Link(nodeA, nodeB)
        self.mScene.addItem(l)
        return
 
def main():

    # Set Google Query
    googleSearch = "apple"    
    print "[*] Doing analysis on the google search:", googleSearch
    
    # Start the viewer
    app = QtGui.QApplication(sys.argv)
    groogleView = GroogleView()
    groogleView.addCenterNode(googleSearch)
    groogleView.mModel.generateQueries(googleSearch, googleSearch, 0)

    sys.exit(app.exec_())

if __name__ == '__main__':    
    main()

    
