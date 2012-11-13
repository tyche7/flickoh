#!/usr/bin/python

import json
import os
import sys

## Partition a json file of tweets into smaller files
## with num_items number of tweets, stored in the folder
## "filename".

def partition_response_file(num_items, filename):
    part = 1;
    prefix = filename.split('.')[0]
    ff = open(filename, 'r')
    os.mkdir('./'+prefix)
    break_while = False
    while (True):
        part_file = open(prefix+'/'+filename.split('.')[0]+'_part'+str(part)+".json", 'w')
        part_file.write('{ "data" : [')
        ending = "\n"
        for i in range(num_items):
            temp = ff.readline()
            if (temp == None or len(temp)<4):
                break_while = True
                break
            if (temp[0] == '{' and temp[-3:] == '},\n'):
                part_file.write(ending)
                ending = ",\n"
                part_file.write(temp[:-2])
                ff.readline()
            else :               
                break_while = True
                break
        part_file.write(']}')
        part_file.close()
        part = part+1
        if (break_while): break
    ff.close()
    
if __name__ == '__main__':
    partition_response_file(int(sys.argv[1]), str(sys.argv[2]))
