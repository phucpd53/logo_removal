import skvideo.io
import imageio
import config
import os
import time
import io
import matplotlib.pyplot as plt

def run():
    images = skvideo.io.vread("input/mask.avi")
    for i in range(0, 10):
        buf = io.BytesIO()
        plt.imsave(buf, images[i])
        time.sleep(1)
        # yield "{:05}.jpg".format(i)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.getvalue() + b'\r\n')

    