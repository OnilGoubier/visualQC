#!/usr/bin/env python

import argparse, os, configparser
from visualQC.graphicGenerator import PlotPPSDSC, NameModel
from obspy import UTCDateTime


"""
example:
$./L4nsplotCsPPSD.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A --station LSV5A --channel BHZ

$plotPPSDSC /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml --station LSV5A --channel BHZ --startTime  "2007-07-20T21:00:00" --endTime "2007-07-23T00:00:00"

$plotPPSDSC /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml --station LSV6A --channel BHZ --startTime  "2007-07-21T15:00:00" --endTime "2007-07-24T18:40:48"


"""

def main():

    #default
    outDir = os.getcwd()
    outFmt = 'jpeg'
    outModel= '%N.%S.#L.%C.PPSDSC.'
    csvDir=os.getcwd()
    csvFileName = 'PPSDSC.csv'
    ppsdDir = os.getcwd()
    ppsdModel= '%N.%S.#L.%C.PPSD.'
    ppsdFormat='npz'
    duration=0
    chan="*"
    sta="*"

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    parser = argparse.ArgumentParser(description='Provide graphical representation of the ppsd of a station (fournit diagramme probabiliste des Densités Spectrales de Puissance pour chaque canal, de code distinct, parmi toutes les stations)')
    parser.add_argument('iPath', metavar='INPUTDIR', help='<INPUTDIR> input SDS root directory path')
    parser.add_argument('iMetaFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument('--station', metavar='STACOD', required=False,  help='<STACOD> Optional station code ')
    parser.add_argument('--channel', metavar='CHACOD', required=False,  help='<CHACOD> Optional channel code ')
    parser.add_argument("--output", required=False, help='<OUTPUT> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')
    #parser.add_argument("--model",  required=False, help='<MODEL> Optional model output file')
    parser.add_argument('--result', required=False,  help='<RESULT> Required path to a CSV output file ')
    parser.add_argument("--startTime", metavar='START_TIME', required=True, help='<START_TIME> Required starting time')
    parser.add_argument("--endTime",  metavar='END_TIME', required=True, help='<END_TIME> Optional end time')
    parser.add_argument("--duration",  metavar='SECONDCOUNT', required=False, type=int, help='<SECONDCOUNT> Optional number of second for each station waveform plot, this usually corresponds to the duration of a seismic event')

    args = parser.parse_args()

    if args.station:
        sta=args.station

    if args.channel:
        chan=args.channel

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('PPSDSC', 'RELIMAGEDIR')
            outModel = config.get('PPSDSC', 'NAMEMODEL')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None

    if args.outFormat:
        outFormat=args.outFormat
        print(outSuffix)
    else:
        if confExists:
            outFormat = config.get('ALLPLOTS', 'OUTFORMAT')   

    if args.result:
        #print(args.result)
        csvAbsFileName=args.result
    else:
        if confExists:
            csvDir = config.get('PPSDSC', 'CSVDIR')
            csvFileName = config.get('PPSDSC', 'CSVFILENAME')
        if not os.path.isdir(csvDir):
            os.makedirs(csvDir)
        csvAbsFileName=csvDir+csvFileName

    if args.startTime:
        startTime=UTCDateTime(args.startTime)
        #print(startTime)
    if args.endTime:
        endTime=UTCDateTime(args.endTime)
        #print(endTime)
    if args.duration:
        duration=args.duration
        #print(duration)
        endTime=startTime+duration

    if args.iMetaFile:
        iMetaFile=args.iMetaFile

    if confExists:
        ppsdDir = config.get('PPSD', 'PPSDDIR')
        ppsdModel=config.get('PPSD', 'NAMEMODEL')
        if not os.path.isdir(ppsdDir):
            os.makedirs(ppsdDir)
        ppsdFormat = config.get('PPSD', 'PPSDFORMAT')

    if args.iPath:
        outNameModel = NameModel(outModel)
        ppsdNameModel = NameModel(ppsdModel)
        csvFieldNames=['station code', 'channel code', ' Absolute Path File']  
        grGenerator=PlotPPSDSC(args.iPath, iMetaFile, outDir, outNameModel, outFile, outFormat, station=sta, channel=chan, startTime=startTime, endTime=endTime, duration=duration, csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames, ppsdDir=ppsdDir, ppsdNameModel=ppsdNameModel, ppsdFormat=ppsdFormat)
        grGenerator.generate()

if __name__ == "__main__":
    main()	

