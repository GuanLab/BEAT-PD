#!/usr/bin/env python
import os
import sys
import logging
import numpy as np
import cv2
import time
import theano
from theano import tensor as T
import lasagne

#size=int(sys.argv[2])
path1=sys.argv[1]
eva=open ('train_pred.txt','w')
size=4000

the_map={}
MAP=open('the_map.dat','r')
for line in MAP:
    line=line.strip()
    table=line.split('\t')
    the_map[table[0]]=int(table[1])
MAP.close()

if __name__ == '__main__':
    model = 'guan_version1_4000'
    params = 'params'

    import pkgutil
    loader = pkgutil.get_importer('/ssd/gyuanfan/PDDB/code_pull/model')
    # load network from file in 'models' dir
    model = loader.find_module(model).load_module(model)

    input_var = T.tensor3('input')
    label_var= T.ivector('label')
    shape=(1,3,size)
    
    net, _, _,_ = model.network(input_var, label_var, shape)

    # load saved parameters from "params"
    with open('params', 'rb') as f:
        import pickle
        params = pickle.load(f)
        lasagne.layers.set_all_param_values(net, params)
        pass

    output_var = lasagne.layers.get_output(net, deterministic=True)
    pred = theano.function([input_var], output_var)
    
    TEST=open('train_gs.dat','r')
    for line in TEST:
        line=line.strip()
        table=line.split('\t')
        #image = cv2.imread(table[0], cv2.IMREAD_GRAYSCALE)
        eva.write('%s' % table[0])

## get all 500 sequences;
        the_id=table[1]
        image = np.loadtxt(path1 + the_id + '.csv')[:,1:4]
        i=0
        the_sum=0
        the_count=0
        vector=np.zeros(31)
        iii=0
        while ((i<len(image)-4000)):
            data=image[i:(i+2000),:]
            data_mean=np.mean(data,axis=0)
            data=(data-data_mean)/np.std(data,axis=0)
            sub_data=np.zeros((4000,3))
            sub_data[0:2000,:]=data
            sub_data=sub_data.T
            input_pred=[]
            input_pred.append(sub_data)
            input_pred=np.asarray(input_pred,dtype='float32')
            output = pred(input_pred)
            vector[iii]=output
            i=i+2000
            iii=iii+1
        vector=np.sort(vector)

        for vvv in vector:
            eva.write('\t%.4f' % vvv)

        eva.write('\n')
        pass
    


