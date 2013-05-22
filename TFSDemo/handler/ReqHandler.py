# -*- coding: UTF-8 -*-
from Model import TFSModel
import string

class ReqHandler(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__ordered = {}
        self.__calledcount = 0;
        self.__tfs_model = TFSModel.TFSModel()
    
    def doProcessRequest(self, request):
        self.__calledcount = self.__calledcount+1
        
        rslt = False
        msg = None
        print 'request=', request
        service = None;
        method = None;
        
        if request.has_key('service'):
            service = request['service']
            print "requesttype is",service
        else:
            return False,"";
        
        if request.has_key('method'):
            method = request['method']
            print "method is:",method
        else:
            return False,""
        
        #do handle request
        rslt=False
        msg=""
        if service == "transparent":
            rslt,msg = self.__processTransparentMethod(request)
        
        if service == "local":
            rslt,msg = self.__processLocalMethod(request)
            
        if service == "monitor":
            rslt,msg = True,self.__getDiskSnapShot()
        return rslt, msg
    
    
    
    def __processLocalMethod(self, request):
        rslt = False
        msg = "failed"
        
        '''process local create'''
        if request['method'] == "create":
            fileName = request['filename'][0]
            size = string.atoi(request['size'][0])
            print "filename:"+fileName,type(size),":",size
            rslt = self.__tfs_model.createFile(fileName, size)
            if rslt == True:
                msg = "ok"
        '''process local delete'''
        if request['method'] == "delete":
            fileName = request['filename'][0]
            print "file to delete:",fileName
            rslt = self.__tfs_model.deleteFile(fileName)
            if rslt == True:
                msg = "ok"
        if request['method'] == "ls":
            msg = self.__tfs_model.lsLocalFiles()
        return True,msg
        
    def __processTransparentMethod(self, request):
        msg = "failed"
        '''process transparent create'''
        if request['method'] == "create":
            fileName = request['filename'][0]
            size = string.atoi(request['size'][0])
            print "filename:"+fileName,type(size),":",size
            rslt = self.__tfs_model.createTransparentFile(fileName, size)
            if rslt == True:
                msg = "ok"
        if request['method'] == "delete":
            fileName = request['filename'][0]
            print "file to delete:",fileName
            rslt = self.__tfs_model.deleteTransparentFile(fileName)
            if rslt == True:
                msg = "ok"
        if request['method'] == "open":
            fileName = request['filename'][0]
            print "file to open:",fileName
            rslt = self.__tfs_model.openTransparentFile(fileName)
            if rslt == True:
                msg = "ok"
        if request['method'] == "ls":
            msg = self.__tfs_model.lsTransparentFiles()
        return True,msg;
    
    def __getDiskSnapShot(self):
        return self.__tfs_model.getDiskSnapshot()
    
