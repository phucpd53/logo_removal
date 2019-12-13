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
    mask_3D = np.dstack([mask, mask, mask])
    return y_pred * (1 - mask) + y_true * mask