# crossing_helper.py

import sys
import csv

#------------------------------------------------

class Crosswaypoint_Helper():
    def __init__(self, sourceList=[], destList=[]):
        self.sourceList = sourceList
        self.destList = destList

    #methods ------------------------------------
    def readFromFile(self, dir_data_path):
        try:
            datafilestr = dir_data_path+"paths_s.txt"
            datafile = open(datafilestr,"r")
            reader = csv.reader(datafile)
            text = "" #clear and ready for new data
            for line in reader:
                try:
                    tmpLat = float(line[0].replace(" ",""))
                    tmpLon = float(line[1].replace(" ",""))
                    text += str(tmpLat)+","+str(tmpLon)+"\n"
                except:
                    print("Read CrossWaypoint: ERROR: "+str(line))
        except:
            print("Read CrossWaypoint: ERROR: file="+str(datafilestr))
        #end
        datafile.close()
        return text

    def straightLine(self, dir_path_output, new_data=False):
        open_mode = "w+"
        if(new_data): open_mode = "a+"
        f_path   = open(dir_path_output+"paths.txt", open_mode)
        f_path_s = open(dir_path_output+"paths_s.txt", open_mode)
        #crossing waypoints -- straight line paths from depot to customer
        Depot_Loc = self.sourceList
        Cust_Loc = self.destList
        for idept in Depot_Loc:
            for icust in Cust_Loc:
                #not same route check
                if( idept[3]!=icust[3] ):
                    continue
                #end not same route
                L = []
                # a x + b = c x + d           yc − yd = m (xc − xd) 
                # (a-c) x = (d-b)
                # x = (d-b)/(a-c)
                # y = a x + b
                #
                ixd = idept[1]
                iyd = idept[2]
                ixc = icust[1]
                iyc = icust[2]
                a = (iyc-iyd)/(ixc-ixd)
                b = iyd - a*ixd
                for jdept in Depot_Loc:
                    for jcust in Cust_Loc:
                        #initial skip
                        if( jdept[3]!=jcust[3] ):
                            continue #not same route check
                        if( idept[0]==jdept[0] or icust[0]==jcust[0] ):
                            continue #same starting and/or end points
                        #end init skip
                        jxd = jdept[1]
                        jyd = jdept[2]
                        jxc = jcust[1]
                        jyc = jcust[2]
                        c = (jyc-jyd)/(jxc-jxd)
                        d = jyd - c*jxd
                        #post-process skip                    
                        if( a == c ):
                            continue #parallel lines (no intersect in grid)
                        #end post skip
                        ix = (d-b)/(a-c)
                        iy = a*ix + b
                        #skip pts outside of environment
                        if( ix>max(ixd,ixc,jxd,jxc) or ix<min(ixd,ixc,jxd,jxc) or iy>max(iyd,iyc,jyd,jyc) or iy<min(iyd,iyc,jyd,jyc) ):
                            continue #outside of line segments
                        #end skip pts
                        L.append( (ix,iy, idept[0],jdept[0],icust[0],jcust[0]) ) #add waypoint(x,y) and id
                        f_path_s.write("%f,%f,%d,%d,%d,%d\n" %(ix,iy,idept[0],jdept[0],icust[0],jcust[0]))
                    #f_path_s.write("\n")
                #end
                for ipt in L:
                    for item in ipt:
                        f_path.write(str(item)+",")
                    f_path.write(";")
                f_path.write("\n")
        print("Straight Line Intersection File(1) = "+str(f_path))
        print("Straight Line Intersection File(2) = "+str(f_path_s))