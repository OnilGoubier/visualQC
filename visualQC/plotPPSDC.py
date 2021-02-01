#!/usr/bin/env python

from visualQC.graphicGenerator import PlotPPSDC, NameModel
import os
import argparse, configparser


def main():

    #default
    outDir = os.getcwd()
    outPrefix = ''
    outInfix = 'PPSDC.'
    outSuffix =''
    outFormat = 'jpeg'
    csvDir=os.getcwd()
    csvFileName = 'PPSDC.csv'
    ppsdDir = os.getcwd()
    ppsdPrefix=''
    ppsdInfix='PPSD.'
    ppsdSuffix=''
    ppsdFormat='npz'

    # config
    config_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                               'config', 'config.ini')
    config = configparser.ConfigParser()                                     
    confExists = config.read(config_filename)
    
    parser = argparse.ArgumentParser(description='Provide graphical representation of the ppsd of a channel for all stations (fournit diagramme probabiliste des Densités Spectrales de Puissance pour chaque canal, de code distinct, parmi toutes les stations)')
    parser.add_argument('iMetaFile', metavar='INPUTMETAFILE', help='<INPUTMETAFILE> input file, wildcards accepted (please write the name with wildcards * between quotes, ex. "*.xml")')
    parser.add_argument('channel', metavar='CHANNELCODE', help='<CHANNELCODE> channel code required')
    parser.add_argument("--output", required=False, help='<OUTPUTFILE> Optional output file name')
    parser.add_argument("--outFormat",  metavar='FMTID', required=False, help='<FMTID> Optional format of output file (JPEG ro PNG)')
    parser.add_argument('--result', required=False,  help='<RESULT> Required path to a CSV output file ')

    args = parser.parse_args()

    if args.channel:
        channel = args.channel

    if args.output:
        outDir = os.path.dirname(args.output)
        if not os.path.isdir(outDir):
            if outDir != '': 
                os.makedirs(outDir)
        outFile=args.output
    else:
        if confExists:
            outDir = config.get('PPSDC', 'RELIMAGEDIR')
            outInfix = config.get('PPSDC', 'OUTINFIX')
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
            csvDir = config.get('PPSDC', 'CSVDIR')
            csvFileName = config.get('PPSDC', 'CSVFILENAME')
        if not os.path.isdir(csvDir):
            os.makedirs(csvDir)
        csvAbsFileName=csvDir+csvFileName

    if args.iMetaFile:
        iMetaFile=args.iMetaFile

    if confExists:
        ppsdDir = config.get('PPSD', 'PPSDDIR')
        ppsdInfix=config.get('PPSD', 'PPSDINFIX') 
        if not os.path.isdir(ppsdDir):
            os.makedirs(ppsdDir)
        ppsdFormat = config.get('PPSD', 'PPSDFORMAT')

    outNameModel = NameModel(outPrefix, outInfix, outSuffix)
    ppsdNameModel = NameModel(ppsdPrefix, ppsdInfix, ppsdSuffix)
    csvFieldNames=['channel code', ' Absolute Path File']  
    grGenerator=PlotPPSDC(iMetaFile, outDir, outNameModel, outFile, outFormat, channel=channel,  csvFileName=csvAbsFileName, csvFieldNames=csvFieldNames, ppsdDir=ppsdDir, ppsdNameModel=ppsdNameModel, ppsdFormat=ppsdFormat)
    grGenerator.generate()

if __name__ == "__main__":
    main()	

