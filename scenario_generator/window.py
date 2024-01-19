# window.py

from enum import Enum
class RadioState(Enum):
    Depot = 1
    Customer = 2
    Graph = 3

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from scenario_map import Ui_MainWindow  #Qt Design .ui file
from csv_helper import CSV_Helper
from crossing_helper import Crosswaypoint_Helper
from graph_helper import Graph_Helper

DEPOT_SIZE = 25
DEPOT_COLOR = QtGui.QColor("goldenrod")
CUSTOMER_SIZE = 10
CUSTOMER_COLOR = QtGui.QColor("blue")
CROSSPT_SIZE = 4
CROSSPT_COLOR = QtGui.QColor("orange")
#--------------------------------------

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        #event handles
        self.actionExportCSV.triggered.connect(self.exportCSV)
        self.actionImportCSV.triggered.connect(self.importCSV)
        self.textEditLatLon.textChanged.connect(self.updateLatLon)
        self.textEditCustomerLoc.textChanged.connect(self.updateLocCustomer)
        self.textEditDepotLoc.textChanged.connect(self.updateLocDepot)
        self.pushButtonNewRoute.pressed.connect(self.updateLatLonNewRoute)
        #self.pushButtonRandomRoute.pressed.connect(MainWindow.update)
        self.radioButtonCustomer.toggled['bool'].connect(self.readRadioCustomer)
        self.radioButtonDepot.toggled['bool'].connect(self.readRadioDepot)
        self.radioButtonGraph.toggled['bool'].connect(self.readRadioGraph)
        #self.pushButtonRandomGraph.pressed.connect(MainWindow.update)

        #add other events handles
        self.graphicsView.installEventFilter(self)

        #add other inits here
        self.LocCustomertext = ""
        self.LocCustomerList = []
        self.LocDepottext = ""
        self.LocDepotList = []
        self.LatLontext = ""
        self.LatLontextList = []
        self.LocCrosspttext = ""
        self.LocCrossptList = []
        #---
        self.radioState = RadioState.Graph
        #---
        self.graphicsView.show()
        self.gx = 0
        self.gy = 0
        self.gw = 600
        self.gh = 300
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.gx,self.gy,self.gw,self.gh)
        self.graphicsView.setScene(scene)
        self.graphicsView.invalidateScene() #redraw
    
    #for mouse/graphics handle ------------------ 
    def eventFilter(self, obj, event):
        if self.graphicsView is obj:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                mx = event.x() 
                my = event.y() 
                print(self.graphicsView, "press at ("+str(mx)+","+str(my)+")")
                lat = mx + self.gx
                lon = my + self.gy
                #
                #check which state...
                if(RadioState.Graph == self.radioState):                    
                    if(0 < len(self.LatLontext)):
                        #not first pt..
                        if(";"!=self.LatLontext[-1] and "\n"!=self.LatLontext[-1]): 
                            self.LatLontext += ";"
                    self.LatLontext += str(lat)+","+str(lon)
                elif(RadioState.Depot == self.radioState):
                    if(0 < len(self.LocDepottext)):
                        #not first pt..
                        if("\n"!=self.LocDepottext[-1]): 
                            self.LocDepottext += "\n"
                    tmpText = str(lat)+","+str(lon)+"\n"
                    self.LocDepottext += tmpText
                elif(RadioState.Customer == self.radioState):
                    if(0 < len(self.LocCustomertext)):
                        #not first pt..
                        if("\n"!=self.LocCustomertext[-1]): 
                            self.LocCustomertext += "\n"
                    tmpText = str(lat)+","+str(lon)+"\n"
                    self.LocCustomertext += tmpText
                #
                #update data on gui
                if(""!=self.LatLontext):
                    print("MousePress: Adding ROUTE data...")
                    self.textEditLatLon.setText(self.LatLontext)
                    self.updateLatLon()
                if(""!=self.LocCustomertext):
                    print("MousePress: Adding CUSTOMER data...")
                    self.textEditCustomerLoc.setText(self.LocCustomertext)
                    self.updateLocCustomer()
                if(""!=self.LocDepottext):
                    print("MousePress: Adding DEPOT data...")
                    self.textEditDepotLoc.setText(self.LocDepottext)
                    self.updateLocDepot()
        #end graphicsView
        return super(Window, self).eventFilter(obj, event)
    

    #MODIFY SELECTION ---------------------------
    def readRadioDepot(self, val):
        print("Depot = "+str(val))
        if(val): self.radioState = RadioState.Depot
    
    def readRadioCustomer(self, val):
        print("Customer = "+str(val))
        if(val): self.radioState = RadioState.Customer

    def readRadioGraph(self, val):
        print("Graph = "+str(val))
        if(val): self.radioState = RadioState.Graph

    #CSV FILE -----------------------------------
    def exportCSV(self):
        tmpcsv = CSV_Helper()
        tmpcsv.LatLontext = self.LatLontext
        tmpcsv.exportCSV_routes("./output/dataOUT.csv")
        tmpcsv.Depottext = self.LocDepottext
        tmpcsv.exportCSV_depots("./output/depot_loc.txt")
        tmpcsv.Customertext = self.LocCustomertext
        tmpcsv.exportCSV_customers("./output/customer_loc.txt")
        #graph output ---
        tmpgraph = Graph_Helper("./output/")
        tmpgraph.createDistanceMatrixPaths("./output/")
        tmpgraph.createDistanceMatrixStraightLineL2("./output/")

    def importCSV(self):
        tmpcsv = CSV_Helper()
        tmpcsv.importCSV_routes("./output/dataOUT.csv")
        self.LatLontext = tmpcsv.LatLontext
        tmpcsv.importCSV_depots("./output/depot_loc.txt")
        self.LocDepottext = tmpcsv.Depottext
        tmpcsv.importCSV_customers("./output/customer_loc.txt")
        self.LocCustomertext = tmpcsv.Customertext
        #update data on gui
        if(""!=self.LatLontext):
            print("Import CSV: Adding ROUTE data...")
            self.textEditLatLon.setText(self.LatLontext)
            self.updateLatLon()
        if(""!=self.LocCustomertext):
            print("Import CSV: Adding CUSTOMER data...")
            self.textEditCustomerLoc.setText(self.LocCustomertext)
            self.updateLocCustomer()
        if(""!=self.LocDepottext):
            print("Import CSV: Adding DEPOT data...")
            self.textEditDepotLoc.setText(self.LocDepottext)
            self.updateLocDepot()

    #ROUTE MODIFICATION -------------------------
    def updateLatLonNewRoute(self):
        self.LatLontext += "\n" 
        print("New Route Added")

    def updateLatLon(self):
        self.LatLontext = self.textEditLatLon.toPlainText()
        print("Lat,Lon: "+self.LatLontext)
        #expected format: #Lat#,Lon#;...\n...repeat
        self.LatLontextList = self.LatLontext.split("\n")
        print("Lat,Lon: line split: "+str(self.LatLontextList))
        self.updateRouteCrossing()
        self.updateGraphicView()

    def updateRouteCrossing(self):
        #brute-force compare..
        print("Cmp routes: START..")
        first_flag=True
        #run through list: expected format: #Lat#,Lon#;...repeat for START and END
        tmpLen = len(self.LatLontextList)
        for index1 in range(tmpLen):
            for index2 in range(tmpLen):
                text1 = self.LatLontextList[index1]
                text2 = self.LatLontextList[index2]
                #assume no self route intersect.. and 
                if(index1!=index2 and index1<index2):
                    tmpList1 = text1.split(";")
                    tmpList2 = text2.split(";")
                    #make sure not pt..
                    if(1<len(tmpList1) and 1<len(tmpList2)):
                        ptmpLat1 = None
                        ptmpLon1 = None
                        for tmpListPair1 in tmpList1:
                            ptmpLat2 = None
                            ptmpLon2 = None
                            for tmpListPair2 in tmpList2:
                                #--- one route
                                try:
                                    tmpLatLon1 = tmpListPair1.split(",")
                                    tmpLat1 = float(tmpLatLon1[0].replace(" ","")) #remove whitespace
                                    tmpLon1 = float(tmpLatLon1[1].replace(" ",""))
                                except:
                                    print("Cmp routes: Route Crossing: ERROR: "+str(tmpListPair1))
                                #--- other route
                                try:
                                    tmpLatLon2 = tmpListPair2.split(",")
                                    tmpLat2 = float(tmpLatLon2[0].replace(" ","")) #remove whitespace
                                    tmpLon2 = float(tmpLatLon2[1].replace(" ",""))
                                except:
                                    print("Cmp routes: Route Crossing: ERROR: "+str(tmpListPair2))
                                #--- COMPARE
                                if(None!=ptmpLat1 and None!=ptmpLat2):
                                    new_data_flag = True
                                    if(first_flag): 
                                        new_data_flag = False
                                        first_flag = False
                                        print("Cmp routes: First Flag set")
                                    sourceList = [ [index1,ptmpLat1,ptmpLon1,index1],[index2,ptmpLat2,ptmpLon2,index2] ]
                                    destinList = [ [index1,tmpLat1,tmpLon1,index1],  [index2,tmpLat2,tmpLon2,index2] ]
                                    print("Cmp routes: source = "+str(sourceList))
                                    print("Cmp routes: destin = "+str(destinList))
                                    tmpCmp = Crosswaypoint_Helper(sourceList,destinList)
                                    tmpCmp.straightLine("./output/",new_data_flag)
                                    print("Cmp routes: [ "+str(index1)+"->"+str(index2)+" ]")
                                #update2
                                ptmpLat2 = tmpLat2
                                ptmpLon2 = tmpLon2
                            #update1
                            ptmpLat1 = tmpLat1
                            ptmpLon1 = tmpLon1
        #update
        print("Cmp routes: DONE")
        tmpCmp = Crosswaypoint_Helper()
        self.LocCrosspttext = tmpCmp.readFromFile("./output/")
        self.LocCrossptList = self.LocCrosspttext.split("\n")

    #CUSTOMER-DEPOT MODIFICATION ----------------
    def updateCustomerNum(self):
        tmpNum = len(self.LocCustomerList)
        if(tmpNum>0):
            if(""==self.LocCustomerList[-1]): tmpNum -= 1
            tmpNumStr = str(tmpNum)
            self.textEditCustomer.setText(tmpNumStr)
            print("Updated Customer Num="+tmpNumStr)

    def updateLocCustomer(self):
        self.LocCustomertext = self.textEditCustomerLoc.toPlainText()
        print("Customer Lat,Lon: "+self.LocCustomertext)
        #expected format: #Lat#,Lon#\n...repeat
        self.LocCustomerList = self.LocCustomertext.split("\n")
        print("Customer Lat,Lon: line split: "+str(self.LocCustomerList))
        self.updateCustomerNum()
        self.updateGraphicView()

    def updateDepotNum(self):
        tmpNum = len(self.LocDepotList)
        if(tmpNum>0):
            if(""==self.LocDepotList[-1]): tmpNum -= 1
            tmpNumStr = str(tmpNum)
            self.textEditDepot.setText(tmpNumStr)
            print("Updated Depot Num="+tmpNumStr)

    def updateLocDepot(self):
        self.LocDepottext = self.textEditDepotLoc.toPlainText()
        print("Depot Lat,Lon: "+self.LocDepottext)
        #expected format: #Lat#,Lon#\n...repeat
        self.LocDepotList = self.LocDepottext.split("\n")
        print("Depot Lat,Lon: line split: "+str(self.LocDepotList))
        self.updateDepotNum()
        self.updateGraphicView()
    
    #VISUAL GRAPHIC DISPLAY ---------------------
    def updateGraphicView(self):
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.gx,self.gy, self.gw,self.gh)
        w = scene.width()
        h = scene.height()
        print("GraphicsView: running... ("+str(w)+","+str(h)+")")
        #---
        #run through list: expected format: #Lat#,Lon#;...repeat for START and END
        tmpLen = len(self.LatLontextList)
        for index in range(tmpLen):
            text = self.LatLontextList[index]
            #
            tmpList = text.split(";")
            ptmpLat = None
            ptmpLon = None
            for tmpListPair in tmpList:
                try:
                    tmpLatLon = tmpListPair.split(",")
                    tmpLat = float(tmpLatLon[0].replace(" ","")) #remove whitespace
                    tmpLon = float(tmpLatLon[1].replace(" ",""))
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
        #run through Depot list: expected format: #Lat#,Lon#...repeat
        for tmpLoc in self.LocDepotList:
            try:
                tmpList = tmpLoc.split(",")
                tmpLat = float(tmpList[0].replace(" ","")) #remove whitespace
                tmpLon = float(tmpList[1].replace(" ",""))
                scene.addEllipse(tmpLat, tmpLon, DEPOT_SIZE,DEPOT_SIZE, DEPOT_COLOR)
                print("Depot (%f,%f)" %(tmpLat, tmpLon))
            except:
                print("GraphicsView: ERROR: "+str(tmpLoc))
        #---
        #run through Customer list: expected format: #Lat#,Lon#...repeat
        for tmpLoc in self.LocCustomerList:
            try:
                tmpList = tmpLoc.split(",")
                tmpLat = float(tmpList[0].replace(" ","")) #remove whitespace
                tmpLon = float(tmpList[1].replace(" ",""))
                scene.addEllipse(tmpLat, tmpLon, CUSTOMER_SIZE,CUSTOMER_SIZE, CUSTOMER_COLOR)
                print("Customer (%f,%f)" %(tmpLat, tmpLon))
            except:
                print("GraphicsView: ERROR: "+str(tmpLoc))
        #---
        #run through crossing pts
        for tmpLoc in self.LocCrossptList:
            try:
                tmpList = tmpLoc.split(",")
                tmpLat = float(tmpList[0].replace(" ","")) #remove whitespace
                tmpLon = float(tmpList[1].replace(" ",""))
                scene.addEllipse(tmpLat, tmpLon, CROSSPT_SIZE,CROSSPT_SIZE, CROSSPT_COLOR)
                print("Crossing pt (%f,%f)" %(tmpLat, tmpLon))
            except:
                print("GraphicsView: ERROR: "+str(tmpLoc))
        #---
        self.graphicsView.setScene(scene)
        self.graphicsView.invalidateScene() #redraw
        print("GraphicsView: Done")
    #end updateGraphicView()
