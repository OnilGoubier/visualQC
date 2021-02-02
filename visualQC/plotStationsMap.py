#!/usr/bin/env python

"""
Provide a map of all stations.
Can use one xml file containing metadata of all stations
"""

from obspy import read_inventory
import os, argparse
from visualQC.graphicGenerator import PlotStationsMap, NameModel
import configparser

"""
example:

$ ./plotStationsMap.py /stationXML/directory/filename.xml

$ ./plotStationsMap.py /stationXML/directory/filename.xml --output myStationMap.jpeg

If the package is installed using pip
$ plotStationsMap /stationXML/directory/filename.xml

"""

def main():

    # defaultvalue
    outDir=os.getcwd()
    outPrefix = ''
    outInfix = 'StaMap.'
    outSuffix =''
    outFmt = 'jpeg'
    outModel= '%N.#S.#L.#C.StationsMap.'

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
            outModel = config.get('STATIONMAP', 'NAMEMODEL')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None

    if args.outFormat:
        outFmt=args.outFormat
    else:
        if confExists:
            outFmt = config.get('ALLPLOTS', 'OUTFORMAT')
    
    if args.iFile:
        outNameModel = NameModel(outModel, outPrefix, outInfix, outSuffix)   
        grGenerator=PlotStationsMap(args.iFile, outDir, outNameModel, outFile, outFmt)
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main()  
