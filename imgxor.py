from PIL import Image
import numpy as np
from itertools import chain
import utils


def xor_img_data(img_arr:np.ndarray, key:list) -> list:
    """
    takes list of rgb values of image and encrypts it using key

    :param img_arr: list
    :param key: list
    :return: list (encrypted rgb values)
    """
    size = len(img_arr)
    k_len = len(key)
    key = utils.key_mod(key)
    # Repeating key to match the size of the img_array list. this method is faster than previous method
    key = (key*((size//k_len)+1))[:size]
    key = np.array(key).astype('uint8')
    img_arr ^= key # xor'ing each value of img_arr with key value
    return img_arr

def img_to_array(img:Image.Image):
    """
    Takes an image and returns it's rgb values as array

    :param img: PIL.Image.Image
    :return: np.ndarray
    """
    return np.array(img).flatten()

def array_to_img(imgarr:np.ndarray, height:int, width:int):
    """
    Takes array of rgb values and creates an image using the values and returns it

    :param img_list : np.ndarray
    :return: PIL.Image.Image
    """
    return Image.fromarray(imgarr.reshape((height, width, 3)), "RGB")

def encrypt_image(img:Image.Image,key:str="") -> Image.Image:
    """
    Takes an image and key and encrypts the image using key and returns the encrypted image

    :param img: PIL.Image.Image - Image to be encrypted
    :return: PIL.Image.Image - Encrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width , height = img.size
    img_data = img_to_array(scrambler(img, key))
    xored = xor_img_data(img_data,key)
    nimg = array_to_img(xored, height, width)
    return nimg

def decrypt_image(img:Image.Image,key:str) -> Image.Image:
    """
    Takes the image and key, and decrypts the encrypted image using key and returns the decrypted image

    :param img: image to be decrypted
    :param key: encryption key
    :return: PIL.Image.Image - Decrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width, height = img.size
    img_data = img_to_array(img)
    xored = xor_img_data(img_data, key)
    img2 = array_to_img(xored, height=height, width=width)
    data = img_to_array(unscrambler(img2, key))
    nimg = array_to_img(data, height, width)
    return nimg

def resizer(img:Image.Image,max_size:int) -> Image.Image:
    """
    Takes the image and resizes it according the max_size provided while keeping the aspect ratio same as original image.

    :param img: PIL.Image.Image
    :param max_size: int
    :return: PIL.Image.Image - Resized image
    """
    width,height = img.size
    multiplier = max_size/max(width,height)
    new_size = int(multiplier*width),int(multiplier*height)
    return img.resize(new_size)

def scrambler(img,key) -> Image.Image:
    """
    Takes an image and scrambles it and returns the scrambled image
    (this function is inverse of unscrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_array(img)
    seed = utils.get_seed(key[::-1])
    data = utils.scramble(data,seed)
    return array_to_img(data, height=h, width=w)


def unscrambler(img,key) -> Image.Image:
    """
    Takes an image and performs inverse of scrambling algorithm
    i.e unscrambles the scrambled image and returns it
    (this function is inverse of scrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_array(img)
    seed = utils.get_seed(key[::-1])
    data = utils.unscramble(data, seed)
    return array_to_img(data, h, w)

if __name__ == '__main__':
    from tkinter import filedialog as fd

    file = fd.askopenfilename()
    if file:
        pass
    else:
        exit()
    img = Image.open(file)
    ckey = f"{utils.random_KeyGen(30)}"
    print(ckey)
    s = utils.timenow()
    img2 = encrypt_image(img,ckey)
    e = utils.timenow()
    print(e-s)
    img2.show(title="E")
    img2.save("./dump/testing_e5.png")
    print('-----------------------------------')
    ckey2 = str(utils.change(ckey))
    s = utils.timenow()
    img3 = decrypt_image(img2,ckey2)
    e = utils.timenow()
    print(e-s)
    img3.show(title="D")
    print('-----------------------------------')
    s = utils.timenow()
    img3 = decrypt_image(img2,ckey)
    e = utils.timenow()
    print(e-s)
    img3.show()
    img3.save("./dump/testing_d5.png")