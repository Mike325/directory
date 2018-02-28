#!/usr/bin/env python

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


class HashTable(object):
    """Hash table to handle directory data"""

    def __init__(self, arg):
        super(HashTable, self).__init__()
        self.arg = arg

    def hashAscii(string):
        acomulator = 0
        for element in string:
            if type(element) == int:
                acomulator += chr(element)
            elif type(element) == str:
                acomulator += ord(element)
            else:
                print("Invalid Element")
        return acomulator % 4
      
if __name__ == "__main__":
        
    raise Exception("This is a handle, not a standalone script")
