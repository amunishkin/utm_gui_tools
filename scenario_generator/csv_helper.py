# csv_helper.py

import sys
import csv

#------------------------------------------------

class CSV_Helper():
    def __init__(self, routeTxt="", depotTxt="", customerTxt=""):
        self.LatLontext = routeTxt
        self.Depottext = depotTxt
        self.Customertext = customerTxt

    #methods ------------------------------------
    def exportCSV_customers(self, file):
        if( ""==self.Customertext ):
            print("Export CSV: NO CUSTOMER DATA")
        else:
            print("Export CSV: CUSTOMER running...")
            datafilestr = file
            datafile = open(datafilestr,"w+")
            #run through list: expected format: #Lat#,Lon#\n...repeat
            CustomertextList = self.Customertext.split("\n")
            tmpLen = len(CustomertextList)
            for index in range(tmpLen):                
                try:
                    text = CustomertextList[index]
                    if(""==text): break
                    tmpstr = "Customer,"+str(index)
                    tmpList = text.split(",")
                    tmpLat = tmpList[0].replace(" ","") #remove whitespace
                    tmpLon = tmpList[1].replace(" ","")
                    tmpstr += ","+str(tmpLat)+","+str(tmpLon)+"\n"
                    datafile.write(tmpstr)
                    print(tmpstr, end="")
                except:
                    print("Export CSV: CUSTOMER ERROR: "+str(text))
            #end    
            datafile.close()
            print("Export CSV: CUSTOMER Done")

    def exportCSV_depots(self, file):
        if( ""==self.Depottext ):
            print("Export CSV: NO DEPOT DATA")
        else:
            print("Export CSV: DEPOT running...")
            datafilestr = file
            datafile = open(datafilestr,"w+")
            #run through list: expected format: #Lat#,Lon#\n...repeat
            DepottextList = self.Depottext.split("\n")
            tmpLen = len(DepottextList)
            for index in range(tmpLen):                
                try:
                    text = DepottextList[index]
                    if(""==text): break
                    tmpstr = "Depot,"+str(index)
                    tmpList = text.split(",")
                    tmpLat = tmpList[0].replace(" ","") #remove whitespace
                    tmpLon = tmpList[1].replace(" ","")
                    tmpstr += ","+str(tmpLat)+","+str(tmpLon)+"\n"
                    datafile.write(tmpstr)
                    print(tmpstr, end="")
                except:
                    print("Export CSV: DEPOT ERROR: "+str(text))
            #end    
            datafile.close()
            print("Export CSV: DEPOT Done")

    def exportCSV_routes(self, file):
        if( ""==self.LatLontext ):
            print("Export CSV: NO ROUTE DATA")
        else:
            print("Export CSV: ROUTE running...")
            datafilestr = file
            datafile = open(datafilestr,"w+")
            datafile.write("# of pts,START Lat,START Lon,...,END Lat,END Lon\n") #create header
            #run through list: expected format: #Lat#,Lon#;...\n...repeat for START and END
            LatLontextList = self.LatLontext.split("\n")
            tmpLen = len(LatLontextList)
            for index in range(tmpLen):
                text = LatLontextList[index]
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
                        print("Export CSV: ROUTE ERROR: "+str(tmpListPair))
                tmpstr += "\n"
                #end for
                datafile.write(tmpstr)
                print(tmpstr, end="")
            #end    
            datafile.close()
            print("Export CSV: ROUTE Done")
    #end exportCSV()

    #---
    def importCSV_customers(self, file):
        print("Import CSV: CUSTOMER running...")
        try:
            datafilestr = file
            datafile = open(datafilestr,"r")
            reader = csv.reader(datafile)
            self.Customertext = "" #clear and ready for new data
            for line in reader:
                try:
                    tmpLat = float(line[2].replace(" ",""))
                    tmpLon = float(line[3].replace(" ",""))
                    self.Customertext += str(tmpLat)+","+str(tmpLon)+"\n"
                except:
                    print("Import CSV: CUSTOMER ERROR: "+str(line))
        except:
            print("Import CSV: CUSTOMER ERROR: file="+str(datafilestr))
        #end
        datafile.close()
        print("Import CSV: CUSTOMER Done")

    def importCSV_depots(self, file):
        print("Import CSV: DEPOT running...")
        try:
            datafilestr = file
            datafile = open(datafilestr,"r")
            reader = csv.reader(datafile)
            self.Depottext = "" #clear and ready for new data
            for line in reader:
                try:
                    tmpLat = float(line[2].replace(" ",""))
                    tmpLon = float(line[3].replace(" ",""))
                    self.Depottext += str(tmpLat)+","+str(tmpLon)+"\n"
                except:
                    print("Import CSV: DEPOT ERROR: "+str(line))
        except:
            print("Import CSV: DEPOT ERROR: file="+str(datafilestr))
        #end
        datafile.close()
        print("Import CSV: DEPOT Done")

    def importCSV_routes(self, file):
        print("Import CSV: ROUTE running...")
        try:
            datafilestr = file
            datafile = open(datafilestr,"r")
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
                    print("Import CSV: ROUTE ERROR: "+str(line))
        except:
            print("Import CSV: ROUTE ERROR: file="+str(datafilestr))
        #end
        datafile.close()
        print("Import CSV: ROUTE Done")
    #end importCSV()