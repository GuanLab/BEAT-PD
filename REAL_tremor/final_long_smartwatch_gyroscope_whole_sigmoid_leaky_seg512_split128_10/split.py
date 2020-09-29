import glob
import random
import sys

random.seed(sys.argv[1])
### randomly select 3 always in test;
REF=open('../../../rawdata_new/real-pd.data_labels/REAL-PD_Training_Data_IDs_Labels.csv','r')
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
    if (rrr<-0.4):
        test_id[the_id]=1;



REF=open('../../../rawdata_new/real-pd.data_labels/REAL-PD_Training_Data_IDs_Labels.csv','r')
TRAIN=open('train_gs.dat','w')
TEST=open('test_gs.dat','w')
line=REF.readline()
for line in REF:
    line=line.strip()
    table=line.split(',')
    rrr=random.random()
    if 'NA' in table[4]:
        pass
    else:
        if (table[1] in test_id):
            TEST.write(table[4])
            TEST.write('\t')
            TEST.write(table[0])
            TEST.write('\t')
            TEST.write(table[1])
            TEST.write('\n')
        else:
            if (rrr<1.75):
                TRAIN.write(table[4])
                TRAIN.write('\t')
                TRAIN.write(table[0])
                TRAIN.write('\t')
                TRAIN.write(table[1])
                TRAIN.write('\n')
            else:
                TEST.write(table[4])
                TEST.write('\t')
                TEST.write(table[0])
                TEST.write('\t')
                TEST.write(table[1])
                TEST.write('\n')

REF=open('../../../testdata/real-pd.REAL-PD_Test_Data_IDs.csv','r')
TEST=open('test_gs.dat','w')
line=REF.readline()
for line in REF:
    line=line.strip()
    table=line.split(',')
    rrr=random.random()
    TEST.write(table[0])
    TEST.write('\t')
    TEST.write(table[0])
    TEST.write('\t')
    TEST.write(table[1])
    TEST.write('\n')




