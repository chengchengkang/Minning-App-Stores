import urllib2
from elementtree import ElementTree
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import csv

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android_2=db_android.androidAppsClusterTest

        
def _getCollection():
     clusters=[]
     clusterIDs=[]
     count=0
     csvfile = "clusterStatsAndroidNew.csv"
     
     for post in collection_android_2.find(no_cursor_timeout=True):
             count=count+1
             print "Apps processed:"+str(count)
             #print count
             title=(post['title'])
             devName=(post['developer_name'])
             category=(post['category'])
             clusterID=post['android_clusterID']
             clusterID2=clusterID.replace("\\","")
             #print clusterID2
             #print clusterID
             #print clusterIDs
             if clusterID not in clusterIDs:
                clusterIDs.append(clusterID)
                clusterIDs.append(clusterID2)

                appsPerCluster=collection_android_2.count({'android_clusterID':clusterID})
                appsPerCluster2=collection_android_2.count({'android_clusterID':clusterID2})
                if appsPerCluster==appsPerCluster2:
                    totAppsPerCluster=appsPerCluster
                else:
                    totAppsPerCluster=appsPerCluster+appsPerCluster2    

                #totAppsPerCluster=appsPerCluster+appsPerCluster2
                clusters.append({'clusterName':clusterID2, 'AppsInCluster':totAppsPerCluster})
                #print appsPerCluster

                

     with open(csvfile, "w") as output:
         writer = csv.writer(output, lineterminator='\n')
         writer.writerow(["cluster Name", "Number of Apps in Cluster"])
         for cluster in clusters:
            cluster_Name=cluster['clusterName']
            writer.writerow([cluster_Name.encode('utf-8').strip(), cluster['AppsInCluster']])            




if __name__ == '__main__':
   _getCollection()


