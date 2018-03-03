#!/usr/bin/env python

from time import time
from logger.messages import debug

__header__ = """
                              -`
              ...            .o+`
           .+++s+   .h`.    `ooo/
          `+++%++  .h+++   `+oooo:
          +++o+++ .hhs++. `+oooooo:
          +s%%so%.hohhoo'  'oooooo+:
          `+ooohs+h+sh++`/:  ++oooo+:
           hh+o+hoso+h+`/++++.+++++++:
            `+h+++h.+ `/++++++++++++++:
                     `/+++ooooooooooooo/`
                    ./ooosssso++osssssso+`
                   .oossssso-````/osssss::`
                  -osssssso.      :ssss``to.
                 :osssssss/  Mike  osssl   +
                /ossssssss/   8a   +sssslb
              `/ossssso+/:-        -:/+ossss'.-
             `+sso+:-`                 `.-/+oso:
            `++:.                           `-/+/
            .`                                 `/
"""

# Global because we don't want to recaulculate thi every time
__values = []


def base64Values():
    """TODO: Docstring for base64Values.
    :returns: TODO

    """
    global __values
    __values = []

    # A - Z
    for item in range(65, 91):
        __values.append(chr(item))

    # a - z
    for item in range(97, 123):
        __values.append(chr(item))

    # 0 - 9
    for item in range(0, 10):
        __values.append("{0}".format(item))

    __values.append("+")
    __values.append("/")

    # This array is global but we allow other libs to get base 64 elements
    # witout accesing the global value
    return __values


def hashBase64(string, tsize=4):
    """Create a hash of a given string

    :string: TODO
    :returns: TODO

    """
    global __values

    if len(__values) == 0:
        base64Values()

    start = time()

    bstring = ""

    for i in str(string):
        bits = bin(ord(i))[2:]
        bsize = len(bits)
        if bsize < 8:
            bits = "0" * (8 - bsize) + bits
        bstring = bstring + bits

    encode = ""
    while len(bstring) > 0:
        encode += __values[int(bstring[0:6], 2)]
        bstring = bstring[6:]

    end = time()
    debug("Hashing time: {0}".format(end - start))
    return sum(ord(x) for x in encode) % 4


def hashAscii(string, tsize=4):
    start = time()
    if type(string) != str:
        raise Exception(
            "Only strings are allow to be used in this hash function")
    end = time()
    debug("Hashing time: {0}".format(end - start))
    return sum(ord(x) for x in string) % tsize


if __name__ == "__main__":
    raise Exception("This is a handle, not a standalone script")
else:
    # We want to calculate this from the start
    base64Values()
