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
    cmd = [item for item in cmd if item != "" and item != " "]
    #print cmd
    op = cmd[0]
    if op == "create":
        if len(cmd) < 3:
            print "usage: create [filename] [size]\n"
        else:
            fileName = cmd[1]
            size = cmd[2]
            transparentService.create(fileName, size)
    elif op == "delete":
        if len(cmd) < 2:
            print "usage: delete [filename]\n"
        else:
            fileName = cmd[1]
            transparentService.delete(fileName)
    elif op == "open":
        if len(cmd) < 2:
            print "usage: open [filename]\n"
        else:
            fileName = cmd[1]
            transparentService.open(fileName)
    elif op == "ls":
        transparentService.ls();
    elif op == "quit":
        break