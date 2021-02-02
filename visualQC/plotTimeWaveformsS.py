#!/usr/bin/env python

from obspy import read_inventory
import os, argparse, sys
from visualQC.graphicGenerator import PlotTimeWaveformsS, NameModel
from obspy import UTCDateTime
import configparser

"""
Example:
$ ./L2BnsplotSTimeWaveforms.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS --station LSV5A

onil@laut$./L2BnsplotSTimeWaveforms.py  /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A/AZBBA/SDS_corrected/SDS  --station AZBBA

Installed with pip:

$ plotTimeWaveformsS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS --station LSV5A --startTime  "2007-07-20T21:00:00" --endTime "2007-07-23T19:10:03"

$plotTimeWaveformsS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV6A/SDS_corrected/SDS --station LSV6A --startTime  "2007-07-21T15:00:00" --endTime "2007-07-24T18:40:48"

"""


def main():

    #default
    outDir = os.getcwd()
    outPrefix = ''
    outInfix = 'TimeWaveformsS.'
    outSuffix =''
    outFmt = 'jpeg'
    outModel= '%N.#S.#L.#C.TimeWaveformsS.'
    csvDir=os.getcwd()
    csvFileName = 'TimeWaveformsS.csv'
    startTime=None
    endTime=None
    eventTime=None
    duration=60
    sta="*"

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    
    parser = argparse.ArgumentParser(description='Provide waveforms of all (or a subset of) channels of a station (fournit graphe/courbe de réponse instrumentale, avec tous les canaux, pour une station). Fournit diagramme de séries temporelles pour chaque station, relativement à un événement sismique particulier (Doc Olivier)')
    parser.add_argument('iPath', metavar='INPUTDIR', help='<INPUTDIR> input file path / directory')
    parser.add_argument('--station', metavar='STACOD', required=True,  help='<STACOD> Required station code ')
    parser.add_argument("--output", required=False, help='<OUTPUT> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG, PNG, SVG)')
    #parser.add_argument("--model",  required=False, help='<MODEL> Optional model output file')
    parser.add_argument('--result', required=False,  help='<RESULT> Optional path to a CSV output file ')
    parser.add_argument("--startTime", metavar='START_TIME', required=True, help='<START_TIME> Optional starting time')
    parser.add_argument("--endTime",  metavar='END_TIME', required=False, help='<END_TIME> Optional end time')
    parser.add_argument("--duration",  metavar='SECONDCOUNT', required=False, type=int, help='<SECONDCOUNT> Optional number of second for each station waveform plot, this usually corresponds to the duration of a seismic event')

    args = parser.parse_args()

    if args.station:
        sta=args.station

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('TIMEWAVEFORMSS', 'RELIMAGEDIR')
            outInfix = config.get('TIMEWAVEFORMSS', 'OUTINFIX')
            outModel = config.get('TIMEWAVEFORMSS', 'NAMEMODEL')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None

    if args.outFormat:
        outFmt=args.outFormat
        print(outSuffix)
    else:
        if confExists:
            outFmt = config.get('ALLPLOTS', 'OUTFORMAT')   

    #if args.model:
        #print(args.model)

    if args.result:
        #print(args.result)
        csvAbsFileName=args.result
    else:
        if confExists:
            csvDir = config.get('TIMEWAVEFORMSS', 'CSVDIR')
            csvFileName = config.get('TIMEWAVEFORMSS', 'CSVFILENAME')
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

    if args.iPath:
        outNameModel = NameModel(outModel, outPrefix, outInfix, outSuffix)
        csvFieldNames=['station code', ' start time', ' end time', ' Absolute Path File']   
        grGenerator=PlotTimeWaveformsS(args.iPath, outDir, outNameModel, outFile, outFmt, station=sta, startTime=startTime, endTime=endTime, duration=duration, csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames )
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main() 

