import glob
import random
import sys

random.seed(sys.argv[1])
### randomly select 3 always in test;
REF=open('../../../rawdata/cis-pd.data_labels/CIS-PD_Training_Data_IDs_Labels.csv','r')
line=REF.readline()
all_id={}
for line in REF:
    line=line.strip()
    table=line.split(',')
    all_id[table[1]]=0
ids=all_id.keys()
REF.close()

test_id={}
for the_id in ids:
    rrr=random.random()
    if (rrr<-0.2):
        test_id[the_id]=1;



REF=open('../../../rawdata/cis-pd.data_labels/CIS-PD_Training_Data_IDs_Labels.csv','r')
TRAIN=open('train_gs.dat','w')
TEST=open('test_gs.dat','w')
line=REF.readline()
for line in REF:
    line=line.strip()
    table=line.split(',')
    rrr=random.random()
    if 'NA' in table[2]:
        pass
    else:
        if (table[1] in test_id):
            TEST.write(table[2])
            TEST.write('\t')
            TEST.write(table[0])
            TEST.write('\t')
            TEST.write(table[1])
            TEST.write('\n')
        else:
            if (rrr<1.75):
                TRAIN.write(table[2])
                TRAIN.write('\t')
                TRAIN.write(table[0])
                TRAIN.write('\t')
                TRAIN.write(table[1])
                TRAIN.write('\n')
            else:
                TEST.write(table[2])
                TEST.write('\t')
                TEST.write(table[0])
                TEST.write('\t')
                TEST.write(table[1])
                TEST.write('\n')






REF=open('../../../testdata/cis-pd.CIS-PD_Test_Data_IDs.csv','r')
TEST=open('test_gs.dat','w')
line=REF.readline()
for line in REF:
    line=line.strip()
    table=line.split(',')
    TEST.write('0')
    TEST.write('\t')
    TEST.write(table[0])
    TEST.write('\t')
    TEST.write(table[1])
    TEST.write('\t')
    TEST.write('0')
    TEST.write('\t')
    TEST.write('0')
    TEST.write('\t')
    TEST.write('0')
    TEST.write('\n')

