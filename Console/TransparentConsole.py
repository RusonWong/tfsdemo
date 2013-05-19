'''
Created on 2013-5-20

@author: sniperwang
'''
from Common.TransparentService import TransparentService

if __name__ == '__main__':
    pass
transparentService = TransparentService()

while True:
    cmd = raw_input("transparent>")
    #print cmd
    cmd = cmd.split(" ")
    #print cmd
    op = cmd[0]
    if op == "create":
        fileName = cmd[1]
        size = cmd[2]
        transparentService.create(fileName, size)
    elif op == "delete":
        fileName = cmd[1]
        transparentService.delete(fileName)
    elif op == "clean":
        fileName = cmd[1]
        transparentService.delete(fileName)
    elif op == "ls":
        transparentService.ls();
    elif op == "quit":
        break