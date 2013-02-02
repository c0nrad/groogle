# node.py

# Structure for each individual node on the qgraphicsscene, also holds information about the word
# such as it's queryes and other relations

import sys

from PyQt4 import QtGui, QtCore, Qt

class Node(QtGui.QGraphicsItem):
    def __init__(self, parent = None):
        super(Node, self).__init__()

        self.mName = "LOLNOWAI"
        self.update()
        self.mTextColor = Qt.Qt.darkGreen;
        self.mOutlineColor = Qt.Qt.darkBlue;
        self.mBackgroundColor = Qt.Qt.white;
        self.mIsHovered = False;

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True);
        self.setAcceptDrops(True);

#    def addLink(self, link):
#        mLinks.insert(link);
     
#    def removeLink(self, link):
#        mLinks.remove(link);

    def outlineRect(self):
        SIZE = 80;
        constSize = QtCore.QRectF(-SIZE/2, -SIZE/2, SIZE, SIZE);

        if (self.mIsHovered):
            constSize.adjust(-5, -5, 5, 5);
        return constSize;

    def boundingRect(self):
        MARGIN = 6;
        return self.outlineRect().adjusted(-MARGIN, -MARGIN, MARGIN, MARGIN);

    def shape(self):
        rect = self.outlineRect();

        path = QtGui.QPainterPath()
        path.addRoundRect(rect, self.roundness(rect.width()), self.roundness(rect.height()));
        return path;

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.mOutlineColor);
        if (option.state & Qt.QStyle.State_Selected):
            pen.setStyle(Qt.Qt.DotLine);
            pen.setWidth(2);
            

        painter.setPen(pen);
        painter.setBrush(self.mBackgroundColor);

        rect = self.outlineRect();
        painter.drawRoundedRect(rect, self.roundness(rect.width()), self.roundness(rect.height()));
        
        painter.setPen(self.mTextColor);
        painter.drawText(rect, Qt.Qt.AlignCenter | Qt.Qt.TextWordWrap, self.mName);

    def roundness(self, size):
        DIAMETER = 12;
        return 50 * DIAMETER / int(size);

    def hoverEnterEvent(self, event):
        self.mIsHovered = True;
        self.update();

    def hoverLeaveEvent(self, event):
        self.mIsHovered = False;
        self.update();




