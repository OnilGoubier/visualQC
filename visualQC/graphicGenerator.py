
from abc import ABC, abstractmethod
from visualQC.dirAndFiles import listOfFilesWithAbsName
from obspy.clients.filesystem.sds import Client
from obspy import read_inventory
from obspy import read
from obspy.io.xseed import Parser
from obspy.signal import PPSD
import os
import csv
import re
import matplotlib.pyplot as plt
import numpy as np

NOISE_MODEL_FILE = os.path.join(os.path.dirname(__file__),
                                "data", "noise_models.npz")
"""
The following functions (get_nlnm() and get_nhnm()) are the copy of the functions of obspy
in the spectral_estimation.py 
"""

def get_nlnm():
    """
    Returns periods and psd values for the New Low Noise Model.
    For information on New High/Low Noise Model see [Peterson1993]_.
    """
    data = np.load(NOISE_MODEL_FILE)
    periods = data['model_periods']
    nlnm = data['low_noise']
    return (periods, nlnm)


def get_nhnm():
    """
    Returns periods and psd values for the New High Noise Model.
    For information on New High/Low Noise Model see [Peterson1993]_.
    """
    data = np.load(NOISE_MODEL_FILE)
    periods = data['model_periods']
    nlnm = data['high_noise']
    return (periods, nlnm)

class NameModel():

    """
    Le model de nom d'un fichier :
	prefix + infix + suffix + format

    (si il ne devait y avoir, de façon certaine, qu'un station code dans le
    graphique, ce code apparaitrait tel quel dans le nom de fichier à la
    place du symbole "#S")

    L'absence de #L et #C dans le nom de fichier indique que les informations
    de location et channel codes ne sont pas présentes dans le graphique.

    (concernant les informations qui peuvent être présentes dans les
    différents types de graphique, l'ordre à respecter dans les modèles
    de nom de fichier serait : NETCODE, STACODE, LOCCODE, CHACODE)

    ex. 4G.#S.#L.AZBBA.TimeWaveformsC.jpeg
    prefix = 4G.#S.#L.AZBBA
    infix = TimeWaveformsC
    suffix = ''
    format = .jpeg

    """

    def __init__(self, prefix='', infix='', suffix=''):
        self.prefix=prefix
        self.infix=infix
        self.suffix=suffix

    def setPrefix(self, aPrefix):
        self.prefix=aPrefix

    def setInfix(self, anInfix):
        self.infix=anInfix

    def setSuffix(self, aSuffix):
        self.suffix=aSuffix    

    def generateName(self):
        return self.prefix + self.infix + self.suffix

