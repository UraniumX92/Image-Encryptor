from datetime import datetime
import random
import math
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

def str_replace(st:str,index:int,char:str) -> str:
    """
    Takes a string and replaces the character present at index with given char
    and returns the modified string.

    :param st: str : string to be modified
    :param index: int: index at which replacement is to be done
    :param char: str : a character which should be replaced
    :return: str : modified string
    """
    lstr = list(st)
    lstr[index] = char
    return "".join(lstr)

def randint(a,b) -> int:
    return random.randint(a,b)

def random_KeyGen(keylen:int) -> list[int]:
    return random.sample(range(255),keylen)

def dump_json(object, filename):
    with open(filename, "w") as dump:
        json.dump(object, dump, indent=4)

def load_json(filename):
    with open(filename, "r") as load:
        return json.load(load)

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
        k = [ord(x) for x in strval]
    return k

def get_compact_key(strval:str) -> str:
    """
    takes a string, converts it into a list of ints using get_key(),
    then converts this list into string with no spaces and removes the square brackets and returns it

    :param strval:
    :return: str
    """
    return str(get_key(strval)).replace(" ","")

def to_even(n):
    """
    Takes an int n, if n is odd integer then converts n to an even number and returns n, else returns n as it is.

    :param n: int
    :return: int : closest even number to n in range(0,255)
    """
    if n%2==0:
        return n
    else:
        return n-1

def to_odd(n):
    """
    Takes an int n, if n is even integer then converts n to an odd number and returns n. else returns n as it is.

    :param n: int
    :return: int : closest odd number to n in range(0,255)
    """
    if n%2!=0:
        return n
    else:
        return n+1

def circular_increment(value:int,limit:int):
    """
    Does a circular increment to the given number and returns the incremented number.
    :param value: int
    :param limit: int
    :return: int - circularly incremented value
    """
    value += 1
    if value>=limit:
        value = 0
    return value

def split_and_flip(array:list,level:int=2):
    """
    divides the list into 2 halves and flips each half, joins the flipped halves and returns single list
    does the same thing with each half recursively for total of 3 times if the list contains even number of items, otherwise only 1 time.
    because array with odd number items cannot be split and obtained back in original form. where as arary with even number items
    can be split for total of 3 times recursively and also able to obtain original form of array.

    :param array: list
    :return: list - modified
    """
    if len(array)%2!=0:
        level = 0
    elif level>2:
        level = 2
  
    h1 = array[:len(array) // 2]
    h2 = array[len(array) // 2:]
    if level>0:
        h1 = split_and_flip(h1,level-1)
        h2 = split_and_flip(h2,level-1)
    return h1[::-1] + h2[::-1]

if __name__ == '__main__':
    arr = [x for x in range(40)]
    old = split_and_flip(arr,0)
    new = split_and_flip(arr)
    print(old)
    print(new)
    reset = split_and_flip(new)
    print(sorted(new) == reset)