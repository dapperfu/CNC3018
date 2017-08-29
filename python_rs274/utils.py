
from subprocess import check_output

resolution = "1600x900"

def picture():
    img_root = "images"
    img_name = "{}.jpeg".format(datetime.datetime.now())

    if not os.path.exists(img_root):
        os.makedirs(img_root)
        
    img_path = os.path.join(img_root, img_name)

    cmd_array = ["streamer", "-s", resolution, "-o", img_path, ]
    cmd_array

    ret  = check_output(cmd_array)
    
    display_jpeg(Image(img_path))