'''
Created on 2012-9-19

@author: sniperwang
'''
import urllib;
import urllib2;

class HtmlGraber(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def doGrab(self,url):
        sock=urllib.urlopen(url);
        htmlSource=sock.read();
        sock.close();
        return htmlSource;
    
    def doRequest(self,url,params):
        req=urllib2.Request(url,urllib.urlencode(params));
        content=urllib2.urlopen(req).read();
        return content;
        
        