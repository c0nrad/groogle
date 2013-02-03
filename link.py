
import node
from PyQt4 import QtGui, QtCore, Qt

class Node(QtGui.QGraphicsItem):
    def __init__(self, parent = None):
        super(Node, self).__init__()


class Link(QtGui.QGraphicsLineItem):
    def __init__(self, fromNode, toNode, parent = None):
        super(Link, self).__init__()

        self.mFromNode = fromNode
        self.mToNode = toNode

        #self.mFromNode.addLink(self)
        #self.mToNode.addLink(self)
        self.setZValue(-1)
        self.mColor = Qt.Qt.darkRed;
        self.trackNodes();
        

    def trackNodes(self):
        self.setLine(QtCore.QLineF(self.mFromNode.pos(), self.mToNode.pos()))
