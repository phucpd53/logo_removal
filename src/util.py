import os
import numpy as np
import skvideo.io
import imageio
import cv2

def read_video_to_frame(video_path):
    frames = skvideo.io.vread(video_path)
    return frames

def detect_fpt_logo(img, logo_img):
    '''
    @return 
        mask_img with logo region is 0, otherwise 1. SHAPE = [HEIGHT, WIDTH, 1]
    '''
    pass

def reconstruct(y_pred, y_true, mask):
    '''
    y_pred: image generated from CNN. SHAPE = [HEIGHT, WIDTH, 3]
    y_true: input image with logo. SHAPE = [HEIGHT, WIDTH, 3]
    mask: a binary image with logo region is 0, otherwise 1. SHAPE = [HEIGHT, WIDTH, 1]
    '''
    mask = cv2.gaussian_blur(mask, (3, 3), 0)
    mask_3D = np.dstack([mask, mask, mask])
    return (y_pred * (1 - mask_3D) + y_true * mask_3D).astype(np.uint8)

def generate_x(height, width):
    '''
    generate a fix matrix as below. SHAPE = [HEIGHT, WIDTH, 2]
    then use it as prior for CNN to generate a new image.
    '''
    y = np.linspace(0.0, 1.0, height)
    x = np.linspace(0.0, 1.0, width)
    XX, YY = np.meshgrid(x, y)
    input_meshgrid = np.concatenate([XX[:,:,np.newaxis], YY[:,:,np.newaxis]], axis=2)
    return input_meshgrid