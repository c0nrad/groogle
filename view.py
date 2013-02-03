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
    
        self.mScene =  QGraphicsScene(0, 0, 600, 500)
        self.mView = QGraphicsView(self.mScene)
        self.mNodes = []
        self.mLinks = []

        self.initUI()        
        self.addNode(100, 100, "LOL")

    def initUI(self):      

        self.setGeometry(200, 200, 900, 800)
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
    sys.exit(app.exec_())

    n = node.Node()

if __name__ == '__main__':
    main()
