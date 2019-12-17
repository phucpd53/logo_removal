import skvideo.io
import imageio
import config
def run():
    images = skvideo.io.vread("1584158644.mp4")
    for i in range(images.shape[0]):
        output_path = os.path.join(config.OUT_DIR, "{:05}.jpg".format(i))
        imageio.imwrite(output_path, images[i])
        yield output_path
    