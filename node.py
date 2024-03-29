# node.py
# Structure for each individual node on the qgraphicsscene, also holds information about the word
# such as it's queryes and other relations

import sys

from PyQt4 import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *

from debug import *

class Node(QtGui.QGraphicsObject):
    def __init__(self, parent = None):
        super(Node, self).__init__()

        self.mName = ""
        self.mLinks = []
        self.mChildren = []
        self.mParent = ""
        self.mQueries = []

        self.mTextColor = Qt.Qt.darkGreen;
        self.mOutlineColor = Qt.Qt.darkBlue;
        self.mBackgroundColor = Qt.Qt.white;
        self.mIsHovered = False;
        self.mIsHighlighted = False;

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True);
        self.setAcceptDrops(True);
        self.setFlag(QtGui.QGraphicsItem.ItemSendsScenePositionChanges, True)

    def addLink(self, link):
        mLinks.append(link);

    def getAllChildren(self):
        out = [self]
        for child in self.mChildren:
            out += child.getAllChildren()
        return out

    def setHighlighted(self, val):
        self.mIsHighlighted = val

    def isHighlighted(self):
        return self.mIsHighlighted
    
    def getLink(self, node):
        for link in self.mLinks:
            if node == link.mToNode or node == link.mFromNode:
                return link
        errorMessage("node::getLink: no link between nodes found")

    def outlineRect(self):
        size = 60;
        roundness = 30
        rect = QtCore.QRectF(-size + roundness/2, -size + size/2, size + roundness, size); #yea ionno,but it works
    
        if (self.mIsHovered or self.mIsHighlighted):
            rect.adjust(-5, -5, 5, 5);

        return rect;

    def boundingRect(self):
        MARGIN = 6;
        return self.outlineRect().adjusted(-MARGIN, -MARGIN, MARGIN, MARGIN);

    def shape(self):
        rect = self.boundingRect()
        path = QtGui.QPainterPath()
        path.addEllipse(rect);
        return path;

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.mOutlineColor);
        if (option.state & Qt.QStyle.State_Selected):
            pen.setStyle(Qt.Qt.DotLine);
            pen.setWidth(2);

        if (self.mIsHighlighted):
            pen.setWidth(2)
            
            
        painter.setPen(pen);
        painter.setBrush(self.mBackgroundColor);

        rect = self.outlineRect();
        painter.drawEllipse(rect)
        
        painter.setPen(self.mTextColor);
        painter.drawText(rect, Qt.Qt.AlignCenter | Qt.Qt.TextWordWrap, self.mName);

    def hoverEnterEvent(self, event):
        self.mIsHovered = True;
        self.update();

    def hoverLeaveEvent(self, event):
        self.mIsHovered = False;
        self.update();

    def mouseDoubleClickEvent(self, event):
        QtCore.QObject.emit(self, QtCore.SIGNAL("doubleClickEvent"), self)

    def mousePressEvent(self, event):
        QtCore.QObject.emit(self, QtCore.SIGNAL("singlePressEvent"), self)

    def itemChange(self, change, value):
        if (change == QGraphicsItem.ItemPositionHasChanged):
            newPos = value.toPointF();
            for link in self.mLinks:
                link.trackNodes();
        return QVariant(value)

