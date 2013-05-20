# -*- coding: UTF-8 -*-

import sys
from threading import Thread
import copy
import time
from traceback import * 




REQUEST_OK = 0x00
REQUEST_APPEND = 0x01
REQUEST_ERROR = 0x02
REQUEST_INVALID = 0x03


#Print Level of PrintD
#0:Debug 1:Failure 2:Error
PRINT_LEVEL = 2


class ServiceBase(Thread):
    
    READY = 0
    RUN = 1
    STOP = 2
    PAUSE = 3
    RELEASE = 4
    
    def __init__(self, args=[]):
        Thread.__init__(self)
        self.name = 'ServiceBase'
        self.args = []
        self.status = ServiceBase.READY
        PrintD(self, '__init__')
    
    #override
    def run(self):
        print 'run'
        self.status = ServiceBase.RUN
    
    def Start(self):
        self.setDaemon(True)
        self.start()

        
    def Stop(self):
        print 'stop'
        self.status = ServiceBase.STOP

    def Pause(self):
        print 'pause'
        self.status = ServiceBase.PAUSE

    def Resume(self):
        print 'resume'
        self.status = ServiceBase.RUN

    def Release(self):
        print 'release'
        self.status = ServiceBase.RELEASE

    def QueryService(self, request, response=None, callback=None):
        if request.has_key('Request'):
            PrintD(self, 'QueryService', {'Request':request['Request']})
        return REQUEST_INVALID


#Print the Debug Info
#@param self: object instance
#@param type: Info=0,Failure=1,Error=2,Debug=3
def PrintD(self, mName=None, infos={}, info_type=0):
    t = time.time()
    info = ''
    if info_type == 0:
        pass
    elif info_type == 1:
        info = 'Failure,'
    elif info_type == 2:
        info = 'Error,'
    
    for key, data in infos.iteritems():
        if data:
            info += '%s<%s>;' % (key, data.__repr__())
        else:
            info += '%s' % key
    
    if info_type >= PRINT_LEVEL:
        print '[time:', t, '%s:%s:%s] %s\n' \
        % (self.__module__, self.__class__.__name__, mName, info)
        

def test():
    print "test!"
    print sys.platform
    
    service = ServiceBase()
    PrintD(service, infos={'test':3})

    print 'End'
#================================================================

if __name__ == '__main__':
    test()
    #PrintD(infos=['test',3])

