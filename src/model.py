import numpy as np
import cv2
from keras.layers import Input, Convolution2D, MaxPooling2D, Activation,GlobalAveragePooling2D,\
                        Dropout, Dropout, Flatten, Dense, Lambda, BatchNormalization, AveragePooling2D, UpSampling2D, LeakyReLU
from keras.applications.inception_v3 import InceptionV3
from keras import backend as K
from keras.models import Model, load_model
from keras.optimizers import Adam
from keras.losses import mean_squared_error
import tensorflow as tf
import config

def conv2D_block(x, filter, kernel_size):
    x = Convolution2D(filter, kernel_size, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = AveragePooling2D()(x)
    return x
def deconv2D_block(x, filter, kernel_size):
    x = Convolution2D(filter, kernel_size, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = UpSampling2D(interpolation="bilinear")(x)
    return x

def my_model(input_shape=config.INPUT_SHAPE):
    # input layer
    input_tensor = Input(input_shape, name='input_tensor')
    # downsampling
    x = conv2D_block(input_tensor, 128, 3)
    x = conv2D_block(x, 128, 3)
    x = conv2D_block(x, 128, 3)
    x = conv2D_block(x, 128, 3)
    x = conv2D_block(x, 256, 3)

    # upsampling
    x = deconv2D_block(x, 256, 3)
    x = deconv2D_block(x, 128, 3)
    x = deconv2D_block(x, 128, 3)
    x = deconv2D_block(x, 128, 3)
    x = deconv2D_block(x, 128, 3)

    #output layer
    output_tensor = Convolution2D(3, 1)(x)
    
    model = Model(input_tensor, output_tensor)
    return model