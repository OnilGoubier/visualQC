
from abc import ABC, abstractmethod
from dirAndFiles import listOfFilesWithAbsName
from obspy.clients.filesystem.sds import Client
from obspy import read_inventory
from obspy import read
from obspy.io.xseed import Parser
from obspy.signal import PPSD
import os
import csv
import re

class GraphicGenerator(ABC):

    def __init__(self,inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None):
        self.inputDir=inputDir
        self.outputDir = outputDir
        self.outSuffix = outSuffix
        self.outputFile=outputFile
        self.outputFormat=outputFormat

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class MetadataGraphicGenerator(GraphicGenerator):

    #input file extension
    extension='.xml'
    iXMLFiles=[]

    def __init__(self, inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None):
        super().__init__(inputDir, outputDir, outSuffix, outputFile, outputFormat)
        self.iMetaDataDir=inputDir

    def getInputFile(self, station=None):
        """ return an xml format input file with absolut path, or an absolute path name with *.xml, for a number of stations"""

        
        self.iXMLFiles=listOfFilesWithAbsName(self.iMetaDataDir, self.extension)
        #print(self.iXMLFiles)
        #print("getInputfile station:", station)
        if not self.iXMLFiles:
            print("No xml station file in the directory")
        else:
            if(len(self.iXMLFiles)>1):
                if station:
                    for fn in self.iXMLFiles:
                        if (os.path.basename(fn).rfind(station) >= 0):
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

    def __init__(self, inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None, startTime=None, endTime=None):
        super().__init__(inputDir, outputDir, outSuffix,  outputFile, outputFormat)
        self.startTime=startTime
        self.endTime=endTime

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class EventBasedGraphicGenerator(TimeBasedGraphicGenerator):

    def __init__(self, inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None, startTime=None, endTime=None, eventTime=None):
        super().__init__(inputDir, outputDir, outSuffix, outputFile, outputFormat, startTime, endTime)
        self.eventTime=eventTime

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class DurationBasedGraphicGenerator(TimeBasedGraphicGenerator):

    def __init__(self, inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None, startTime=None, endTime=None, duration=None):
        super().__init__(inputDir, outputDir, outSuffix,  outputFile, outputFormat, startTime, endTime)
        self.duration=duration

    @abstractmethod
    def generate(self):
        "call obspy to generate graphic"

class MeasuredDataGraphicGenerator(DurationBasedGraphicGenerator):

    net="*"
    sta="*"
    loc="*"
    chan="*"

    def __init__(self, inputDir, outputDir=None, outSuffix=None, outputFile=None, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None):
        super().__init__(inputDir, outputDir, outSuffix,  outputFile, outputFormat, startTime, endTime, duration)
        self.iDataDir=inputDir
        self.sta=station
        self.chan=channel

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

        with open(self.csvFileName, 'w', newline='') as csvfile:
            mywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            mywriter.writerow(self.csvFieldNames)
            mywriter.writerow(data)        

class plotStationsMap(MetadataGraphicGenerator):

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
            outFile = inv[0].code+self.outSuffix
            if self.outputDir != None:
                outFile = self.outputDir+'/'+outFile
        print('Generate image: '+outFile)
        inv.plot(projection="local", resolution="i", outfile=outFile)

class plotDataAvailability(EventBasedGraphicGenerator):

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
            outFile = self.outSuffix
            if self.outputDir != None:
                outFile = self.outputDir+'/'+outFile
        self.command=self.command+' --output '+outFile
        print(self.command)
        os.system(self.command)

class L2_nsplot_sInstrumentResponse(MetadataGraphicGenerator):
    
    station = ""

    def __init__(self, inputDir,outputFile, outputFormat=None, station=""):
        super().__init__(inputDir,outputFile, outputFormat)
        self.station=station

    def generate(self):
        """
        Generate graphic of instrument response with all channels for a station
        """

        #inFile = self.getInputFile(self.station)
        inFile =self.iMetaDataDir        
        sta = read_inventory(inFile,'STATIONXML')[0][0]	
        sta.plot(0.001, output="VEL", outfile=self.outputFile)

class L3_nsplot_cInstrumentResponse(MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir,outputFile, outputFormat=None, channel="", csvFileName="", csvFieldNames=[]):
        MetadataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.channel=channel

    def generate(self):

        print("InputDir:"+self.inputDir)
        print(self.extension)
        inFile = self.getInputFile()
        inv = read_inventory(inFile,'STATIONXML')
        inv = inv.select(station='*', channel=self.channel)	
        #inv.plot_response(0.001, outfile=self.outputFile, label_epoch_dates=True)
        inv.plot_response(0.001, outfile=self.outputFile)
        self.generateCSV([self.channel, self.outputFile])


class  L2B_nsplot_sTimeWaveforms(MeasuredDataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir,outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[]):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel, startTime, endTime, duration)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)

    def generate(self):
        """
        Provide waveforms of all (or a subset of) channels of a station
        Fournir des graphes/courbe de series temporelles, avec tous les canaux, pour une station.      
        Fournir diagramme de séries temporelles pour chaque station, 
        relativement à un événement sismique particulier (Doc Olivier)
        """

        st = self.getStream()
        print(st)
        st.plot(outfile=self.outputFile, equal_scale = False)
        #st.plot(outfile=self.outputFile)
        self.generateCSV([self.sta, self.startTime, self.endTime, self.outputFile])

