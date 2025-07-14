#imports and other set-up
import sys
import csv

dir_sim_input   = "./sim_input/"
dir_sim_output  = "./sim_output/"

datafilestr = dir_sim_input + "dataOUT"
#--------------------------------------

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)
from display_location import Ui_MainWindow
#--------------------------------------

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        #event handles
        self.actionExportCSV.triggered.connect(self.exportCSV)
        self.textEditStartLatLon.textChanged.connect(self.updateStartLatLon)
        self.textEditEndLatLon.textChanged.connect(self.updateEndLatLon)
        self.actionImportCSV.triggered.connect(self.importCSV)

        #add other inits here
        self.startLatLontext = ""
        self.startLatLontextList = []
        self.endLatLontext = ""
        self.endLatLontextList = []
        self.graphicsView.show()

    #methods
    #--------------------------------------
    def exportCSV(self):
        if( ""==self.startLatLontext or ""==self.endLatLontext ):
            print("Export CSV: NO DATA")
        else:
            print("Export CSV: running...")
            datafile = open(datafilestr+".csv","w+")
            datafile.write("START Lat,START Lon,END Lat,END Lon\n") #create header
            #run through list: expected format: Lat#,Lon#\n...repeat for START and END
            tmpLen = min(len(self.startLatLontextList),len(self.endLatLontextList))
            for index in range(tmpLen):
                stext = self.startLatLontextList[index]
                etext = self.endLatLontextList[index]
                #
                tmpStartList = stext.split(",") 
                tmpEndList   = etext.split(",") 
                try:
                    tmpStartLat = float(tmpStartList[0].replace(" ","")) #remove whitespace on START
                    tmpStartLon = float(tmpStartList[1].replace(" ",""))
                    tmpEndLat = float(tmpEndList[0].replace(" ","")) #remove whitespace on END
                    tmpEndLon = float(tmpEndList[1].replace(" ",""))
                    datafile.write("%f,%f,%f,%f\n" %(tmpStartLat,tmpStartLon,tmpEndLat,tmpEndLon))
                    print("%f,%f,%f,%f" %(tmpStartLat,tmpStartLon,tmpEndLat,tmpEndLon))
                except:
                    print("Export CSV: ERROR: ["+str(index)+"]= "+str(tmpStartList)+"+"+str(tmpEndList))
            datafile.close()
            print("Export CSV: Done")
    #end exportCSV()

    def importCSV(self):
        print("Import CSV: running...")
        try:
            datafile = open(datafilestr+".csv","r")
            reader = csv.reader(datafile)
            reader.__next__() #skip header
            self.startLatLontext = "" #clear and ready for new data
            self.endLatLontext = ""
            for line in reader:
                try:
                    tmpStartLat = float(line[0].replace(" ","")) #remove whitespace on START
                    tmpStartLon = float(line[1].replace(" ",""))
                    tmpEndLat = float(line[2].replace(" ","")) #remove whitespace on END
                    tmpEndLon = float(line[3].replace(" ",""))
                    self.startLatLontext += str(tmpStartLat)+","+str(tmpStartLon)+"\n"
                    self.endLatLontext += str(tmpEndLat)+","+str(tmpEndLon)+"\n"
                except:
                    print("Import CSV: ERROR: "+str(line))
        except:
            print("Import CSV: ERROR: file="+str(datafilestr))
        #update data on gui
        if(""!=self.startLatLontext and ""!=self.endLatLontext):
            print("Import CSV: Adding data...")
            self.textEditStartLatLon.setText(self.startLatLontext)
            self.textEditEndLatLon.setText(self.endLatLontext)
            self.updateStartLatLon()
            self.updateEndLatLon()
        datafile.close()
        print("Import CSV: Done")
    #end importCSV()

    def updateStartLatLon(self):
        self.startLatLontext = self.textEditStartLatLon.toPlainText()
        print("Start Lat,Lon: "+self.startLatLontext)
        #
        #expected format: Lat#,Lon#\n...repeat
        self.startLatLontextList = self.startLatLontext.split("\n")
        print("Start Lat,Lon: line split: "+str(self.startLatLontextList))
        #
        self.updateGraphicView()
    #end updateStartLatLon()
    
    def updateEndLatLon(self):
        self.endLatLontext = self.textEditEndLatLon.toPlainText()
        print("End Lat,Lon: "+self.endLatLontext)
        #
        #expected format: Lat#,Lon#\n...repeat
        self.endLatLontextList = self.endLatLontext.split("\n")
        print("End Lat,Lon: line split: "+str(self.endLatLontextList))
        #
        self.updateGraphicView()
    #end updateEndLatLon()
    
    def updateGraphicView(self):
        scene = QtWidgets.QGraphicsScene()
        print("GraphicsView: running...")
        #---
        #run through list: expected format: Lat#,Lon#\n...repeat for START and END
        tmpLen = min(len(self.startLatLontextList),len(self.endLatLontextList))
        for index in range(tmpLen):
            stext = self.startLatLontextList[index]
            etext = self.endLatLontextList[index]
            #
            tmpStartList = stext.split(",") 
            tmpEndList   = etext.split(",") 
            try:
                tmpStartLat = float(tmpStartList[0].replace(" ","")) #remove whitespace on START
                tmpStartLon = float(tmpStartList[1].replace(" ",""))
                tmpEndLat = float(tmpEndList[0].replace(" ","")) #remove whitespace on END
                tmpEndLon = float(tmpEndList[1].replace(" ",""))
                scene.addLine(QtCore.QLineF(tmpStartLat, tmpStartLon, tmpEndLat, tmpEndLon))
                print("Line (%f,%f)->(%f,%f)" %(tmpStartLat,tmpStartLon,tmpEndLat,tmpEndLon))
            except:
                print("GraphicsView: ERROR: ["+str(index)+"]= "+str(tmpStartList)+"+"+str(tmpEndList))
        #---
        self.graphicsView.setScene(scene)
        self.graphicsView.invalidateScene() #redraw
        print("GraphicsView: Done")
    #end updateGraphicView()

#--------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Window()
    w.show()

    sys.exit(app.exec_())