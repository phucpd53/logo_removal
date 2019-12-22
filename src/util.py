import os
import numpy as np
import skvideo.io
import imageio
import cv2

def read_video_to_frame(video_path):
    frames = skvideo.io.vread(video_path)
    return frames

def detect_logo(img, logo_img, scale=1.1):
    '''
    scale: scale up bbox x times (default: 1.1 times) to make sure it can cover all logo
    @return: mask image with 0 including logo region and 1 including others. Shape of [HEIGHT, WIDTH, 1]
    '''
    best_val = -1
    ori_h, ori_w = logo_img.shape[:2]
    for i in range(img.shape[0]//50, img.shape[0] // 2, img.shape[0]//100):
        h = i
        w = int(ori_w / ori_h * h)
        template = cv2.resize(logo_img, (w, h))
        # Apply template Matching
        res = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= best_val:
            best_val = max_val
            center_x = max_loc[0] + w // 2 
            center_y = max_loc[1] + h // 2 
            top_left = (max(0, center_x - int(w / 2 * scale)), max(0, center_y - int(h / 2 * scale)))
            bottom_right = (min(img.shape[1], center_x + int(w / 2 * scale)), min(img.shape[0], center_y + int(h / 2 * scale)))
    mask = np.ones((img.shape[:2]), np.uint8)
    mask[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]] = 0
    return mask

# TODO: test the drawing function
def reconstruct(y_pred, y_true, mask, iteration, loss):
    '''
    y_pred: image generated from CNN. SHAPE = [HEIGHT, WIDTH, 3]
    y_true: input image with logo. SHAPE = [HEIGHT, WIDTH, 3]
    mask: a binary image with logo region is 0, otherwise 1. SHAPE = [HEIGHT, WIDTH, 1]
    '''
    h, w, c = y_pred.shape
    result = np.ones(((int)(h * 1.1), w, 3), dtype=np.uint8) * 255
    confidence_score = (1 - np.sqrt(loss/(w*h))) * 100
    text = "iteration: {}, matched rate: {:0.2f}%".format(iteration, confidence_score)
    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (int(w / 20), int(h + (h / 20)))
    fontScale = 1
    color = (0, 0, 0) 
    thickness = 2
    cv2.putText(result, text, org, cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, thickness, cv2.LINE_AA)
    
    mask = cv2.GaussianBlur(mask, (7,7), cv2.BORDER_DEFAULT)
    mask_3D = np.dstack([mask, mask, mask])
    result[:h, :w, :c] = (y_pred * (1 - mask_3D) + y_true * mask_3D).astype(np.uint8)
    return result

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