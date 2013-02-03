# view.py
#
# The interface for the user interface and data storage method


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *

import time
import node
import pdb


class View(QtGui.QWidget):
    
    def __init__(self):
        super(View, self).__init__()
        self.NODES_PER_LEVEL = 5
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


    def addNode(self, x, y, name):
        print "[*] Adding node \"", name, "\" at X:", x, "Y:", y, 
        sys.stdout.flush()

        mNode = node.Node(self)
        mNode.mName = name
        mNode.setPos(QPoint(x, y));

        self.mScene.addItem(mNode);

        mNode.setSelected(True);
        mNode.setVisible(True)
        
        self.mNodes.append(mNode);
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    view = View()
    view.addNode(view.SCENE_WIDTH / 2 , view.SCENE_HEIGHT / 2, "groogle")



    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
