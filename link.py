
import node
from debug import *
from PyQt4 import QtGui, QtCore, Qt

class Link(QtGui.QGraphicsLineItem):
    def __init__(self, fromNode, toNode, parent = None):
        super(Link, self).__init__()

        self.mFromNode = fromNode
        self.mToNode = toNode
        self.mIsHighlighted = False

        self.mFromNode.mLinks.append(self)
        self.mToNode.mLinks.append(self)
        self.setZValue(-1)
        self.mColor = Qt.Qt.darkRed;
        self.trackNodes();

    def setHighlighted(self, val):
        self.mIsHighlighted = val

    def trackNodes(self):
        pen = QtGui.QPen(self.mColor);
        pen.setWidth(0)

        if self.mIsHighlighted == True:
            pen.setWidth(2)
            
            
        self.setPen(pen)
        self.setLine(QtCore.QLineF(self.mFromNode.pos(), self.mToNode.pos()))