class GraphicGenerator(ABC):

    def __init__(self, outputDir=None, outModel=None, outputFile=None, outputFormat=None):
        self.outputDir = outputDir
        self.outputModel = outModel
        self.outputFile=outputFile
        self.outputFormat=outputFormat

    def generateName(self):

        outModel = self.outputModel
        outFile = outModel.generateName() + self.outputFormat
        if self.outputDir != None:
            outFile = self.outputDir+outFile
        return outFile

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class MetadataGraphicGenerator(GraphicGenerator):

    #input file extension
    extension='.xml'
    iXMLFiles=[]

    def __init__(self, iMetaDataDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None):
        super().__init__(outputDir, outModel, outputFile, outputFormat)
        self.iMetaDataDir=iMetaDataDir
        #print("metadata dir: " + iMetaDataDir)
        #self.inventory=read_inventory(self.iMetaDataDir,'STATIONXML')

    def getInputFile(self, station=None):
        """ return an xml format input file with absolut path, or an absolute path name with *.xml, for a number of stations. Deprecated !!!"""

        
        self.iXMLFiles=listOfFilesWithAbsName(self.iMetaDataDir, self.extension)
        #print(self.iXMLFiles)
        #print("getInputfile station:", station)
        if not self.iXMLFiles:
            print("No xml station file in the directory")
        else:
            if(len(self.iXMLFiles)>1):
                if station:
                    for fn in self.iXMLFiles:
                        if (os.path.base(fn).rfind(station) >= 0):
                            inXMLFile=fn
                            #print("inXMLFile : ", inXMLFile)		
                else:
                    inXMLFile=self.inputDir+'/*'+self.extension			
		
            else:
                inXMLFile=self.inputDir+self.iXMLFiles[0]
        return inXMLFile


    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class TimeBasedGraphicGenerator(GraphicGenerator):

    def __init__(self, inputDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None, startTime=None, endTime=None):
        super().__init__(outputDir, outModel,  outputFile, outputFormat)
        #GraphicGenerator.__init__(outputDir, outModel,  outputFile, outputFormat)
        self.inputDir=inputDir
        self.startTime=startTime
        self.endTime=endTime

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class EventBasedGraphicGenerator(TimeBasedGraphicGenerator):

    def __init__(self, inputDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None, startTime=None, endTime=None, eventTime=None):
        super().__init__(inputDir, outputDir, outModel, outputFile, outputFormat, startTime, endTime)
        self.eventTime=eventTime

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class DurationBasedGraphicGenerator(TimeBasedGraphicGenerator):

    def __init__(self, inputDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None, startTime=None, endTime=None, duration=None):
        super().__init__(inputDir, outputDir, outModel,  outputFile, outputFormat, startTime, endTime)
        self.duration=duration

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class MeasuredDataGraphicGenerator(DurationBasedGraphicGenerator):

    net="*"
    sta="*"
    loc="*"
    chan="*"

    def __init__(self, inputDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None):
        super().__init__(inputDir, outputDir, outModel,  outputFile, outputFormat, startTime, endTime, duration)
        self.iDataDir=inputDir
        self.sta=station
        self.chan=channel

    def isHydrophone(self):
        if re.match('..H', self.chan) != None:
            #self.isHydrophone = True
            return True
        else:
            #self.isHydrophone = False
            return False            

    #input from SDS file
    def getStream(self):
        client = Client(self.iDataDir)
        #print(self.sta)
        #print(self.iDataDir)
        #print(self.startTime)
        #print(self.endTime)
        return client.get_waveforms(self.net, self.sta, self.loc, self.chan, self.startTime, self.endTime)

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"


class GraphicMetaData:
    """
    Output meta data in a CSV file
    """

    def __init__(self, csvFileName=None, csvFieldNames=None):
        self.csvFileName=csvFileName
        self.csvFieldNames=csvFieldNames

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

    def  generateCSV(self, data):

        if os.path.exists(self.csvFileName):
            with open(self.csvFileName, 'a') as csvfile:
                mywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                mywriter.writerow(data)
        else: 
            with open(self.csvFileName, 'w', newline='') as csvfile:
                mywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                mywriter.writerow(self.csvFieldNames)
                mywriter.writerow(data) 

class PlotStationsMap(MetadataGraphicGenerator):


    def generate(self):
        """
        Generate graphic stations on a map
        """

        #inFile = self.getInputFile()
        inFile =self.iMetaDataDir
        inv= read_inventory(inFile,'STATIONXML')
        outFile = self.outputFile
        #print(inv[0].code)
        #print(self.outSuffix)
        if  outFile == None:
            self.outputModel.setPrefix(inv[0].code+'.')
            outFile = self.generateName()
        print('Generate image: '+outFile)
        inv.plot(projection="local", resolution="i", outfile=outFile)

class PlotDataAvailability(EventBasedGraphicGenerator):

    command='obspy-scan'

    def generate(self):
        """
        Generate a plot of data availability
        """

        self.command=self.command+' '+self.inputDir
        if self.startTime:
            self.command=self.command+' --start-time '+self.startTime
        if self.endTime:
            self.command=self.command+' --end-time '+self.endTime
        if self.eventTime:
            self.command=self.command+' --event-time '+self.eventTime

        outFile = self.outputFile
        if  outFile == None:
            outFile = self.generateName()
        self.command=self.command+' --output '+outFile
        #print(self.command)
        print('Generate image: '+outFile)
        os.system(self.command)

