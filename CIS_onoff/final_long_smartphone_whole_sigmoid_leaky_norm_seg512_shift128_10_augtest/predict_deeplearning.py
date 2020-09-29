#!/usr/bin/env python
import os
import sys
import random
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
import math
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

def norm_axis(a,b,c):
    newa=a/(math.sqrt(float(a*a+b*b+c*c)))
    newb=b/(math.sqrt(float(a*a+b*b+c*c)))
    newc=c/(math.sqrt(float(a*a+b*b+c*c)))
    return ([newa,newb,newc])

def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)], [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)], [2*(bd+ac), 2*(cd-ab
), aa+dd-bb-cc]])


def rotateC(image,theta,a,b,c): ## theta: angle, a, b, c, eular vector
    axis=norm_axis(a,b,c)
    imagenew=np.dot(image, rotation_matrix(axis,theta))
    return imagenew
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
        image_ori = np.loadtxt((path1 + the_id),delimiter=',',skiprows=1)[:,1:4]
        the_mean=np.mean(image_ori,axis=0)
        the_std=np.std(image_ori,axis=0)
        image_ori=(image_ori-the_mean)/the_std


        image_batch=[]
        aug=0
        while(aug<5):
            theta=random.random()*360
            #print(theta)
            a=random.random()
            b=random.random()
            c=random.random()
            image=rotateC(image_ori,theta,a,b,c)

            image_pad=np.zeros((size,3))
            image_pad[0:image.shape[0],:]=image

            image_batch.append(image_pad)
            aug=aug+1
        image_batch=np.asarray(image_batch)


        output = model.predict(image_batch)
        output=np.mean(output)
        if (the_max-the_min)==0:
            output=the_max
        else:
            output=output*(the_max-the_min)+the_min
            # below are not modified
        PRED.write('%.4f\n' % output)
    PRED.close()

