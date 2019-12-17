import skvideo.io
import imageio
import config
import os
def run(input_path):
    images = skvideo.io.vread("input/1584158644.mp4")
    for i in range(images.shape[0]):
        output_path = os.path.join(config.OUT_DIR, "{}".format(os.path.basename(input_path)))
        imageio.imwrite(output_path, images[i])
    