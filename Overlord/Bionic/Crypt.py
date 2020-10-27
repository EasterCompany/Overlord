from time import time
from random import randint
from hashlib import sha256


def spice(meat):
    meat = str(meat) + str(time())
    i,j,k = str(
        randint(0, 999999)
    ), str(
        randint(0, 999999)
    ), str(
        randint(0, 999999)
    )
    ji = int(
        len(meat)/2
    )
    return sha256(
        str(
            i + meat[0:ji] + j + meat[ji+1:-1] + k
        ).encode()
    ).hexdigest()

