
import keras
import tensorflow as tf
import numpy as np
from keras.models import Model
from keras.layers import Input, Conv1D, MaxPooling1D, BatchNormalization, Dense, Flatten,concatenate
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
    return K.mean(K.square(K.clip(y_pred, 0., 3.0) - K.clip(y_true, 0., 3.0)), axis=-1)


def cnn1d(seq_len, channel):

    inputA = Input((seq_len, channel))  # 262144
    inputB = Input((20,))

    layer = BatchNormalization()(Conv1D(filters=32, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(inputA)) 
    layer = BatchNormalization()(Conv1D(filters=32, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 32768
    layer = BatchNormalization()(Conv1D(filters=64, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=64, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 16384

    layer = BatchNormalization()(Conv1D(filters=128, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=128, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 8192

    layer = BatchNormalization()(Conv1D(filters=256, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=256, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 4096

    layer = BatchNormalization()(Conv1D(filters=512, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=512, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 2048

    layer = BatchNormalization()(Conv1D(filters=1024, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=1024, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 1024

    layer = BatchNormalization()(Conv1D(filters=2048, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=2048, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 512

    layer = BatchNormalization()(Conv1D(filters=2048, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=2048, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 256

    layer = BatchNormalization()(Conv1D(filters=4096, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = BatchNormalization()(Conv1D(filters=4096, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 
    layer = MaxPooling1D(pool_size=2)(layer)                                                    # 128

    layer = BatchNormalization()(Conv1D(filters=4096, kernel_size=3, activation="relu", kernel_initializer=glorot_uniform(),padding='same')(layer)) 

    layer = Flatten()(layer)
    #print(layer.get_shape())
    #print(type(inputB))
    #print(inputB.get_shape())
    #print(type(layer))

#    layer=Reshape(layer,(-1,524288))
    layer=concatenate([layer,inputB])
    #print(layer.get_shape())
    #outputs = Dense(10, activation="relu")(inputB)
    outputs = Dense(10, activation="relu")(layer)
    outputs = Dense(10, activation="relu")(layer)
#    outputs = Dense(1, activation="sigmoid")(layer)
    outputs = Dense(1, activation="relu")(layer)

    model = Model(inputs=[inputA,inputB], outputs=[outputs])
    model.compile(optimizer=Adam(lr=3e-5, beta_1=0.9, beta_2=0.999, decay=0.0), loss=clipped_mse, metrics=["accuracy"])

    return model 

