import random
import string


def generate_random_string(length=10, mode="lettersdigits"):
    if mode == "letters":
        string_pool = string.ascii_letters
    elif mode == 'upperletters':
        string_pool = string.ascii_uppercase
    elif mode == 'lowerletters':
        string_pool = string.ascii_lowercase
    elif mode == "digits":
        string_pool = string.digits
    elif mode == "lettersdigits":
        string_pool = string.ascii_letters + string.digits
    else:
        raise ValueError("No mode has been detected")
    return [random.choice(string_pool) for _ in range(length)]


def is_number(num):
    try:
        int(num)
        return True
    except ValueError as e:
        return False
