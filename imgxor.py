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
    k_len = len(key)
    key = utils.key_mod(key)
    k_index = 0
    for i in range(size):
        num = img_arr[i]
        k_char = key[k_index]
        img_arr[i] = num ^ k_char
        k_index = utils.circular_increment(k_index,k_len)
    return img_arr

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
    img_data = img_to_list(scrambler(img))
    xored = xor_img_data(img_data,key)
    return list_to_img(xored,height,width)

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
    img_data = img_to_list(img)
    xored = xor_img_data(img_data, key)
    img2 = list_to_img(xored, height=height, width=width)
    data = img_to_list(unscrambler(img2))
    return list_to_img(data, height, width)

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

def scrambler(img) -> Image.Image:
    """
    Takes an image and scrambles it and returns the scrambled image
    (this function is inverse of unscrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_list(img)
    data = utils.split_and_flip(data)
    newimg = list_to_img(data, height=h, width=w)
    newimg = newimg.rotate(90, expand=1)
    data = utils.split_and_flip(img_to_list(newimg))
    return list_to_img(data, width=h, height=w).rotate(-90,expand=1)

def unscrambler(img) -> Image.Image:
    """
    Takes an image and performs inverse of scrambling algorithm
    i.e unscrambles the scrambled image and returns it
    (this function is inverse of scrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    img = img.rotate(90,expand=1)
    data = utils.split_and_flip(img_to_list(img))
    newimg = list_to_img(data, w, h).rotate(-90, expand=1)
    data = utils.split_and_flip(img_to_list(newimg))
    return list_to_img(data, h, w)

if __name__ == '__main__':
    img = Image.open("./dump/car.png")
    # s1 = scrambler(img)
    # s1.show()
    # s2 = scrambler(s1)
    # s2.show()
    # exit()
    # us1 = unscrambler(s2)
    # us2 = unscrambler(us1)
    # us2.show()
    # exit()
    ################################
    s = utils.timenow()
    # ckey = str(utils.random_KeyGen(254))
    ckey = "[122, 155, 22, 217, 76, 251, 38, 84, 136, 191, 100, 97, 14, 140, 180, 213, 56, 131, 116, 63, 28, 193, 112, 242, 229, 1, 132, 173, 0, 97, 125, 29, 153, 235, 213, 229, 23, 160, 83, 176, 124, 194, 242, 151, 38, 205, 42, 153, 171, 151, 174, 17, 128, 53, 168, 113, 138, 45, 21, 179, 238, 174, 135, 165, 13, 250, 52, 166, 88, 76, 60, 67, 227, 18, 28, 200, 106, 207, 89, 69, 35, 148, 165, 146, 123, 89, 155, 215, 128, 96, 223, 95, 247, 101, 205, 77, 56, 176, 26, 142, 117, 215, 186, 166, 64, 67, 196, 50, 34, 48, 203, 188, 93, 232, 56, 239, 199, 159, 91, 146, 254, 49, 129, 236, 168, 218, 239, 115, 158, 8, 147, 92, 184, 32, 96, 47, 2, 143, 173, 179, 127, 75, 4, 43, 47, 20, 192, 28, 44, 218, 167, 177, 159, 249, 138, 132, 111, 161, 83, 189, 38, 242, 43, 227, 59, 59, 204, 200, 95, 32, 80, 125, 102, 54, 9, 190, 230, 22, 75, 148, 255, 151, 79, 137, 184, 158, 141, 26, 76, 174, 246, 36, 130, 99, 9, 67, 136, 137, 147, 219, 252, 202, 168, 16, 141, 61, 243, 15, 183, 187, 197, 208, 15, 39, 80, 226, 230, 145, 246, 235, 119, 27, 68, 57, 62, 32, 148, 40, 246, 216, 3, 103, 224, 14, 183, 105, 250, 73, 169, 19, 44, 105, 64, 64, 4, 14, 207, 92, 87, 53, 189, 81, 182, 224]"
    print(ckey)
    img2 = encrypt_image(img,ckey)
    e = utils.timenow()
    print(e-s)
    img2.show(title="E")
    img2.save("./dump/testing_e5.png")
    print('-----------------------------------')
    s = utils.timenow()
    ckey2 = "[121, 154, 21, 216, 75, 250, 39, 85, 135, 190, 101, 96, 15, 141, 179, 212, 55, 132, 115, 62, 27, 192, 113, 243, 230, 0, 133, 174, 1, 98, 124, 28, 154, 234, 214, 230, 24, 161, 82, 175, 123, 193, 241, 150, 39, 204, 43, 152, 172, 150, 173, 16, 129, 52, 167, 112, 137, 44, 22, 178, 237, 175, 136, 164, 12, 249, 53, 165, 89, 77, 59, 66, 226, 19, 29, 199, 105, 208, 90, 70, 34, 149, 164, 145, 122, 88, 156, 214, 127, 95, 224, 96, 246, 100, 206, 78, 57, 177, 25, 141, 118, 216, 187, 165, 63, 68, 195, 51, 35, 47, 202, 187, 92, 233, 57, 238, 198, 158, 92, 145, 255, 50, 128, 235, 169, 217, 238, 116, 159, 7, 148, 93, 185, 31, 97, 48, 3, 142, 172, 178, 126, 76, 3, 42, 46, 21, 191, 27, 43, 217, 166, 176, 158, 248, 139, 131, 112, 160, 84, 188, 37, 243, 44, 226, 58, 60, 203, 199, 94, 33, 81, 126, 101, 55, 8, 189, 231, 23, 74, 147, 254, 152, 80, 136, 185, 157, 142, 25, 75, 173, 245, 37, 129, 98, 10, 68, 137, 138, 148, 220, 251, 201, 167, 17, 140, 62, 242, 14, 184, 186, 196, 207, 14, 38, 79, 225, 231, 146, 245, 234, 120, 26, 67, 56, 61, 33, 147, 41, 247, 215, 2, 102, 223, 13, 184, 106, 251, 74, 168, 18, 45, 104, 65, 63, 5, 15, 206, 93, 86, 54, 190, 80, 181, 223]"
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