from __future__ import print_function
import os
import sys
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
from keras.models import Model
from keras.layers import Input, concatenate, Conv1D, MaxPooling1D, Conv2DTranspose,Lambda
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras import backend as K
import tensorflow as tf
import keras
#import cv2
import scipy.io
import math

sys.path.append("../../model/")

import cnn_sigmoid_leaky_1024 as cnn
from keras.backend.tensorflow_backend import set_session
#config = tf.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.45
#set_session(tf.Session(config=config))

K.set_image_data_format('channels_last')  # TF dimension ordering in this code
path1=sys.argv[2]
size=512

channel=3
batch_size=64
ss = 1

import random
model = cnn.cnn1d(size,3)

max_scale=1.3
min_scale=0.8


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
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)], [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)], [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


def rotateC(image,theta,a,b,c): ## theta: angle, a, b, c, eular vector
    axis=norm_axis(a,b,c)
    imagenew=np.dot(image, rotation_matrix(axis,theta))
    return imagenew

def scaleImage(image,scale):
    [x,y]= image.shape
    y1=int(y*scale)
    x1=3
    image=cv2.resize(image,(y1,x1))
    new=np.zeros((x,y))
    if (y1>y):
        start=0
        end=start+y
        new=image[:,start:end]
    else:
        new_start=0
        new_end=new_start+y1
        new[:,new_start:new_end]=image
    return new
  

all_ids=open(sys.argv[1],'r')
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

random.shuffle(all_line)
partition_ratio=0.8
train_line=all_line[0:int(len(all_line)*partition_ratio)]
test_line=all_line[int(len(all_line)*partition_ratio):len(all_line)]


def generate_data(train_line, batch_size, if_train):
    """Replaces Keras' native ImageDataGenerator."""
##### augmentation parameters ######
    i = 0
    while True:
        image_batch = []
        label_batch = []
        for b in range(batch_size):
            if i == len(train_line):
                i = 0
                random.shuffle(train_line)
            sample = train_line[i]
            i += 1
            table=sample.split('\t')
            the_id=table[1]
            #print(path1 + the_id)
            image = np.loadtxt(path1 + the_id, delimiter=',',skiprows=1)[:,1:4]

            rrr=random.random() 
            rrr_scale=rrr*(max_scale-min_scale)+min_scale 
            if (if_train==1):
            #        seq=scaleImage(seq,rrr_scale)
#                theta=random.random()*math.pi*2
                theta=random.random()*360
                #print(theta)
                a=random.random()
                b=random.random()
                c=random.random()
                image=rotateC(image,theta,a,b,c)
            image_pad=np.zeros((size,3))
            image_pad[0:image.shape[0],:]=image
            if (the_max-the_min)==0:
                label=0.5
            else:
                label=(float(table[0])-the_min)/(the_max-the_min)
            image_batch.append(image_pad)
            label_batch.append(label)
        image_batch=np.array(image_batch)
        label_batch=np.array(label_batch)
#        print(image_batch.shape,label_batch.shape)
        yield image_batch, label_batch

#model_checkpoint = ModelCheckpoint('weights.h5', monitor='val_loss', save_best_only=False)
name_model='weights_' + sys.argv[3] + '.h5'
callbacks = [
#    keras.callbacks.TensorBoard(log_dir='./',
#    histogram_freq=0, write_graph=True, write_images=False),
    keras.callbacks.ModelCheckpoint(os.path.join('./', name_model),
    verbose=0, save_weights_only=False,save_best_only=True,monitor='val_loss')
    ]

model.fit_generator(
    generate_data(train_line, batch_size,True),
    steps_per_epoch=int(len(train_line) // batch_size), nb_epoch=10,
    validation_data=generate_data(test_line,batch_size,False),
    validation_steps=int(len(test_line) // batch_size),callbacks=callbacks)

