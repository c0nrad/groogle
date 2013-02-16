# google.py
# 
# Top level file, serves as connector for three main modules (ui, scrapper, analysis)
import groogleView

import sys
from PyQt4.QtGui import *
from PyQt4 import *

def main():

    # Set Google Query
    googleSearch = "Microsoft"    
    print "[*] Doing analysis on the google search:", googleSearch
    
    # Start the viewer
    app = QtGui.QApplication(sys.argv)
    view = groogleView.GroogleView()
    view.addCenterNode(googleSearch)
    view.mModel.generateQueries(googleSearch, googleSearch)

    sys.exit(app.exec_())

if __name__ == '__main__':    
    main()
