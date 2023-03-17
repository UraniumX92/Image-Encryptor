from datetime import datetime
from functools import reduce
import numpy as np
import random
import json

bullet_char = "\u2022"

def generate_ascii_values():
    return [chr(num) for num in range(1, 256)]

# ----------------------------------- #
ascii_values = generate_ascii_values()
# ----------------------------------- #

def timenow():
    """
    Current timestamp
    :return: float - timestamp
    """
    return datetime.now().timestamp()

def random_KeyGen(keylen:int) -> list[int]:
    return random.sample(range(256),keylen,counts=[2 for x in range(256)])

def dump_json(object, filename):
    with open(filename, "w") as dump:
        json.dump(object, dump, indent=4)

def load_json(filename):
    with open(filename, "r") as load:
        return json.load(load)

def key_mod(key:int) -> int:
    """
    Modifies the given key before using it for encryption/decryption

    :param key:
    :return:
    """
    return [int(format(x,'08b')[::-1],2) for x in key]

def get_key(strval:str) -> list[int]:
    """
    takes string, tries to decode using json, converts to list
    checks if all the elements in the list are integers or not, if not, then tries to convert the characters to integer using ord().
    if it fails to so.. then entire string will be taken as string key, and each character of this string will be converted to integer and returns as list

    :param strval: str
    :return: list[int]
    """
    k = []
    try:
        k = json.loads(strval)
        if type(k) != type(list()):
            raise json.decoder.JSONDecodeError("not int","",0)
        elif any(type(x) != type(int()) for x in k):
            raise json.decoder.JSONDecodeError("not int","",0)
    except json.decoder.JSONDecodeError:
        k = [abs(ord(x))%256 for x in strval]
    return k

def get_compact_key(strval:str) -> str:
    """
    takes a string, converts it into a list of ints using get_key(),
    then converts this list into string with no spaces and removes the square brackets and returns it

    :param strval:
    :return: str
    """
    return str(get_key(strval)).replace(" ","")

def split_and_flip(array:list,proceed=True) -> list:
    """
    divides the list into 2 halves and flips each half, joins the flipped halves and returns single list
    does the same thing with each half recursively if the list contains even number of items, otherwise only 1 time.
    because array with odd number items cannot be split and obtained back in original form. where as arary with even number items
    can be split recursively and can be obtained as original form of array.

    :param array: list
    :return: list - modified
    """
    size = len(array)
    halfsize_int = size // 2
    h1 = array[:halfsize_int]
    h2 = array[halfsize_int:]
    s1 = halfsize_int
    s2 = size - halfsize_int
    # first half
    if s1%2==0:
        h1 = split_and_flip(h1)
    # second half
    if s2%2==0:
        h2 = split_and_flip(h2)
    return h1[::-1] + h2[::-1]

def get_seed(array:list):
    """
    Obtains the seed from given array and returns it.

    :param array : an array from which seed is to be obtained
    :return: int - seed obtained from the key
    """
    max_seed = 4294967296 # This value is 2**32 and maximum value allowed for np.random.seed()
    def seed_func(a,b):
        """
        function to pass in reduce() to get the seed
        """
        if is_even(a) and is_even(b):
            return (2*a)+b
        elif is_even(a) and is_odd(b):
            return (2*b)+a
        elif is_odd(a) and is_even(b):
            return (b+a)//a
        else: # odd , odd
            return (a*b)+(abs(b-a)//a)
    return (reduce(seed_func,array) + (sum(array)//len(array))) % (max_seed)

def is_even(n):
    return n%2==0

def is_odd(n):
    return n%2!=0

def scramble(data:np.ndarray,seed:int):
    """
    Scrambles the data, using a seed and returns it.

    :param data: data to be scrambled
    :param seed: seed to be used for rng
    :return: modified data
    """
    scrambled = data.copy()
    np.random.seed(seed)
    np.random.shuffle(scrambled)
    # Resetting the seed to default (to avoid problems using random elsewhere)
    np.random.seed()
    return scrambled

def unscramble(scrambled:np.ndarray,seed:int):
    """
    Unscrambles the scrambled data using a seed and returns it.

    :param scrambled: scrambled data
    :param seed: seed to be used for rng
    :return: modified data
    """
    temp = np.arange(len(scrambled))
    s_temp = scramble(temp, seed)
    sorted_indices = np.argsort(s_temp)
    return scrambled[sorted_indices]

def change(key):
    """
    Temp function to use for testing.
    this function changes each value of a given list of integers by +/- 1
    :param key:
    :return:
    """
    key = json.loads(key)
    kl = len(key)
    for i in range(kl):
        value = key[i]
        if value == 255:
            key[i] = 254
        elif value == 0:
            key[i] = 1
        else:
            r = random.randint(0,10)
            if r%2==0:
                key[i] = value + 1
            else:
                key[i] = value -1
    return key
if __name__ == '__main__':
    key = random_KeyGen(30)
    print(key)
    seed = get_seed(key)
    seed2 = get_seed(key[::-1])
    seed3 = get_seed(change(str(key)))
    print(seed)
    print(seed2)
    print(seed3)
    exit()
