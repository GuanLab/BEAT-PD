import numpy as np
import glob

import os
import sys
os.system('rm *.train.dat')
ALL=open(('all.train.dat'),'w')
FILE=open('train_gs.dat','r')
line=FILE.readline()
line=line.strip()
table=line.split('\t')
NEW=open((table[2]+'.train.dat'),'w')
old=table[2]

print(sys.argv[1]+'*'+table[1]+'.csv')
try:
    all_file=glob.glob(sys.argv[1]+'*'+table[1]+'.csv')
    for the_file in all_file:

        ALL.write(table[0])
        ALL.write('\t')
        ALL.write(the_file)
        ALL.write('\t')
        ALL.write(table[2])
        ALL.write('\n')
        
        NEW.write(table[0])
        NEW.write('\t')
        NEW.write(the_file)
        NEW.write('\t')
        NEW.write(table[2])
        NEW.write('\n')
except:
    pass
    
for line in FILE:
    line=line.strip()
    table=line.split('\t')
    if (table[2] ==old):
        try:
            all_file=glob.glob(sys.argv[1]+'*'+table[1]+'.csv')
            for the_file in all_file:

                ALL.write(table[0])
                ALL.write('\t')
                ALL.write(the_file)
                ALL.write('\t')
                ALL.write(table[2])
                ALL.write('\n')
                
                NEW.write(table[0])
                NEW.write('\t')
                NEW.write(the_file)
                NEW.write('\t')
                NEW.write(table[2])
                NEW.write('\n')
        except:
            pass

    else:
        
        old=table[2]
        NEW.close()
        NEW=open((table[2]+'.train.dat'),'w')
        try:
            all_file=glob.glob(sys.argv[1]+'*'+table[1]+'.csv')
            for the_file in all_file:

                ALL.write(table[0])
                ALL.write('\t')
                ALL.write(the_file)
                ALL.write('\t')
                ALL.write(table[2])
                ALL.write('\n')
                
                NEW.write(table[0])
                NEW.write('\t')
                NEW.write(the_file)
                NEW.write('\t')
                NEW.write(table[2])
                NEW.write('\n')

        except:
            pass

