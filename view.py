# view.py
#
# The interface for the user interface and data storage method


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *

import time



class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.mScene = QGraphicsScene()
        self.mView = QGraphicsView(self.mScene)
        self.mNodes = []
        self.mLinks = []

        self.initUI()        
        self.addNode()

    def initUI(self):      

        self.setGeometry(200, 200, 900, 800)
        self.setWindowTitle('Groogle')

        layout = QVBoxLayout()
        layout.addWidget(self.mView)
        self.setLayout(layout)

        self.show()

    def addNode(self):
        ellipse = QGraphicsEllipseItem()
        ellipse.setRect(100, 100, 100, 100)
        self.mScene.addItem(ellipse)

    def drawRectangles(self, qp):
      
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        qp.setBrush(QtGui.QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QtGui.QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QtGui.QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)
              
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
