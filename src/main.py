import sys
from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import csv, wfdb
import numpy as np 
import pandas as pd
from math import ceil
#Local Imports

#Globals
main_Window = any


class MainWindow(QtWidgets.QMainWindow, ):
    def __init__(self,*args, **kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        uic.loadUi("./UI/layout.ui",self)

        self.setWindowTitle("")
        self.setWindowIcon(QtGui.QIcon("./Images/radio-waves.png"))
         
    




def main():
     myapp = QtWidgets.QApplication(sys.argv)
     main_Window = MainWindow()
     main_Window.show()
     sys.exit(myapp.exec_())        


if __name__ == "__main__" :
    main()    