'''
Created on 2013-5-19

@author: rusonwong
'''
from Model import Disk
import json
import random

class TFSModel(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__Disk = Disk.Disk()
    
    def getDiskSnapshot(self):
        dmodel = self.__Disk.snapshot();
        
        #test
        #for i in range(100):
        #    dmodel['states'][i] = random.randint(1,5)
        #test end
        
        return json.dumps(dmodel);
    
    '''delete file'''
    def deleteFile(self,fileName):
        return self.__Disk.deleteFile(fileName)
    
    def createFile(self,fileName,size):
        return self.__Disk.createFile(fileName,size)
    
    #transparent operations
    def deleteTransparentFile(self,fileName):
        return self.__Disk.deleteTransparentFile(fileName)
    
    def cleanTransparentFile(self,fileName):
        return self.__Disk.cleanTransparentFile(fileName)
    
    def createTransparentFile(self,fileName,size):
        return self.__Disk.createTransparentFile(fileName, size)
    
    def openTransparentFile(self,fileName):
        return self.__Disk.openTransparentFile(fileName)
    
    def lsLocalFiles(self):
        return json.dumps(self.__Disk.lsLocalFiles())
    
    def lsTransparentFiles(self):
        return json.dumps(self.__Disk.lsTransparentFiles())
        