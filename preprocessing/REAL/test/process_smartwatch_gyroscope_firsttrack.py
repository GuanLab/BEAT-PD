import glob 
import numpy as np
import sys
import os
os.system('rm -rf smartwatch_gyroscope_firsttrack')
os.system('mkdir smartwatch_gyroscope_firsttrack')

all_files=glob.glob('smartwatch_gyroscope/*')
for the_file in all_files:
    name=the_file.split('/')
    FILE=open(the_file,'r')
    line=FILE.readline()
    NEW=open('smartwatch_gyroscope_firsttrack/'+name[-1],'w')
    NEW.write(line)
    line=FILE.readline()
    line=line.strip()
    table=line.split(',')
    old=table[1]
    NEW.write(table[0])
    NEW.write(',')
    NEW.write(table[2])
    NEW.write(',')
    NEW.write(table[3])
    NEW.write(',')
    NEW.write(table[4])
    NEW.write('\n')

    for line in FILE:
        table=line.split(',')
        line=line.strip()
        if (table[1] == old):
            NEW.write(table[0])
            NEW.write(',')
            NEW.write(table[2])
            NEW.write(',')
            NEW.write(table[3])
            NEW.write(',')
            NEW.write(table[4])
            NEW.write('\n')
    NEW.close()
    FILE.close()

        


