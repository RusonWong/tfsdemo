# -*- coding: UTF-8 -*-

'''
Created on 2012-2-12

@author: guxin
'''

from handler.ReqHandler import ReqHandler
from utils import common
from webserver.WebServer import WebServerService
import sys


if __name__ == '__main__':
    print 'test'
    print sys.platform
    common.PRINT_LEVEL = 0
    
    handler = ReqHandler()
    service = WebServerService(handler.doProcessRequest)
    service.start()
    
    print 'started'
