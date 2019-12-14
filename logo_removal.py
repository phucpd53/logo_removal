import os
import imageio
from skimage.transform import resize
import numpy as np
from keras.layers import Input, Lambda
from keras import backend as K
from keras.models import Model, load_model
from keras.optimizers import Adam

from src import model_class
from src import util
import config

def run(input_path):
    # input image
    image = imageio.imread(input_path)
    HEIGHT, WIDTH = image.shape[:2]
    mask_image = imageio.imread("input/mask.jpg")
    mask_image = resize(mask_image, (HEIGHT, WIDTH))
    
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
        i += 1
        res = model.train_on_batch(
            x=[x_train[None, :, :, :], y_train[None, :, :, :], mask_image[None, :, :, None]],
            y=np.zeros((1, HEIGHT, WIDTH)), # dummy params. True loss is calculated from x only
        )
        if i % 100 == 0:
            print("Iteration: {}, Loss: {}".format(i, res))
            out_img = base_model.predict(x_train[None, :, :, :], steps=1)[0]
            out_img = np.clip(out_img, 0, 255).astype(np.uint8)
            
            result = util.reconstruct(y_pred=out_img, y_true=y_train, mask=mask_image)
            imageio.imwrite(os.path.join(config.OUT_DIR, "{:05}.jpg".format(i)), result)