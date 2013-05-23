'''
Created on 2013-5-19

@author: rusonwong
'''

from Model.Block import Block
from Model.File import File

class Disk(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__block_count = 100
        
        self.__hot_space_count = 10
        
        self.__blocks = [] #Blocks
        self.__LFiles = [] #Local Files
        self.__TFiles = [] #Transparent Filess
        
        #init blocks
        for i in range(100):
            self.__blocks.append(Block())
    
    def snapshot(self):
        dmodel = {}
        dmodel["blockcount"] = self.__block_count
        states = [block.getState() for block in self.__blocks]
        dmodel["states"] = states;
        return dmodel;
       
       
    '''
    write
    delete
    clean transparent
    write transparent
    Delete transparent
    '''
    def deleteFile(self,fileName):
        fileToDelete = None;
        files = [f for f in self.__LFiles if f.fileName==fileName]
        if len(files) > 0:
            fileToDelete = files[0]
            for idx in range(len(fileToDelete.blocks)):
                blockidx = fileToDelete.blocks[idx]
                self.__blocks[blockidx].processOperation("delete")
            '''todo delete file from file array'''
            for i in range(len(self.__LFiles)):
                if self.__LFiles[i].fileName == fileName:
                    del self.__LFiles[i]
                    break
            return True
        return False
    
    '''
    ..............................
    create local file
    ..............................
    '''
    def createFile(self,fileName,size):
        '''check filename existence'''
        files = [f for f in self.__LFiles if f.fileName==fileName]
        if len(files) > 0:
            return False;
        
        newFile = File();
        newFile.fileName = fileName
        newFile.fileSize = size
        sizeleft = size;
        for i in range(self.__block_count):
            block = self.__blocks[i]
            if block.getState() == Block.States["Free"] or block.getState() == Block.States["Transparent"] or block.getState() == Block.States["Free_and_Overwritten"]:
                newFile.blocks.append(i)
                sizeleft = sizeleft - Block.BlockSize;
                if sizeleft <= 0:
                    break
        if sizeleft > 0:
            return False
        for i in range(len(newFile.blocks)):
            self.__blocks[newFile.blocks[i]].processOperation("write")
        self.__LFiles.append(newFile)
        return True;
    
    
    #transparent operations
    def deleteTransparentFile(self,fileName):
        if not self.__isTFileExist(fileName):
            return False
        
        if self.__isTFileExistandDirty(fileName):
            return self.cleanTransparentFile(fileName)
        
        fileToDelete = None;
        files = [f for f in self.__TFiles if f.fileName==fileName]
        if len(files) > 0:
            fileToDelete = files[0]
            for idx in range(len(fileToDelete.blocks)):
                blockidx = fileToDelete.blocks[idx]
                self.__blocks[blockidx].processOperation("delete_transparent")
            '''todo delete file from file array'''
            for i in range(len(self.__TFiles)):
                if self.__TFiles[i].fileName == fileName:
                    del self.__TFiles[i]
                    break
            return True
        return False
    
    def openTransparentFile(self,fileName):
        if self.__isTFileExistandDirty(fileName):
            self.cleanTransparentFile(fileName)
            return False
        return True
    
    def cleanTransparentFile(self,fileName):
        if not self.__isTFileExistandDirty(fileName):
            return False
        fileToDelete = None;
        files = [f for f in self.__TFiles if f.fileName==fileName]
        if len(files) > 0:
            fileToDelete = files[0]
            for idx in range(len(fileToDelete.blocks)):
                blockidx = fileToDelete.blocks[idx]
                self.__blocks[blockidx].processOperation("clean_transparent")
            '''todo delete file from file array'''
            for i in range(len(self.__LFiles)):
                if self.__TFiles[i].fileName == fileName:
                    del self.__TFiles[i]
                    break
            return True
        return False
    
    def createTransparentFile(self,fileName,size):
        '''check filename existence'''
        files = [f for f in self.__TFiles if f.fileName==fileName]
        if len(files) > 0:
            return False;
        
        newFile = File();
        newFile.fileName = fileName
        newFile.fileSize = size
        sizeleft = size;
        for i in range(self.__block_count - self.__hot_space_count):
            block = self.__blocks[i + self.__hot_space_count]
            if block.getState() == Block.States["Free"]:
                newFile.blocks.append(i + self.__hot_space_count)
                sizeleft = sizeleft - Block.BlockSize;
                if sizeleft <= 0:
                    break
        if sizeleft > 0:
            return False
        for i in range(len(newFile.blocks)):
            self.__blocks[newFile.blocks[i]].processOperation("write_transparent")
        self.__TFiles.append(newFile)
        return True;
    
    def lsLocalFiles(self):
        files = [f.fileName for f in self.__LFiles]
        return files
    
    def lsTransparentFiles(self):
        files = [f.fileName for f in self.__TFiles]
        return files
    
    '''
    check file deleteable, just to check if it is transparent(all blocks transparent)
    '''
    def __isTFileExist(self,fileName):
        '''find file'''
        files = [f for f in self.__TFiles if f.fileName==fileName]
        if len(files) <= 0:
            return False;
        return True
    
    '''
    isFileCleanable: check file clean able, just to check if it is(partly) overwritten 
    '''
    def __isTFileExistandDirty(self,fileName):
        files = [f for f in self.__TFiles if f.fileName==fileName]
        if len(files) <= 0:
            return False;
        
        fileToCheck = files[0]
        for idx in range(len(fileToCheck.blocks)):
            blockidx = fileToCheck.blocks[idx]
            if (self.__blocks[blockidx].getState() == Block.States['Free_and_Overwritten']\
                     or self.__blocks[blockidx].getState() == Block.States['Allocated_and_Overwritten']):
                print "find some block overwritten... cleanable"
                return True
        return False