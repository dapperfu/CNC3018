
from subprocess import check_output
import datetime
import os
from IPython.display import Image, display_jpeg

resolution = "1600x900"


def picture():
    img_root = "images"
    img_name = "{}.jpeg".format(datetime.datetime.now())

    if not os.path.exists(img_root):
        os.makedirs(img_root)

    img_path = os.path.join(img_root, img_name)

    cmd_array = ["streamer", "-c", "/dev/video1", "-s", resolution, "-o", img_path, ]
    cmd_array

    ret = check_output(cmd_array)

    display_jpeg(Image(img_path))
