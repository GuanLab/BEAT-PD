#!/usr/bin/env python
import os
import sys
import logging
import numpy as np
import time
import scipy.io
import glob
import pickle
from keras.utils.np_utils import to_categorical
from keras import backend as K
import tensorflow as tf
import keras
# import cv2
from keras.backend.tensorflow_backend import set_session
sys.path.append("../../model/")
import cnn_sigmoid_leaky_1024 as cnn
print('example 262144 ../../../processedData/real-pd.training_data/smartphone_accelerometer/')
(the_file, the_path)=(sys.argv[1],sys.argv[2])
size=512

# set fraction of GPU the program can use
#config = tf.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.4
#set_session(tf.Session(config=config))

# set the value of data format convention
K.set_image_data_format('channels_last')  # TF dimension ordering in this code

# handles for txt files
all_ids=open(the_file,'r')
the_max=-100
the_min=100
all_line=[]
for line in all_ids:
    all_line.append(line.rstrip())
    table=line.split('\t')
    if (float(table[0])>the_max):
        the_max=float(table[0])
    if (float(table[0])<the_min):
        the_min=float(table[0])
all_ids.close()

# read into arousal data (arousal data is only helper data, help to determine the sleep length)

# load models
all_models=glob.glob('weights_*.h5')
for the_model in all_models:
    model = cnn.cnn1d(size,3)
    model.load_weights(the_model)
    path1=the_path
    the_file=the_file.replace('train','test')
    all_test_files=open(the_file,'r')
    PRED=open(('prediction.dat.'+the_model),'w')
    for test_line in all_test_files:
        sample = test_line
        table=sample.split('\t')
        the_id=table[1]
        image = np.loadtxt((path1 + the_id),delimiter=',',skiprows=1)[:,1:4]

        image_pad=np.zeros((size,3))
        image_pad[0:image.shape[0],:]=image
        image_batch=[]
        image_batch.append(image_pad)
        image_batch=np.asarray(image_batch)

        output = model.predict(image_batch)
        if (the_max-the_min)==0:
            output=the_max
        else:
            output=output*(the_max-the_min)+the_min
            # below are not modified
        PRED.write('%.4f\n' % output)
    PRED.close()
