'''
Created on 2013-5-20

@author: sniperwang
'''
from Common.HtmlGraber import HtmlGraber

class LocalService(object):
    '''
    classdocs
    '''
    urlbase = "http://localhost:8080/local"
    htmlGraber = HtmlGraber()
    def __init__(self):
        '''
        Constructor
        '''
    def ls(self):
        url = self.urlbase + "/ls"
        #print url
        content = self.htmlGraber.doGrab(url)
        print content
        
    def create(self,fileName,size):
        url = self.urlbase + "/create?filename="+fileName+"&size="+str(size)
        #print url
        content = self.htmlGraber.doGrab(url)
        print content
        
    def delete(self,fileName):
        url = self.urlbase + "/delete?filename="+fileName
        #print url
        content = self.htmlGraber.doGrab(url)
        print content
        