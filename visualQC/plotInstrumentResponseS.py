#!/usr/bin/env python

from obspy import read_inventory
import os, argparse, sys
from visualQC.graphicGenerator import PlotInstrumentResponseS, NameModel
import configparser


"""
Example:
$./L2nsplotSInstrumentResponse.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A --station AZBBA

Installed by pip
$plotInstrumentResponseS /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml --station AZBBA

"""


def main():

    # defaultvalue
    outDir='.'
    outPrefix = ''
    outInfix = 'instrumentResponseS.'
    outSuffix =''
    outFmt = 'jpeg'

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)

    parser = argparse.ArgumentParser(description='Provide plots of instrument response with all channels for one station (fournit graphe/courbe de réponse instrumentale, avec tous les canaux, pour une station)')
    parser.add_argument('iFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument("--output", metavar='OUTPUTFILE', required=False, help='<OUTPUTFILE> Optional output file name')
    parser.add_argument('--station', metavar='STACOD', help='<STACOD> Optional code stationn required when there are more than one stationXML file', required=True)
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')
    parser.add_argument('--result', required=False,  help='<RESULT> Required path to a CSV output file ')

    args = parser.parse_args()

    if args.station:
        station=args.station

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('INSTRESPONSES', 'RELIMAGEDIR')
            outInfix = config.get('INSTRESPONSES', 'OUTINFIX')
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        outFile = None
 
    if args.outFormat:
        outFmt=args.outFormat
    else:
        if confExists:
            outFmt = config.get('ALLPLOTS', 'OUTFORMAT')

    if args.result:
        print(args.result)
        csvAbsFileName=args.result
    else:
        if confExists:
            csvDir = config.get('INSTRESPONSES', 'CSVDIR')
            csvFileName = config.get('INSTRESPONSES', 'CSVFILENAME')
        if not os.path.isdir(csvDir):
            os.makedirs(csvDir)
        csvAbsFileName=csvDir+csvFileName 
  
    if args.iFile:
        outNameModel = NameModel(outPrefix, outInfix, outSuffix)
        csvFieldNames=['station code', ' Absolute Path File']     
        grGenerator=PlotInstrumentResponseS(args.iFile, outDir, outNameModel, outFile, outFmt, station=station, csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames)
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main() 
