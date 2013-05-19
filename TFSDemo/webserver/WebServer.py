# -*- coding: UTF-8 -*-


from SimpleHTTPServer import SimpleHTTPRequestHandler
from utils.common import *
import BaseHTTPServer
import httplib
import json
import os.path
import posixpath
#import sys
#import time
import urllib
import urlparse
#from utils.ServiceBase import ServiceBase, PrintD
#import os

#from threading import Thread
#import thread
#import win32process

#try:
#    import ServiceBase
#except ImportError:
#    sys.path.append(os.path.abspath(r'..\ServiceAgent'))
#    import ServiceBase

handles = []





"""
-------------------------------------------------------------------------------

 StoppableHttpServer

 @summary:  The class implements the HTTP server, so that it can be stopped

-------------------------------------------------------------------------------
"""
class StoppableHttpServer (BaseHTTPServer.HTTPServer):
    """http server that reacts to self.stop flag"""

    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.Stop = False
        while not self.Stop:
            self.handle_request()


"""
-------------------------------------------------------------------------------

 WebServerService

 @summary:  The class implements the WebServer service

-------------------------------------------------------------------------------
"""
class WebServerService(ServiceBase):
    
    def __init__(self, callback=None):
        ServiceBase.__init__(self)
        
        self.httpd = None
        self.name = 'WebServer'
        self.status = ServiceBase
        self.port = 8080
        
        self.__OnReqService = callback
        self.__OnEvent = None
        
        self.__SessionID = 0
    
    #override the run
    def run(self):
        server_address = ('', 8080)
        self.httpd = StoppableHttpServer(server_address, RequestHandler)
        RequestHandler.OnReqService = self.__OnReqService
        
        self.status = ServiceBase.RUN
        self.httpd.serve_forever()
        
        while self.status == ServiceBase.RUN:
            #print 'web status %d' % self.status
            try:
                self.httpd.handle_request()
            except Exception as e:
                PrintD(self, 'run', {'http handle_request':e}, 2)
            #print 'after web status %d' % self.status
            #time.sleep(0.05)
            
        if self.__OnEvent:
            self.__OnEvent({'Event':'OnRelease', 'Service':'WebServer'})
        PrintD(self, 'run', {'WebServer service terminated':None})
    
    def Start(self, OnEvent):
        self.__OnEvent = OnEvent
        try:
            self.start()
        except Exception as e:
            PrintD(self, 'Start', {'Start Exception':e}, 2)
    
    #send QUIT request to http server running on localhost:<port>
    def Stop(self):            
        self.status = ServiceBase.STOP
        self.httpd.Stop = True
        try:
            conn = httplib.HTTPConnection("127.0.0.1:%d" % self.port)
            conn.request("QUIT", "/")
        except Exception as e:
            PrintD(self, 'Stop', {'HttpConnection':e}, 2)
        finally:
            self.httpd.socket.close()


"""
------------------------------------------------------------------------------
 RequestHandler

 @summary:     The Handler to process the HTTP Request. It implements the POST 
               method and overrides the GET method. The OnReqService must be 
               initializes with a callback method to process the XmlHttpRequest.
               Usually, the RequestHandler is initialized by the WebServerService,
               which hosts a HTTP Server and passes the HTTP Request to the 
               RequestHandler.
 @todo:        NOTICE that the request of src address MUST be a local address!!!
               It's NOT implemented yet! 

-------------------------------------------------------------------------------
"""
class RequestHandler(SimpleHTTPRequestHandler):

    server_version = "RequestHTTP/"
    #Callback method
    OnReqService = None


    def do_GET(self):
        """Serve a GET request."""
        #print ' '
        #print '==================================================='
        #print 'HTTP Request GET >>> %s' % self.path
        PrintD(self, 'do_GET', {'Request':self.path})
        PrintD(self, 'do_GET', {'IP address':'(%s %s)' % self.client_address})
        
        reqeust = None
        try:            
            reqeust = self.__ParseServiceRequest(self.path)
        except:
            PrintD(self, 'do_GET', {'Failed to parse request':None}, 1)
            
        if (reqeust != None):
            result = False
            data = None
            
            try:
                result, data = self.OnReqService(reqeust) 
                
                if (result == True and data != None):              
                    self.__CreateResponse(data)
                else:
                    SimpleHTTPRequestHandler.do_GET(self)
                    #self.send_error(405, "Method Not Allowed")
                
            except Exception as e:
                PrintD(self, 'do_GET', {'OnReqService Problem':e}, 2)      
                    
        else:
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        
        #print '===================================================='
    
    def do_QUIT (self):
        #send 200 OK response
        #self.status = ServiceBase.STOP
        PrintD(self, 'do_QUIT')
        #self.send_response(200)
        #self.end_headers()        
        #PrintD(self, 'do_QUIT', {'Done':None})


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = urlparse.urlparse(path)[2]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        #path = os.getcwd()
        path = os.path.abspath(r"WebPage")
        print path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): 
                continue
            path = os.path.join(path, word)
        return path
    
    def log_message(self, format, *args):
        """This method overrides the BaseHTTPServer.log_message() to avoid the overflow of log message"""

        PrintD(self, \
               'log_message', \
               {'address':self.address_string(), \
                'date':self.log_date_time_string(), \
                'request': format % args})

    """
    -------------------------------------------------------------------------------
    
    ParseServiceRequest
    
    @summary:  Parse the ServiceRequest, and return the response
    
    -------------------------------------------------------------------------------
    """
    def __ParseServiceRequest(self, url):

        words = urlparse.urlparse(url);
        print "words=",words
        path = words[2]
        print "path:",path;
        paths =  [item for item in path.split("/") if item !=''];
        print "new path:",path
        querys = urlparse.parse_qs(words[4], True);
        print 'query=', querys
        
      
        if len(paths) == 2:
            querys["service"] = paths[0]
            querys["method"] = paths[1]
            return querys
        return None
    
    def __CreateResponse(self, data):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Last-Modified", self.date_time_string(time.time()))
        self.end_headers()
        self.wfile.write(data)            
        return data
   
   
###################################################################
  
def test():
    print "test!"
    print sys.platform
    service = WebServerService()
    service.start()
    print 'End'

if __name__ == ' __main__':
    print 'test'
    test()


    
