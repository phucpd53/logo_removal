import os
import imageio
import cv2
import numpy as np
from keras.layers import Input, Lambda
from keras import backend as K
from keras.models import Model, load_model
from keras.optimizers import Adam
import time
import io
import matplotlib.pyplot as plt

from src import model_class
from src import util
import config
from threading import Thread

class Logo_removal:
    def __init__(self, file_path):
        self.file_path = file_path
    def _run(self):
        # input image
        image = imageio.imread(self.file_path, pilmode="RGB")
        image = cv2.resize(image, (1152, 768))
        HEIGHT, WIDTH = image.shape[:2]
        logo_img = imageio.imread("input/logo-ft.png", pilmode="RGB")
        mask_image = util.detect_logo(image, logo_img)
        if config.DEBUG:
            imageio.imwrite("mask.png", mask_image * 255)

        # define model
        target_tensor = Input(shape=(HEIGHT, WIDTH, 3))
        mask_tensor = Input(shape=(HEIGHT, WIDTH, 1))   
        base_model = model_class.my_model(input_shape=[HEIGHT, WIDTH, config.INPUT_DIM])
        loss = Lambda(lambda x: K.sum(K.square((x[0] - x[1]) * x[2]), axis=-1))([base_model.output, target_tensor, mask_tensor])
        model = Model([base_model.input, target_tensor, mask_tensor], loss)
        model.compile(loss="mae", optimizer=Adam(config.LEARNING_RATE))

        # training
        x_train = util.generate_x(height=HEIGHT, width=WIDTH)
        y_train = image
        res = 1000
        i = 0
        while res > 100:
            buf = io.BytesIO()
            i += 1
            res = model.train_on_batch(
                x=[x_train[None, :, :, :], y_train[None, :, :, :], mask_image[None, :, :, None]],
                y=np.zeros((1, HEIGHT, WIDTH)), # dummy params. True loss is calculated from x only
            )
            if i % 100 == 0:
                print("Iteration: {}, Loss: {}".format(i, res))
                out_img = base_model.predict(x_train[None, :, :, :], steps=1)[0]
                out_img = np.clip(out_img, 0, 255).astype(np.uint8)
                
                result = util.reconstruct(y_pred=out_img, y_true=y_train, mask=mask_image, iteration=i, loss=res)
                plt.imsave(buf, result)
                imageio.imwrite(os.path.join(config.OUT_DIR, "result.jpg"), result[:HEIGHT, :WIDTH, :])
                time.sleep(1)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buf.getvalue() + b'\r\n')