class PlotInstrumentResponseS(MetadataGraphicGenerator, GraphicMetaData):
    
    station = ""

    def __init__(self, inputDir, outputDir=None, outputModel=None, outputFile=None, outputFormat=None, station="", csvFileName="", csvFieldNames=[]):
        super().__init__(inputDir, outputDir, outputModel, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.station=station

    def generate(self):
        """
        Generate graphic of instrument response with all channels for a station
        """

        #inFile = self.getInputFile(self.station)
        inFile =self.iMetaDataDir

        inv = read_inventory(inFile,'STATIONXML')
        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(inv[0].code+'.'+self.station+'.')
            outFile = self.generateName()
                
        sta = inv[0].select(station=self.station)[0]
        print('Generate image: '+outFile)
        sta.plot(0.001, output="VEL", outfile=outFile)
        self.generateCSV([self.station, os.path.abspath(outFile)])

class PlotInstrumentResponseC(MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, outputDir=None, outputModel=None, outputFile=None, outputFormat=None, channel="", csvFileName="", csvFieldNames=[]):
        MetadataGraphicGenerator.__init__(self,inputDir, outputDir, outputModel, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.channel=channel

    def generate(self):

        #print("InputDir:"+self.inputDir)
        #print(self.extension)
        #inFile = self.getInputFile()
        inFile =self.iMetaDataDir
        inv = read_inventory(inFile,'STATIONXML')
        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(inv[0].code+'.#S.#L.'+self.channel+'.')
            outFile = self.generateName()


        inv =inv.select(station='*', channel=self.channel)	
        #inv.plot_response(0.001, outfile=self.outputFile, label_epoch_dates=True)
        print('Generate image: '+outFile)
        inv.plot_response(0.001, outfile=outFile)
        self.generateCSV([self.channel, os.path.abspath(outFile)])


class  PlotTimeWaveformsS(MeasuredDataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, outputDir=None, outModel=None, outputFile=None, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[]):

        MeasuredDataGraphicGenerator.__init__(self,inputDir, outputDir, outModel, outputFile, outputFormat, station, channel, startTime, endTime, duration)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        #self.outInfix = outInfix

    """def generateName(self):

        # Olivier comments : Des informations temporelles pourraient être ajoutées :
        # "<NETCODE>.<#STACODE>.<LOCCODE>.#C.<TIMERANGE>.STimeWaveforms.jpeg"
        # sous la forme : "yyyymmddThhmmss-yyyymmddThhmmss"
        # (année, mois et jour séparés, par le symbole "T", de heure, minute et seconde)

        outModel = self.outputModel
        outModel.setPrefix(self.sta+'.')
        outFile = outModel.generateName() + self.outputFormat
        #outFile = self.sta + self.outInfix + self.outFormat
        if self.outputDir != None:
            outFile = self.outputDir+outFile
        return outFile"""

    def generate(self):
        """
        Provide waveforms of all (or a subset of) channels of a station
        Fournir des graphes/courbe de series temporelles, avec tous les canaux, pour une station.      
        Fournir diagramme de séries temporelles pour chaque station, 
        relativement à un événement sismique particulier (Doc Olivier)
        """

        st = self.getStream()
        #print(st)

        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(self.sta+'.')
            outFile = self.generateName()

        print('Generate image: '+outFile)
        st.plot(outfile=outFile, equal_scale = False)
        #st.plot(outfile=self.outputFile)
        self.generateCSV([self.sta, self.startTime, self.endTime, os.path.abspath(outFile)])


class PlotTimeWaveformsC(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iMetaFile, outputDir=None, outputModel=None, outputFile=None, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[], outUnit="VEL", removeResponse=True):
        MeasuredDataGraphicGenerator.__init__(self,inputDir, outputDir, outputModel, outputFile, outputFormat, station, channel, startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iMetaFile, outputDir, outputModel, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.outUnit=outUnit
        self.removeResponse=removeResponse

    def generate(self):
        """
        Provide plots of waveform of the same channel of all stations 
        Fournir graphes/courbes de réponse instrumentale, avec tous les canaux, pour une station)
        """

        inFile =self.iMetaDataDir
        print('channel: ' +self.chan)
        inv = read_inventory(inFile,'STATIONXML')
        inv = inv.select(station='*', channel=self.chan)
        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(inv[0].code+'.#S.#L.'+self.chan+'.')
            outFile = self.generateName()

        st = self.getStream()
        #print(st)csv/timeWaveformsS/
        print(self.removeResponse)
        if self.removeResponse:
            print(self.removeResponse)
            st2 = st.copy()
            print("st2 : ", st2)
            print(self.outUnit)
            #plotFile="../Images/TWfComp/L3B_nsplot_cTWaveforms_RemResp_"+self.outUnit+"_stepPlot_"+self.sta+"_"+self.chan+".jpeg"
            #st2.remove_response(inventory=inv, output="VEL")
            #st2.remove_response(inventory=inv, output=self.outUnit, plot=plotFile)
            st2.remove_response(inventory=inv, output=self.outUnit)
            st2.plot(outfile=outFile)
        else:
            #st.plot(outfile=self.outputFile, equal_scale = False)
            st.plot(outfile=outFile)
        print('Generate image: '+outFile)
        self.generateCSV([self.chan, self.startTime, self.endTime, os.path.abspath(outFile)])


class PlotPPSDSC(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iMetaFile, outputDir=None, outputModel=None, outputFile=None, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[], ppsdDir="", ppsdNameModel=None, ppsdFormat=""):
        MeasuredDataGraphicGenerator.__init__(self,inputDir, outputDir, outputModel, outputFile, outputFormat, station, channel, startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iMetaFile, outputDir, outputModel, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)

        self.ppsdDir=ppsdDir
        self.ppsdNameModel=ppsdNameModel
        self.ppsdFormat=ppsdFormat

    def generatePPSDName(self):

        ppsdModel = self.ppsdNameModel
        ppsdFile = ppsdModel.generateName() + self.ppsdFormat
        if self.ppsdDir != None:
            ppsdFile = self.ppsdDir+ppsdFile
        return ppsdFile

    def generate(self):
        """
        Provide graphical representation of the ppsd of a station 
        (fournit diagramme probabiliste des Densités Spectrales de Puissance pour chaque canal, 
        de code distinct, parmi toutes les stations)
        """
        if self.sta == "*":
            station=None
        else:
            station=self.sta
        print("station: ", station)

        inFile =self.iMetaDataDir
        #print('channel: ' +self.chan)
        inv = read_inventory(inFile,'STATIONXML')
        inv = inv.select(station=self.sta, channel=self.chan)
        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(inv[0].code+'.'+self.sta+'.#L.'+self.chan+'.')
            outFile = self.generateName()

        self.ppsdNameModel.setPrefix(inv[0].code+'.'+self.sta+'.#L.'+self.chan+'.')
        ppsdFileName=self.generatePPSDName()

        st = self.getStream()
        #print(st)
        if self.isHydrophone():
            print('is hydrophone')
            #ppsd = PPSD(st[0].stats, metadata=inv, db_bins = (-40, 80, 1.0), special_handling = 'hydrophone')
            ppsd = PPSD(st[0].stats, metadata=inv, db_bins = (-80, 80, 1.0), special_handling = 'hydrophone')
        else:
            ppsd = PPSD(st[0].stats, metadata=inv)
        ppsd.add(st)
        #print(ppsd.times_processed[:2])
        #print("number of psd segments:", len(ppsd.times_processed))
        print(ppsdFileName)
        ppsd.save_npz(ppsdFileName)
        ppsd.plot(outFile)
        print('Generate image: '+outFile)
        self.generateCSV([self.sta, os.path.abspath(outFile)])

class PlotPPSDC(MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, iMetaFile, outputDir=None, outputModel=None, outputFile=None, outputFormat=None, channel="*", csvFileName="", csvFieldNames=[], ppsdDir="", ppsdNameModel=None, ppsdFormat=""):

        MetadataGraphicGenerator.__init__(self, iMetaFile, outputDir, outputModel, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
	
        self.chan = channel
        self.ppsdDir=ppsdDir
        self.ppsdNameModel=ppsdNameModel
        self.ppsdFormat=ppsdFormat
        inFile =self.iMetaDataDir
        self.inventory=read_inventory(inFile,'STATIONXML')

    def generatePPSDName(self):

        ppsdModel = self.ppsdNameModel
        ppsdFile = ppsdModel.generateName() + self.ppsdFormat
        if self.ppsdDir != None:
            ppsdFile = self.ppsdDir+ppsdFile
        return ppsdFile

    def createChannelStationsDictForNetwork(self, net):
        """Create a dictionary with the channel code as key and a set of station codes as value
        """        
       
        channelStations={}
        for i in range(len(self.inventory.get_contents()['networks'])):
            if self.inventory[i].code == net:
                for j in range(len(self.inventory.get_contents()['stations'])):
                    for k in range(len(self.inventory[i][j].get_contents()['channels'])):
                        channelStations[self.inventory[i][j][k].code]=set()
                for j in range(len(self.inventory.get_contents()['stations'])):
                    for k in range(len(self.inventory[i][j].get_contents()['channels'])):
                        channelStations[self.inventory[i][j][k].code].add(self.inventory[i][j].code)

        return channelStations

    def generate(self):
        """
        Provide graphical representation of the ppsd of the same channel of all stations 
        (fournit diagramme probabiliste des Densités Spectrales de Puissance pour chaque canal, 
        de code distinct, parmi toutes les stations)
        """
        
        if (re.match('..H', self.chan)) != None:
            isHydrophone = True
        else:
            isHydrophone = False

        outFile = self.outputFile
        if  outFile == None:
            self.outputModel.setPrefix(self.inventory[0].code+'.#S.#L.'+self.chan+'.')
            outFile = self.generateName()

        fig, ax = plt.subplots()
        if not isHydrophone:
            period_lim=(0.01, 1000)
            for periods, noise_model in (get_nhnm(), get_nlnm()):
                xdata3 = periods
                #ax.plot(xdata3, noise_model, '0.4', linewidth=2)
                ax.plot(xdata3, noise_model, linestyle=(':'), linewidth=2, color='grey')


        channelStations=self.createChannelStationsDictForNetwork(self.inventory[0].code) 
        for station in channelStations[self.chan]:
            self.ppsdNameModel.setPrefix(self.inventory[0].code+'.'+station+'.#L.'+self.chan+'.')
            ppsdFileName=self.generatePPSDName()
            if os.path.exists(ppsdFileName):
                ppsd =  PPSD.load_npz(ppsdFileName) # ex '4G.LSV6A.BHZ.PPSDSC.npz'
                print("read npz file : " + ppsdFileName)
                periods, percentile_values = ppsd.get_percentile()
                ax.plot(periods, percentile_values, label=station)
            else:
                print("File : "+ppsdFileName+" does exist")

        ax.semilogx()
        if not isHydrophone:
            ax.set_xlim(period_lim)
        ax.set_xlabel('period  [s]')
        ax.set_ylabel('Amplitude [db]')
        ax.set_title('Median PSD plots for channel code '+ self.chan+ ', all stations')
        ax.legend()
        plt.savefig(outFile)
        plt.close()
        print('Generate image: '+outFile)
        self.generateCSV([self.chan, os.path.abspath(outFile)])