class  L2B_nsplot_sTimeWaveforms_RemResp(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iXMLDir, outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[]):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel, startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iXMLDir, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)

    def generate(self):
        """
        Provide waveforms of all (or a subset of) channels of a station
        Fournir des graphes/courbe de series temporelles, avec tous les canaux, pour une station.      
        Fournir diagramme de séries temporelles pour chaque station, 
        relativement à un événement sismique particulier (Doc Olivier)
        """

        if self.sta == "*":
            station=None
        else:
            station=self.sta
        print("station: ", station)
        inFile = self.getInputFile(station)
        print("inFile : ", inFile)
        inv = read_inventory(inFile,'STATIONXML')

        st = self.getStream()
        print(st)
        st2 = st.copy()
        print("st2 : ", st2)
        st2.remove_response(inventory=inv, output="VEL")
        st2.plot(outfile=self.outputFile)        
        #st.plot(outfile=self.outputFile, equal_scale = False)
        #st.plot(outfile=self.outputFile)
        self.generateCSV([self.sta, self.startTime, self.endTime, self.outputFile])

class L3B_nsplot_cTimeWaveforms(MeasuredDataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir,outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[]):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel, startTime, endTime, duration)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        

    def generate(self):
        """
        Provide plots of waveform of the same channel of all stations 
        Fournir graphes/courbes de réponse instrumentale, avec tous les canaux, pour une station)
        """

        st = self.getStream()
        #print(st)
        st.plot(outfile=self.outputFile, equal_scale = False)
        #st.plot(outfile=self.outputFile)
        self.generateCSV([self.chan, self.startTime, self.endTime, self.outputFile])

class L3B_nsplot_cTimeWaveforms_RemResp(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iXMLDir, outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[], outUnit="VEL"):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel, startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iXMLDir, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.outUnit=outUnit

    def generate(self):
        """
        Provide plots of waveform of the same channel of all stations 
        Fournir graphes/courbes de réponse instrumentale, avec tous les canaux, pour une station)
        """

        if self.sta == "*":
            station=None
        else:
            station=self.sta
        print("station: ", station)
        inFile = self.getInputFile(station)
        print("inFile : ", inFile)
        inv = read_inventory(inFile,'STATIONXML')


        st = self.getStream()
        #print(st)
        st2 = st.copy()
        print("st2 : ", st2)
        plotFile="../Images/TWfComp/L3B_nsplot_cTWaveforms_RemResp_"+self.outUnit+"_stepPlot_"+self.sta+"_"+self.chan+".jpeg"
        #st2.remove_response(inventory=inv, output="VEL")
        st2.remove_response(inventory=inv, output=self.outUnit, plot=plotFile)
        st2.plot(outfile=self.outputFile)
        #st.plot(outfile=self.outputFile, equal_scale = False)
        #st.plot(outfile=self.outputFile)
        self.generateCSV([self.chan, self.startTime, self.endTime, self.outputFile])

class L3_nsplot_cPPSD(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iXMLDir, outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[]):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel,  startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iXMLDir, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)


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
        inFile = self.getInputFile(station)
        print("inFile : ", inFile)
        inv = read_inventory(inFile,'STATIONXML')
        st = self.getStream()
        print(st)
        ppsd = PPSD(st[1].stats, metadata=inv)
        ppsd.add(st)
        print(ppsd.times_processed[:2])
        #print("number of psd segments:", len(ppsd.times_processed))
        ppsd.plot(self.outputFile)
        self.generateCSV([self.sta, self.outputFile])

"""
class L4_nsplot_csPPSD, for a number of stations ? problem with SDS, can not have more than one station in the client SDS root
"""

class L4_nsplot_csPPSD(MeasuredDataGraphicGenerator, MetadataGraphicGenerator, GraphicMetaData):

    def __init__(self, inputDir, iXMLDir, outputFile, outputFormat=None, station="*", channel="*", startTime=None, endTime=None, duration=None, csvFileName="", csvFieldNames=[], ppsdFileName=""):
        MeasuredDataGraphicGenerator.__init__(self,inputDir,outputFile, outputFormat, station, channel,  startTime, endTime, duration)
        MetadataGraphicGenerator.__init__(self, iXMLDir, outputFile, outputFormat)
        GraphicMetaData.__init__(self, csvFileName, csvFieldNames)
        self.ppsdFileName=ppsdFileName
        if re.match('..H', channel) != None:
            self.isHydrophone = True
        else:
            self.isHydrophone = False

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
        inFile = self.getInputFile(station)
        print("inFile : ", inFile)
        inv = read_inventory(inFile,'STATIONXML')
        st = self.getStream()
        print(st)
        if self.isHydrophone:
            print('is hydrophone')
            #ppsd = PPSD(st[0].stats, metadata=inv, db_bins = (-40, 80, 1.0), special_handling = 'hydrophone')
            ppsd = PPSD(st[0].stats, metadata=inv, db_bins = (-80, 80, 1.0), special_handling = 'hydrophone')
        else:
            ppsd = PPSD(st[0].stats, metadata=inv)
        ppsd.add(st)
        print(ppsd.times_processed[:2])
        #print("number of psd segments:", len(ppsd.times_processed))
        print(self.ppsdFileName)
        ppsd.save_npz(self.ppsdFileName)
        ppsd.plot(self.outputFile)
        self.generateCSV([self.sta, self.outputFile])
