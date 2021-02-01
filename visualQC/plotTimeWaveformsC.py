#!/usr/bin/env python

from obspy import read_inventory
import os, argparse
from visualQC.graphicGenerator import PlotTimeWaveformsC, NameModel
from obspy import UTCDateTime
import configparser

"""
example:
onil@laut$./plotTimeWaveformsC.py  /media/onil/NodeA/FileStore-in/2007-.MOMAROBS/2007-2008.MOMAR_A/AZBBA/SDS_corrected/SDS /home/onil/WorkingDocuments/DATA/NodeA/FileStore-in/2007-MOMAROBS/2007-2008.MOMAR_A/MetaData --station AZBBA --channel BHZ --startTime  "2008-03-02T00:19:59" --endTime "2008-03-02T00:23:59" --outUnit "DISP"

onil@dKelana$ ./plotTimeWaveformsC.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A --channel BDH --startTime  "2007-07-20T21:00:00" --endTime "2007-07-23T19:10:03"

Installed with pip:
$plotTimeWaveformsC /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/LSV5A/SDS_corrected/SDS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml --channel BDH --startTime  "2007-07-20T21:00:00" --endTime "2007-07-23T19:10:03" --removeResponse False

"""

def main():

    #default
    outDir = '.'
    outPrefix = ''
    outInfix = 'timeWaveformsC.'
    outSuffix =''
    outFmt = 'jpeg'
    csvDir='.'
    csvFileName = 'timeWaveformsC.csv'

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    startTime=None
    endTime=None
    eventTime=None
    duration=60
    sta="*"

    parser = argparse.ArgumentParser(description='Provide waveforms of a channel for all stations (fournit graphe/courbe de series temporelles pour un canal de toutes les stations)')
    parser.add_argument('iPath', metavar='INPUTPATH', help='<INPUTPATH> input file path / directory')
    #parser.add_argument('iXMLPath', metavar='INPUTXMLPATH', help='<INPUTXMLPATH> input XML file path / directory')
    parser.add_argument('iMetaFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument('--station', metavar='STACOD', required=False,  help='<STACOD> Optional station code ')
    parser.add_argument('--channel', metavar='CHACOD', required=True,  help='<CHACOD> Required channel code ')
    parser.add_argument("--output", required=False, help='<OUTPUT> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG or  PNG)')
    #parser.add_argument("--model",  required=False, help='<MODEL> Optional model output file')
    parser.add_argument('--result', required=False,  help='<RESULT> Required path to a CSV output file ')
    parser.add_argument("--startTime", metavar='START_TIME', required=True, help='<START_TIME> Optional starting time')
    parser.add_argument("--endTime",  metavar='END_TIME', required=False, help='<END_TIME> Optional end time')
    parser.add_argument("--duration",  metavar='SECONDCOUNT', required=False, type=int, help='<SECONDCOUNT> Optional number of second for each station waveform plot, this usually corresponds to the duration of a seismic event')
    parser.add_argument('--outUnit', metavar='OUTUNIT', required=False,  help='<OUTUNIT> Optional output unit. The valid values are: DISP, VEL or ACC. The fault value is VEL')
#    parser.add_argument('--removeResponse', metavar='REMRESP', required=False, type=bool, help='<REMRESP> Optional remove response, True of False. The dafault value is True. Deconvolve instrument response.')
    '''remResp_parser = parser.add_mutually_exclusive_group(required=False)
    remResp_parser.add_argument('--removeResponse', dest='removeResponse', action='store_true')
    remResp_parser.add_argument('--no-removeResponse', dest='removeResponse', action='store_false')
    parser.set_defaults(removeResponse=True)'''
    parser.add_argument('--no-removeResponse', default=False, action="store_true", help=' Optional no remove response, not to deconvolve instrument response. The default value is False.')



    args = parser.parse_args()

    if args.outUnit:
        outUnit=args.outUnit
    else:
        outUnit="VEL"

    if args.no_removeResponse:
        remResp = not args.no_removeResponse
    else:
        remResp = True

    print(remResp)

    #outFile = outFile+"_"+outUnit

    if args.station:
        sta=args.station
        #print(sta)
        #if not args.output:
            #outFile=outFile+'_'+sta #Images directory should have been created

    if args.channel:
        chan=args.channel
        #print(chan)
        #if not args.output:
            #outFile=outFile+'_'+chan

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('TIMEWAVEFORMSC', 'RELIMAGEDIR')
            #outSuffix = config.get('TIMEWAVEFORMSS', 'OUTSUFFIX')
            outInfix = config.get('TIMEWAVEFORMSC', 'OUTINFIX')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None

    if args.outFormat:
        outFormat=args.outFormat
        print(outSuffix)
    else:
        if confExists:
            outFormat = config.get('ALLPLOTS', 'OUTFORMAT')   

    #if args.model:
        #print(args.model)

    if args.result:
        #print(args.result)
        csvAbsFileName=args.result
    else:
        if confExists:
            csvDir = config.get('TIMEWAVEFORMSC', 'CSVDIR')
            csvFileName = config.get('TIMEWAVEFORMSC', 'CSVFILENAME')
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

    if args.iPath:
        outNameModel = NameModel(outPrefix, outInfix, outSuffix)
        csvFieldNames=['channel code', ' start time', ' end time', ' Absolute Path File']   
        grGenerator=PlotTimeWaveformsC(args.iPath, iMetaFile, outDir, outNameModel, outFile, outFormat, station=sta, channel=chan, startTime=startTime, endTime=endTime, duration=duration, csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames, outUnit=outUnit, removeResponse=remResp )
        grGenerator.generate()

if __name__ == "__main__":
    main() 
