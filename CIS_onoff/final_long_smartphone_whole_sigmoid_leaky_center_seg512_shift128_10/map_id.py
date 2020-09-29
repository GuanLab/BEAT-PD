import numpy as np

FILE=open('train_gs.dat','r')
the_map={}
map_id=0
for line in FILE:
    line=line.rstrip()
    table=line.split('\t')
    if (table[2] in the_map):
        pass
    else:
        the_map[table[2]]=map_id
        map_id=map_id+1
  
FILE=open('test_gs.dat','r')
for line in FILE:
    line=line.rstrip()
    table=line.split('\t')
    if (table[2] in the_map):
        pass
    else:
        the_map[table[2]]=map_id
        map_id=map_id+1
  

FILE=open('train_gs.dat','r')
NEW=open('train_id_feature.dat','w')
for line in FILE:
    line=line.rstrip()
    table=line.split('\t')
    NEW.write(table[0])
    NEW.write('\t')
    NEW.write(str(the_map[table[2]]))
    NEW.write('\n')

FILE=open('test_gs.dat','r')
NEW=open('test_id_feature.dat','w')
for line in FILE:
    line=line.rstrip()
    table=line.split('\t')
    NEW.write(table[0])
    NEW.write('\t')
    NEW.write(str(the_map[table[2]]))
    NEW.write('\n')
