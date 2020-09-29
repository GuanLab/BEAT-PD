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

sys.path.append("../../model/")

import cnn_240599 as cnn
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.45
set_session(tf.Session(config=config))

K.set_image_data_format('channels_last')  # TF dimension ordering in this code
(size,fold, path1)=(sys.argv[1],sys.argv[2],sys.argv[3])
size=int(size)

channel=3
batch_size=2
ss = 1

import random
model = cnn.cnn1d(size,3)

all_ids=open('train_gs.dat','r')
all_line=[]
for line in all_ids:
    all_line.append(line.rstrip())
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
            image = np.loadtxt(path1 + the_id + '.csv')[:,1:4]
            image_pad=np.zeros((size,3))
            image_pad[0:image.shape[0],:]=image
            label=int(table[0])
            if (if_train==1):
                #augmentation part
                pass

            image_batch.append(image_pad)
            label_batch.append(label)
        image_batch=np.array(image_batch)
        label_batch=np.array(label_batch)
#        print(image_batch.shape,label_batch.shape)
        yield image_batch, label_batch

#model_checkpoint = ModelCheckpoint('weights.h5', monitor='val_loss', save_best_only=False)
name_model='weights_' + sys.argv[2] + '.h5'
callbacks = [
#    keras.callbacks.TensorBoard(log_dir='./',
#    histogram_freq=0, write_graph=True, write_images=False),
    keras.callbacks.ModelCheckpoint(os.path.join('./', name_model),
    verbose=0, save_weights_only=False,monitor='val_loss')
    ]

model.fit_generator(
    generate_data(train_line, batch_size,True),
    steps_per_epoch=int(len(train_line) // batch_size), nb_epoch=10,
    validation_data=generate_data(test_line,batch_size,False),
    validation_steps=int(len(test_line) // batch_size),callbacks=callbacks)

