
import keras
import tensorflow as tf
import numpy as np
from keras.models import Model
from keras.layers import Input, Conv1D, MaxPooling1D, BatchNormalization, Dense, Flatten
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.optimizers import Adam
from keras.initializers import glorot_uniform
from keras.losses import binary_crossentropy
from keras import backend as K
from keras import losses


def self_crossentropy(y_true, y_pred):
    y_true = K.flatten(y_true)
    y_pred = tf.clip_by_value(K.flatten(y_pred), 1e-7, (1.0 - 1e-7))
    out = -(y_true * K.log(y_pred) + (1.0 - y_true) * K.log(1.0 - y_pred))
    return K.mean(out)

def mean_squared_error(y_true, y_pred):
    return K.mean(K.square(y_pred - y_true), axis=-1)

def clipped_mse(y_true, y_pred):
    return K.mean(K.square(K.clip(y_pred, 0., 1.0) - K.clip(y_true, 0., 1.0)), axis=-1)


def cnn1d(seq_len, channel):

    inputs = Input((seq_len, channel))  # 1024

    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=32, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(inputs)))
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=32, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = MaxPooling1D(pool_size=2)(layer) #512                                                   # 32768
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=64, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=64, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = MaxPooling1D(pool_size=2)(layer)                                                    #256256 

    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=128, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=128, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = MaxPooling1D(pool_size=2)(layer)                                                    #128 

    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=256, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=256, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = MaxPooling1D(pool_size=2)(layer)                                                    #64 

    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=512, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = LeakyReLU()(BatchNormalization()(Conv1D(filters=512, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)))
    layer = MaxPooling1D(pool_size=2)(layer)                                                    #32 


    layer = Flatten()(layer)
    outputs = Dense(1, activation="sigmoid")(layer)
    

    model = Model(inputs=[inputs], outputs=[outputs])

    model.compile(optimizer=Adam(lr=3e-5, beta_1=0.9, beta_2=0.999, decay=0.0), loss=self_crossentropy, metrics=["accuracy"])
    return model


