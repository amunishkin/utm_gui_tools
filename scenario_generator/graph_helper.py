# graph_helper.py

import sys
import csv
import math

#------------------------------------------------

class Graph_Helper():
    def __init__(self, dir_path_input):
        #depot ---
        self.Depot_Loc = []
        try:
            datafilestr = dir_path_input+"depot_loc.txt"
            datafile = open(datafilestr,"r")
            reader = csv.reader(datafile)
            for line in reader:
                try:
                    tmpid = float(line[1].replace(" ",""))
                    tmpLat = float(line[2].replace(" ",""))
                    tmpLon = float(line[3].replace(" ",""))
                    self.Depot_Loc.append( (tmpid,tmpLat,tmpLon) )
                except:
                    print("Read Graph: ERROR: "+str(line))
        except:
            print("Read Graph: ERROR: file="+str(datafilestr))
        datafile.close()
        #customer ---
        self.Cust_Loc = []
        try:
            datafilestr = dir_path_input+"customer_loc.txt"
            datafile = open(datafilestr,"r")
            reader = csv.reader(datafile)
            for line in reader:
                try:
                    tmpid = float(line[1].replace(" ",""))
                    tmpLat = float(line[2].replace(" ",""))
                    tmpLon = float(line[3].replace(" ",""))
                    self.Cust_Loc.append( (tmpid,tmpLat,tmpLon) )
                except:
                    print("Read Graph: ERROR: "+str(line))
        except:
            print("Read Graph: ERROR: file="+str(datafilestr))
        datafile.close()
        #---
        self.num_cust = len(self.Cust_Loc)
        self.num_dept = len(self.Depot_Loc)

    #methods ------------------------------------
    def createDistanceMatrixPaths(self, dir_path_output):
        #init.. load paths
        file = open(dir_path_output+"paths.txt", "r")
        reader = csv.reader(file, delimiter=";")
        sPaths = []
        for line in reader:
            try:
                L = []
                for iwaypt in line:
                    if(""==iwaypt): continue
                    try:
                        tmpLat = float(iwaypt[0].replace(" ",""))
                        tmpLon = float(iwaypt[1].replace(" ",""))
                        L.append( (tmpLat,tmpLon) )
                    except:
                        print("Read Graph: PT ERROR: >"+str(iwaypt)+"<")
                sPaths.append( L )
            except:
                print("Read Graph: ERROR: "+str(line))
        #
        #create D(i,j) matrix based on paths
        #waypoint_i to waypoint_j (depot,customer, or normal waypoint)
        f_d_matrix = open(dir_path_output+"distance_matrix_path.csv", "w+")
        f_d_matrix.write("Number of Customers, %d\n" %self.num_cust)
        f_d_matrix.write("Number of Depots, %d\n" %self.num_dept)
        #write out header for matrix
        #TODO: header here...
        f_d_matrix.write("       , ")
        ispath_cnt = 0
        for idept in self.Depot_Loc:
            f_d_matrix.write("Dept-%d: " %idept[0])
            for ispath in sPaths:
                f_d_matrix.write("sPath-%d, " %ispath_cnt)
                ispath_cnt += 1
                for iswaypoint in ispath:
                    isx = iswaypoint[0]
                    isy = iswaypoint[1]
                    ixdept = idept[1]
                    iydept = idept[2]
                    distance = math.sqrt( math.pow(isx-ixdept,2.0)+math.pow(isy-iydept,2.0) ) #L2-norm
                    f_d_matrix.write("%d, " %distance)
            f_d_matrix.write("\n")
        #END
        f_d_matrix.close()

    def createDistanceMatrixStraightLineL2(self, dir_path_output):
        #create D(i,j) matrix based on L2-norm
        #waypoint_i to waypoint_j (depot,customer, or normal waypoint)
        f_d_matrix = open(dir_path_output+"distance_matrix_L2.csv", "w+")
        f_d_matrix.write("Number of Customers, %d\n" %self.num_cust)
        f_d_matrix.write("Number of Depots, %d\n" %self.num_dept)
        #write out header for matrix
        #TODO: header here...
        #Main Loop
        for idept in self.Depot_Loc:
            f_d_matrix.write("Depot-%d ," %idept[0])
            for icust in self.Cust_Loc:
                icx = icust[1]
                icy = icust[2]
                idx = idept[1]
                idy = idept[2]
                distance = math.sqrt( math.pow(icx-idx,2.0)+math.pow(icy-idy,2.0) ) #L2-norm
                f_d_matrix.write("%f," %distance)
            f_d_matrix.write("\n")
        #END
        f_d_matrix.close()