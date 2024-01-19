#imports and other set-up
import sys
import csv

dir_sim_input   = "./sim_input/"
dir_sim_output  = "./sim_output/"

datafilestr = dir_sim_input + "dataOUT_2"
#--------------------------------------

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)
from display_location_2 import Ui_MainWindow
#--------------------------------------

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        #event handles
        self.actionExportCSV.triggered.connect(self.exportCSV)
        self.textEditLatLon.textChanged.connect(self.updateLatLon)
        self.actionImportCSV.triggered.connect(self.importCSV)
        self.pushButtonNewRoute.pressed.connect(self.updateLatLonNewRoute)
        #self.pushButtonRandomRoute.pressed.connect(MainWindow.update)

        #add other events handles
        self.graphicsView.installEventFilter(self)

        #add other inits here
        self.LatLontext = ""
        self.LatLontextList = []
        self.graphicsView.show()
        #
        self.gx = 10
        self.gy = 10
        self.gw = 600
        self.gh = 300
        #
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.gx,self.gy,self.gw,self.gh)
        self.graphicsView.setScene(scene)
        self.graphicsView.invalidateScene() #redraw
    
    #generic event handler function -- for mouse/graphics 
    def eventFilter(self, obj, event):
        if self.graphicsView is obj:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                mx = event.x() + self.gx
                my = event.y() + self.gy
                print(self.graphicsView, "press at ("+str(mx)+","+str(my)+")")
                #---
                lat = mx
                lon = my
                if(0 < len(self.LatLontext)):
                    #not first pt..
                    if(";"!=self.LatLontext[-1] and "\n"!=self.LatLontext[-1]): 
                        self.LatLontext += ";"
                self.LatLontext += str(lat)+","+str(lon)
                #update data on gui
                if(""!=self.LatLontext):
                    print("MousePress: Adding data...")
                    self.textEditLatLon.setText(self.LatLontext)
                    self.updateLatLon()
        return super(Window, self).eventFilter(obj, event)
    
    #methods
    #--------------------------------------
    def exportCSV(self):
        if( ""==self.LatLontext ):
            print("Export CSV: NO DATA")
        else:
            print("Export CSV: running...")
            datafile = open(datafilestr+".csv","w+")
            datafile.write("# of pts,START Lat,START Lon,...,END Lat,END Lon\n") #create header
            #run through list: expected format: #Lat#,Lon#;...\n...repeat for START and END
            tmpLen = len(self.LatLontextList)
            for index in range(tmpLen):
                text = self.LatLontextList[index]
                #
                tmpList = text.split(";")
                tmpstr = str(len(tmpList))
                for tmpListPair in tmpList:
                    try:
                        tmpList = tmpListPair.split(",")
                        tmpLat = tmpList[0].replace(" ","") #remove whitespace
                        tmpLon = tmpList[1].replace(" ","")
                        tmpstr += ","+str(tmpLat)+","+str(tmpLon)
                    except:
                        print("Export CSV: ERROR: "+str(tmpListPair))
                tmpstr += "\n"
                #end for
                datafile.write(tmpstr)
                print(tmpstr)
            #end    
            datafile.close()
            print("Export CSV: Done")
    #end exportCSV()

    def importCSV(self):
        print("Import CSV: running...")
        try:
            datafile = open(datafilestr+".csv","r")
            reader = csv.reader(datafile)
            reader.__next__() #skip header
            self.LatLontext = "" #clear and ready for new data
            for line in reader:
                try:
                    tmpCnt = int(line[0].replace(" ","")) #remove whitespace
                    cnt = 0
                    for i in range(1,2*tmpCnt,2):
                        tmpLat = float(line[i].replace(" ",""))
                        tmpLon = float(line[i+1].replace(" ",""))
                        if(0<cnt): self.LatLontext += ";"
                        self.LatLontext += str(tmpLat)+","+str(tmpLon)
                        cnt += 1
                    self.LatLontext += "\n"
                except:
                    print("Import CSV: ERROR: "+str(line))
        except:
            print("Import CSV: ERROR: file="+str(datafilestr))
        #update data on gui
        if(""!=self.LatLontext):
            print("Import CSV: Adding data...")
            self.textEditLatLon.setText(self.LatLontext)
            self.updateLatLon()
        datafile.close()
        print("Import CSV: Done")
    #end importCSV()

    def updateLatLonNewRoute(self):
        self.LatLontext += "\n" 

    def updateLatLon(self):
        self.LatLontext = self.textEditLatLon.toPlainText()
        print("Lat,Lon: "+self.LatLontext)
        #
        #expected format: #Lat#,Lon#;...\n...repeat
        self.LatLontextList = self.LatLontext.split("\n")
        print("Lat,Lon: line split: "+str(self.LatLontextList))
        #
        self.updateGraphicView()
    #end updateLatLon()
    
    def updateGraphicView(self):
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.gx,self.gy, self.gw,self.gh)
        w = scene.width()
        h = scene.height()
        print("GraphicsView: running... ("+str(w)+","+str(h)+")")
        #---
        #run through list: expected format: #Lat#,Lon#;...\n...repeat for START and END
        tmpLen = len(self.LatLontextList)
        for index in range(tmpLen):
            text = self.LatLontextList[index]
            #
            tmpList = text.split(";")
            ptmpLat = None
            ptmpLon = None
            for tmpListPair in tmpList:
                try:
                    tmpList = tmpListPair.split(",")
                    tmpLat = float(tmpList[0].replace(" ","")) #remove whitespace
                    tmpLon = float(tmpList[1].replace(" ",""))
                    if(None!=ptmpLat and None!=ptmpLon):
                        scene.addLine(QtCore.QLineF(ptmpLat, ptmpLon, tmpLat, tmpLon))
                        print("Line (%f,%f)->(%f,%f)" %(ptmpLat, ptmpLon, tmpLat, tmpLon))
                    else:
                        scene.addLine(QtCore.QLineF(tmpLat, tmpLon, tmpLat, tmpLon))
                        print("Start Pt (%f,%f)" %(tmpLat, tmpLon))
                    ptmpLat = tmpLat
                    ptmpLon = tmpLon
                except:
                    print("GraphicsView: ERROR: "+str(tmpListPair))
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