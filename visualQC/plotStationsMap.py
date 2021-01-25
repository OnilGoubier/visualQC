#!/usr/bin/env python

"""
Provide a map of all stations.
Can use one xml file containing metadata of all stations
"""

from obspy import read_inventory
import os, argparse
from graphicGenerator import PlotStationsMap, NameModel
import configparser

"""
example:

$ ./plotStationsMap.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.STATION.xml

$ ./plotStationsMap.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.STATION.xml --output myStationMap.jpeg

If the package is installed using pip
$ plotStationsMap /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml
"""

def main():

    # defaultvalue
    outDir='.'
    outPrefix = ''
    outInfix = 'StaMap.'
    outSuffix =''
    outFmt = 'jpeg'

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    description='Provide a map of all stations (fournit carte    géographique des stations du réseau)'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('iFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument("--output", metavar='OUTPUTFILE', required=False, help='<OUTPUTFILE> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')

    args = parser.parse_args()

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('STATIONMAP', 'RELIMAGEDIR')
            outInfix = config.get('STATIONMAP', 'OUTINFIX')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None

    if args.outFormat:
        outFmt=args.outFormat
    else:
        if confExists:
            outFmt = config.get('ALLPLOTS', 'OUTFORMAT')
    
    if args.iFile:
        outNameModel = NameModel(outPrefix, outInfix, outSuffix)   
        grGenerator=PlotStationsMap(args.iFile, outDir, outNameModel, outFile, outFmt)
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main()  
