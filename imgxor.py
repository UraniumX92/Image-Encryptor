from PIL import Image
from itertools import chain
import utils


def xor_img_data(img_arr:list, key:list) -> list:
    """
    takes list of rgb values of image and encrypts it using key

    :param img_arr: list
    :param key: list
    :return: list (encrypted rgb values)
    """
    size = len(img_arr)
    e_list = []
    k_len = len(key)
    k_index = 0
    for i in range(size):
        num = img_arr[i]
        k_char = key[k_index]
        e_list.append(num ^ k_char)
        k_index = utils.circular_increment(k_index,k_len)
    return e_list

def img_to_list(img:Image.Image) -> list:
    """
    Takes an image and returns it's rgb values as list

    :param img: PIL.Image.Image
    :return: list
    """
    data = list(img.getdata())
    flat = list(chain.from_iterable(data))
    return flat

def list_to_img(img_list:list,height:int,width:int) -> Image.Image:
    """
    takes list of rgb values and creates an image using the values and returns it

    :param img_list : list
    :return: PIL.Image.Image
    """
    return Image.frombytes("RGB", (width,height), bytes(img_list))

def encrypt_image(img:Image.Image,key:str="") -> Image.Image:
    """
    Takes an image and key and encrypts the image using key and returns the encrypted image

    :param img: PIL.Image.Image - Image to be encrypted
    :return: PIL.Image.Image - Encrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width , height = img.size
    img_data = img_to_list(img)
    img_data = utils.split_and_flip(img_data)
    xored = xor_img_data(img_data,key)
    ximg = list_to_img(xored,height,width)
    return ximg

def decrypt_image(img:Image.Image,key:str) -> Image.Image:
    """
    Takes the image and key, and decrypts the encrypted image using key and returns the decrypted image

    :param img: image to be decrypted
    :param key: encryption key
    :return: decrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width, height = img.size
    img_data = img_to_list(img)
    xored = xor_img_data(img_data, key)
    xored = utils.split_and_flip(xored)
    ximg = list_to_img(xored, height, width)
    return ximg

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

if __name__ == '__main__':
    img = Image.open("./dump/car.png")
    # newimg = resizer(img,400)
    # newimg.show()
    # newimg.save("./dump/resized.png")
    # exit()
    ################################
    # l = img_to_list(img)
    # l = utils.split_and_flip(l)
    # i2 = list_to_img(l,img.height,img.width)
    # i2.show()
    ################################
    s = utils.timenow()
    ckey = str(utils.random_KeyGen(254))
    img2 = encrypt_image(img,ckey)
    e = utils.timenow()
    print(e-s)
    img2.show(title="E")
    img2.save("./dump/testing_e4.png")
    print('-----------------------------------')
    s = utils.timenow()
    img3 = decrypt_image(img2,ckey)
    e = utils.timenow()
    print(e-s)
    img3.show(title="D")
    img3.save("./dump/testing_d4.png")