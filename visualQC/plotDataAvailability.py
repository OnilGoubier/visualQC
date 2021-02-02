#!/usr/bin/env python

from obspy import read_inventory
import os, argparse
from visualQC.graphicGenerator import PlotDataAvailability, NameModel
import configparser

"""
example:
onil@dKelana: ./plotDataAvailability.py ~/IPGP2020/DocumentsTravail/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A/LSV5A

onil@dKelana: ./plotDataAvailability.py ~/IPGP2020/DocumentsTravail/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A --format mseed --output L1_nsplot_DataAvailability_mseed.jpeg

onil@laut: ./plotDataAvailability.py /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A/AZBBA

onil@laut: ./plotDataAvailability.py /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A --format mseed

Install with pip:
onil@dKelana: plotDataAvailability ~/IPGP2020/DocumentsTravail/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A/LSV5A

"""

def main():

    #default
    outDir= os.getcwd()
    outPrefix = ''
    outInfix = 'DataAvailability.'
    outSuffix =''
    outFmt = 'jpeg'
    mseedDirBaseName = '/*/miniseed_basic/*.mseed'
    sdsDirBaseName = '/SDS_corrected/'
    startTime=None
    endTime=None
    eventTime=None

    #avec config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    parser = argparse.ArgumentParser(description='Provide data availability of all stations of the network, fournir la disponibilité de données des stations du réseau)')
    parser.add_argument('iPath', metavar='INPUTDIR', help='<INPUTDIR> input file path / directory')
    parser.add_argument("--inFormat", required=False, help='<FORMAT> Optional if using format MSEED')
    parser.add_argument("--output", metavar='OUTPUTFILE', required=False, help='<OUTPUTFILE> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')
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
    else:
        if confExists:
            outDir = config.get('DTAVAILABILITY', 'RELIMAGEDIR')
            outInfix = config.get('DTAVAILABILITY', 'OUTINFIX')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None
   
    if args.iPath:
        iDir = args.iPath

    if args.inFormat:
        if confExists:
            mseedDirBaseName = config.get('DTAVAILABILITY', 'MSEEDIFILES')
        iDir=iDir+'/'+mseedDirBaseName
    else:
        if confExists:
            sdsDirBaseName = config.get('DTAVAILABILITY', 'SDSIDIRBASENAME')
        iDir=iDir+'/'+sdsDirBaseName

    if args.outFormat:
        outFmt=args.outFormat
    else:
        if confExists:
            outFmt = config.get('ALLPLOTS', 'OUTFORMAT')

    if args.startTime:
        startTime=args.startTime
    if args.endTime:
        endTime=args.endTime
    if args.eventTime:
        eventTime=args.eventTime

    outNameModel = NameModel(outPrefix, outInfix, outSuffix)
    grGenerator=PlotDataAvailability(iDir, outDir, outNameModel, outFile, outFmt, startTime, endTime, eventTime)
    grGenerator.generate()
    
    
if __name__ == "__main__":
    main()  
