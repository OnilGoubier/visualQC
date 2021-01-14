#!/usr/bin/env python

from obspy import read_inventory
import os, argparse
from graphicGenerator import L1_nsplot_DataAvailability
import configparser

"""
example:
onil@dKelana: ./plotDataAvailability.py ~/IPGP2020/DocumentsTravail/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A/LSV5A

onil@dKelana: ./plotDataAvailability.py ~/IPGP2020/DocumentsTravail/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A --format mseed --output L1_nsplot_DataAvailability_mseed.jpeg

onil@laut: ./plotDataAvailability.py /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A/AZBBA

onil@laut: ./plotDataAvailability.py /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A --format mseed

"""

def main():

    #imagesDir='../Images/'
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    config.read(config_filename)

    startTime=None
    endTime=None
    eventTime=None
    parser = argparse.ArgumentParser(description='Provide data availability of all stations of the network, fournir la disponibilité de données des stations du réseau)')
    parser.add_argument('iPath', metavar='INPUTDIR', help='<INPUTDIR> input file path / directory')
    parser.add_argument("--format", required=False, help='<FORMAT> Optional if using format MSEED')
    parser.add_argument("--output", metavar='OUTPUTFILE', required=False, help='<OUTPUTFILE> Optional output file name')
    parser.add_argument("--startTime", metavar='START_TIME', required=False, help='<START_TIME> Optional starting time')
    parser.add_argument("--endTime", metavar='END_TIME', required=False, help='<END_TIME> Optional end time')
    parser.add_argument("--eventTime", metavar='EVENT_TIME', required=False, help='<EVENT_TIME> Optional event time')
    args = parser.parse_args()

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
        #outFile=imagesDir+args.output
    else:
        imagesDir = config.get('DTAVAILABILITY', 'RELIMAGEDIR')
        if not os.path.isdir(imagesDir):
            os.makedirs(imagesDir)
        #outFile=imagesDir+'L1_nsplot_StationMaps.jpeg'
        outSuffix = config.get('DTAVAILABILITY', 'OUTSUFFIX')
        outDir=imagesDir
        print(imagesDir)
        outFile = None
        #outFile=imagesDir+'L1_nsplot_DataAvailability_withMseed.jpeg'
   
    if args.iPath:
        iDir = args.iPath
    if args.format:
        iDir=iDir+'/*/miniseed_basic/*.mseed'
    else:
        iDir=iDir+'/SDS_corrected/'
    if args.startTime:
        startTime=args.startTime
    if args.endTime:
        endTime=args.endTime
    if args.eventTime:
        eventTime=args.eventTime
  
    grGenerator=L1_nsplot_DataAvailability(iDir, outFile, startTime, endTime, eventTime)
    grGenerator.generate()
    
    
if __name__ == "__main__":
    main()  
