#!/usr/bin/env python

from obspy import read_inventory
import os, argparse, sys
from visualQC.graphicGenerator import PlotInstrumentResponseC, NameModel
import configparser


"""
Example:
$./L3nsplotCInstrumentResponse.py /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/ --channel BDH

Installed by pip
$plotInstrumentResponseC /home/onil/IPGP2020/DocumentsTravail/Obs_Parcs/2007-.MOMAROBS/2007-2008.MOMAR_A/4G.#S.STATION.xml --channel BDH

"""


def main():

    # defaultvalue
    outDir=os.getcwd()
    outFmt = 'jpeg'
    outModel= '%N.#S.#L.%C.instrumentResponseC.'
    csvDir=os.getcwd()
    csvFileName = 'instrumentResponseC.csv'

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)


    parser = argparse.ArgumentParser(description='Provide plot of instrument response of a channel for all stations (fournit graphe/courbe de réponse instrumentale pour chaque canal, de code distinct, parmi toutes les stations)')
    parser.add_argument('iFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument('--channel', metavar='CHACOD', required=True,  help='<CHACOD> Required channel code ')
    parser.add_argument("--output", required=False, help='<OUTPUT> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')
    #parser.add_argument("--model",  required=False, help='<MODEL> Optional model output file')
    parser.add_argument('--result', required=False,  help='<RESULT> Required path to a CSV output file ')

    args = parser.parse_args()

    if args.channel:
        channel=args.channel
  
    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('INSTRESPONSEC', 'RELIMAGEDIR')
            outModel = config.get('INSTRESPONSEC', 'NAMEMODEL')
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
            csvDir = config.get('INSTRESPONSEC', 'CSVDIR')
            csvFileName = config.get('INSTRESPONSEC', 'CSVFILENAME')
        if not os.path.isdir(csvDir):
            os.makedirs(csvDir)
        csvAbsFileName=csvDir+csvFileName
  
    if args.iFile:
        outNameModel = NameModel(outModel)
        csvFieldNames=['channel code', ' Absolute Path File']   
        grGenerator=PlotInstrumentResponseC(args.iFile, outDir, outNameModel, outFile, outFmt, channel=channel, csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames )
        grGenerator.generate()
    
    
if __name__ == "__main__":
    main() 

