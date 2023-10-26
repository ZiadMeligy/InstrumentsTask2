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
        init_connectors(self)
        self.plot1=self.plotGraph1.plot()
        self.plot2=self.plotGraph1.plot()
        self.plot3=self.plotGraph1.plot()
        self.setWindowTitle("")
        self.setWindowIcon(QtGui.QIcon("./Images/radio-waves.png"))

         
    







def BrowseFile(self):
    df = pd.read_csv("EEG_Eye_State.csv")
    data2=df.drop("eyeDetection",axis=1)



    for q in data2.columns:
        data2 = remove_outliers_iqr(data2, q)

    eeg_data = data2[['FC5']]
    count=eeg_data.count(axis=0).values[0]

    eeg_data2 = data2[['AF3']]
    y_axis2 = eeg_data2.AF3.values

    eeg_data3 = data2[['T8']]
    y_axis3 = eeg_data3.T8.values

    y_axis = eeg_data.FC5.values
   
    x_axis = np.linspace(0, 117, count)
    self.plot3.setData(x_axis, y_axis3)
    self.plot2.setData(x_axis, y_axis2)
    self.plot1.setData(x_axis,y_axis)
    view_box=self.plot1.getViewBox()

    


   


def remove_outliers_iqr(data, column):
    # Calculate the first quartile and the third quartile
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    # Calculate the IQR
    iqr = q3 - q1
    # Calculating the thrshold
    threshold = 3 * iqr
    # Defining the lower and upper bounds
    lower_bound = q1 - threshold
    upper_bound = q3 + threshold
    # Filtering and returning the filtered data
    filtered_data = data[(data[column] >= lower_bound) &
                         (data[column] <= upper_bound)]
    return filtered_data


def init_connectors(self):
    self.browseBtn1.clicked.connect(lambda: BrowseFile(self))
    

def main():
     myapp = QtWidgets.QApplication(sys.argv)
     main_Window = MainWindow()
     main_Window.show()
     sys.exit(myapp.exec_())        


if __name__ == "__main__" :
    main()    