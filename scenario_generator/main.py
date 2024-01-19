# main.py

# imports and other set-up
import sys

dir_input   = "./input/"
dir_output  = "./output/"

datafilestr = dir_input + ""
#--------------------------------------

from PyQt5.QtWidgets import QApplication
from window import Window

#--------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())