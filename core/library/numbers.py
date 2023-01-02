# Overlord Numbers Library
# Contains various math, crypto & number to string manipulation handy-dandies.

def zero_prefixed_integer(integer, length=2):
    """
    Converts an integer to a string which is prefixed with zeroes (ie; 1 -> 01)

    :param integer int: input number to be converted
    :param length int: length of string to be returned
    :return str: returns a string prefixed with zeroes
    """
    string = str(integer)
    while len(string) < length:
        string = '0' + string
    return string
