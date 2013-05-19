'''
Created on 2013-5-19

@author: rusonwong
'''

class Block(object):
    States={"Free":1,"Allocated":2,"Transparent":3,"Free_and_Overwritten":4,"Allocated_and_Overwritten":5}
    BlockSize = 10
    def __init__(self):
        self.__state = self.States["Free"]
        
    '''
    write
    delete
    
    clean transparent
    write transparent
    Delete transparent
    '''
    def processOperation(self, operation):
        if self.__state == self.States["Free"]:
            self.__processOpOn_Free(operation)
        elif self.__state == self.States['Allocated']:
            self.__processOpOn_Allocated(operation)
        elif self.__state == self.States['Allocated_and_Overwritten']:
            self.__processOpOn_Allocated_and_Overwritten(operation)
        elif self.__state == self.States['Free_and_Overwritten']:
            self.__processOpOn_Free_and_Overwritten(operation)
        elif self.__state == self.States['Transparent']:
            self.__processOpOn_Transparent(operation)
    
    
    def getState(self):
        return self.__state;
    
    def __processOpOn_Free(self, op):
        if op == "write":
            self.__state = self.States["Allocated"];
        elif op == 'write_transparent':
            self.__state = self.States["Transparent"];
            
    def __processOpOn_Allocated(self, op):
        if op == "delete":
            self.__state = self.States["Free"];
            
    def __processOpOn_Allocated_and_Overwritten(self, op):
        if op == "clean_transparent":
            self.__state = self.States["Allocated"];
        elif op == "delete":
            self.__state = self.States["Free_and_Overwritten"]
    
    def __processOpOn_Free_and_Overwritten(self, op):
        if op == "write":
            self.__state = self.States["Allocated_and_Overwritten"];
        elif op == "clean_transparent":
            self.__state = self.States["Free"];
    def __processOpOn_Transparent(self, op):
        if op == "write":
            self.__state = self.States["Allocated_and_Overwritten"]
        elif op == "delete_transparent":
            self.__state = self.States["Free"]