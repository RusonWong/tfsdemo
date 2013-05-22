'''
Created on 2013-5-20

@author: sniperwang
'''
from Common.HtmlGraber import HtmlGraber

class TransparentService(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.urlbase = "http://localhost:8080/transparent"
        
    def ls(self):
        htmlGraber = HtmlGraber()
        url = self.urlbase + "/ls"
        #print url
        content = htmlGraber.doGrab(url)
        print content
        
    def create(self,fileName,size):
        htmlGraber = HtmlGraber()
        url = self.urlbase + "/create?filename="+fileName+"&size="+str(size)
        #print url
        content = htmlGraber.doGrab(url)
        print content
        
    def delete(self,fileName):
        htmlGraber = HtmlGraber()
        url = self.urlbase + "/delete?filename="+fileName
        #print url
        content = htmlGraber.doGrab(url)
        print content
        
    def open(self,fileName):
        htmlGraber = HtmlGraber()
        url = self.urlbase + "/open?filename="+fileName
        #print url
        content = htmlGraber.doGrab(url)
        print content
        