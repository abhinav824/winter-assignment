from PIL import Image

def get_resized_image(file):

    im=Image.open(file)
    x=im.size[0]
    y=im.size[1]
    x_n=360
    y_n=int(540*(y/x))
    im=im.resize((x_n,y_n),Image.ANTIALIAS)
    return im
