
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
        self.setZValue(-2)
        self.mHighlightedColor = Qt.Qt.darkRed;
        self.mColor = Qt.Qt.darkBlue;
        self.trackNodes();

    def __str__(self):
        return "Link: ( " + self.mFromNode.mName + ", " + self.mToNode.mName + ")"

    def setHighlighted(self, val):
        if val:
            self.setZValue(-1)
        else:
            self.setZValue(-2)
        self.mIsHighlighted = val

    def isHighlighted(self):
        return self.mIsHighlighted

    def trackNodes(self):
        pen = QtGui.QPen();

        if self.isHighlighted():
            pen.setWidth(3)
            pen.setColor(self.mHighlightedColor)
        else:
            pen.setWidth(0)

        self.setPen(pen)
        self.setLine(QtCore.QLineF(self.mFromNode.pos(), self.mToNode.pos()))
