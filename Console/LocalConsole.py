'''
Created on 2013-5-20

@author: sniperwang
'''
from Common.LocalService import LocalService

localService = LocalService()
if __name__ == '__main__':
    pass

while True:
    cmd = raw_input("local>")
    #print cmd
    cmd = cmd.split(" ")
    cmd = [item for item in cmd if item != "" and item != " "]
    #print cmd
    op = cmd[0]
    if op == "create":
        if len(cmd) < 3:
            print "usage: create [filename] [size]\n"
        else:
            fileName = cmd[1]
            size = cmd[2]
            localService.create(fileName, size)
    elif op == "delete":
        if len(cmd) < 2:
            print "usage: delete [filename]\n"
        else:
            fileName = cmd[1]
            localService.delete(fileName)
    elif op == "ls":
        localService.ls();
    elif op == "quit":
        break