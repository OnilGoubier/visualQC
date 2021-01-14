#!/usr/bin/env python

import os

def getListOfStations(campaign):
	""" get station names """
	myDirectories = [name for name in os.listdir(campaign) 
			if os.path.isdir(campaign+'/'+name)]
	#print(myDirectories)
	#check if a directory is a station directory
	stationDirectories = [dir for dir in myDirectories 
			     if isStationDirectory(campaign+'/'+dir)]
	return stationDirectories

def listOfFiles(directory, extension):
	"""return a list of files with extension 'extension'"""

	myList = []
	extension = extension.lower()
	for dirpath, dirnames, files in os.walk(directory):
		for name in files:
			if name.lower().endswith(extension):
				myList.append(name)
	return myList

def listOfFilesWithAbsName(directory, extension):
	"""return a list of files with extension 'extension' and absolute names"""

	myList = []
	extension = extension.lower()
	for dirpath, dirnames, files in os.walk(directory):
		for name in files:
			if name.lower().endswith(extension):
				myList.append(dirpath+'/'+name)
	return myList				


def listOfDirectories(directory):
	"""return a list of directories"""

	myList = []
	for dirpath, dirnames, files in os.walk(directory):
		for name in dirnames:
			myList.append(name)
	return myList

def listOfAll(directory):
	"""return  list of all"""
	
	for dirpath, dirnames, files in os.walk(directory):
		print('Dirpath: '+str(dirpath))
		print('Dirnames: '+str(dirnames))
		print('Files:'+str(files))
	

def isStationDirectory(dir):
	"""Using os.listdir(), it does not go through the tree, to check of a directory is a a station directory (a directory that contains a station structure),
	check if there is *.raw.lch or *.orig.lch files in the directory (could be more than this checking, 
	check if the list is empty using not [ ], return true if the list is not empty"""

	return not not [
	    lchFile for lchFile in [
	        fl for fl in os.listdir(dir) if os.path.isfile(dir+'/'+fl)] 
	        if (lchFile.endswith('.raw.lch') or lchFile.endswith('.orig.lch'))]

def isStationDirectoryTree(dir):
	"""Using os.walk(), to check of a directory tree is a a station directory (a directory that contains a station structure),
	check if there is *.raw.lch or *.orig.lch files in the directory (could be more than this checking, 
	check if the list is empty using not [ ], return true if the list is not empty"""

	extension='.lch'
	return not not listOfFiles(dir, extension)
	    

def checkAndCreate(path, dirName):
    """ create a directory named dirName if it's not in the path"""
    if not os.path.exists(path+'/'+dirName):
        os.mkdir(path+'/'+dirName) 	
