#!/usr/bin/env python

"""
Provide a map of all stations.
Can use one xml file containing metadata of all stations
"""

from obspy import read_inventory
import os, argparse
from graphicGenerator import L1_nsplot_StationMaps
import configparser

"""
example:

$ ./plotStationsMap.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.STATION.xml

$ ./plotStationsMap.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.STATION.xml --output 4G.StationMap.jpeg

"""

def main():

    #imagesDir='Images/StationMap/'
    #config.read('config/config.ini')
    #print(os.path.realpath(__file__))
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    config.read(config_filename)

    description='Provide a map of all stations (fournit carte    géographique des stations du réseau)'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('iFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted')
    parser.add_argument("--output", metavar='OUTPUTFILE', required=False, help='<OUTPUTFILE> Optional output file name')
    args = parser.parse_args()

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        imagesDir = config.get('STATIONMAP', 'RELIMAGEDIR')
        if not os.path.isdir(imagesDir):
            os.makedirs(imagesDir)
        #outFile=imagesDir+'L1_nsplot_StationMaps.jpeg'
        outSuffix = config.get('STATIONMAP', 'OUTSUFFIX')
        outDir=imagesDir
        print(imagesDir)
        outFile = None
    
    if args.iFile:   
        grGenerator=L1_nsplot_StationMaps(args.iFile, outFile, outDir, outSuffix)
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main()  
