#!/usr/bin/env python

import json
from os import path
from time import time
from logger.messages import verbose
from logger.messages import error
from btree.btree import BTree

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

# Global because we don't want to recalculate it every time
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
    # without accessing the global value
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
    hashvalue = sum(ord(x) for x in encode)
    verbose("Hash: {0}".format(hashvalue))
    verbose("Hashing time: {0}".format(end - start))
    return hashvalue % 4


def hashAscii(string, tsize=4):
    start = time()
    if type(string) != str:
        raise Exception(
            "Only strings are allow to be used in this hash function")
    end = time()
    hashvalue = sum(ord(x) for x in string)
    verbose("Hash: {0}".format(hashvalue))
    verbose("Hashing time: {0}".format(end - start))
    return hashvalue % tsize


class HashDataBase(object):
    """  Simple data base with N number of register, each one with its own tree"""

    class Register(object):
        """docstring for Register"""

        def __init__(self,
                     name,
                     last_name,
                     address,
                     cellphone,
                     email,
                     social_network):
            self.name = name
            self.last_name = last_name
            self.address = address
            self.cellphone = cellphone
            self.email = email
            self.social_network = social_network

    def __init__(self, size=4, json_db=None, hashfunction=None):
        super(HashDataBase, self).__init__()
        self.size = size
        self.container = []
        self.collisions = []

        for item in range(0, size):
            # self.container.append(BTree())
            self.container.append({})
            self.collisions.append(0)

        self.hashfunction = hashBase64 if hashfunction is None else hashfunction

        if json_db is not None and path.isfile(json_db):
            with open(json_db, "r") as database:
                data = json.load(database)
                for register, value in data.items():
                    self.insert(data[register])
        elif json_db is not None and not path.isfile(json_db):
            error("{0} must be a valid json file to load the registers")

    def _select_search_type(self):
        """TODO: Docstring for _select_search_type.
        :returns: TODO

        """
        selection = ""
        types = ["Name", "Last name", "Cellphone"]
        while selection != "1" and selection != "2" and selection != "3":
            selection = input("""Please select an option:
                            1) {0}
                            2) {1}
                            3) {2}""".format(types[0], types[1], types[2]))

        search_element = input("Enter the {0}: ".format(types[int(selection)]))

        return (search_element, selection)

    def insert(self, register=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO

        """
        if register is None:
            name = input("Enter name: ")
            last_name = input("Enter last name: ")
            address = input("Enter address: ")
            cellphone = input("Enter cellphone: ")
            email = input("Enter email address: ")
            social_network = input("Enter social network: ")
            register = self.Register(name,
                                     last_name,
                                     address,
                                     cellphone,
                                     email,
                                     social_network)
        rc = False
        start = time()

        if self.search(register=register) is not None:
            hashvalue = self.hashfunction(name)

            isEmpty = False
            # if self.container[hashvalue].empty():
            if len(self.container[hashvalue]) == 0:
                isEmpty = True
            # if not isEmpty and self.container[hashvalue].insert(register):
            self.container[hashvalue][parameter] = register
            if not isEmpty:
                self.collisions[hashvalue] += 1

            verbose("Collisions in container {0}: {1}".format(hashvalue, self.collisions[hashvalue]))
            rc = True
        else:
            error("Name must be unic {0} already exists".format(name))

        end = time()
        verbose("Insertion time {0}".format(end - start))

        return rc

    def update(self, register=None, name=None, last_name=None, cellphone=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO

        """
        selected_type = -1
        if register is None and name is None and last_name is None and cellphone is None:
            parameter, selected_type = self._select_search_type()
        elif register is not None:
            parameter = register.name
            selected_type = 0
        elif name is not None:
            parameter = name
            selected_type = 0
        elif last_name is not None:
            parameter = last_name
            selected_type = 1
        elif cellphone is not None:
            parameter = cellphone
            selected_type = 2

        rc = False
        start = time()

        hashvalue = self.hashfunction(parameter, selected_type)
        # register = self.container[hashvalue].search(parameter, selected_type)
        if parameter in self.container[hashvalue]:
            pass
        else:
            # if register is None:
            error("{0} doesn't exists".format(parameter, selected_type))
        # else:
        #     pass

        end = time()
        verbose("Update time {0}".format(end - start))

        return rc

    def delete(self, register=None, name=None, last_name=None, cellphone=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO

        """
        selected_type = -1
        if register is None and name is None and last_name is None and cellphone is None:
            parameter, selected_type = self._select_search_type()
        elif register is not None:
            parameter = register.name
            selected_type = 0
        elif name is not None:
            parameter = name
            selected_type = 0
        elif last_name is not None:
            parameter = last_name
            selected_type = 1
        elif cellphone is not None:
            parameter = cellphone
            selected_type = 2

        rc = False
        start = time()

        hashvalue = self.hashfunction(parameter, selected_type)
        if parameter is self.container[hashvalue]:
            self.container[hashvalue].pop(parameter, None)
            if self.collisions[hashvalue] > 0:
                self.collisions[hashvalue] -= 1
            verbose("Collisions in container {0}: {1}".format(hashvalue, self.collisions[hashvalue]))
        else:
            error("{0} could not be deleted".format(parameter, selected_type))

        # rc = self.container[hashvalue].delete(parameter, selected_type)
        # if rc is None:
        #     error("{0} could not be deleted".format(parameter, selected_type))
        # else:
        #     if self.collisions[hashvalue] > 0:
        #         self.collisions[hashvalue] -= 1
        #     verbose("Collisions in container {0}: {1}".format(hashvalue, self.collisions[hashvalue]))

        end = time()
        verbose("Deletion time {0}".format(end - start))

        return rc

    def search(self, register=None, name=None, last_name=None, cellphone=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO
        """
        selected_type = -1
        if register is None and name is None and last_name is None and cellphone is None:
            parameter, selected_type = self._select_search_type()
        elif register is not None:
            parameter = register.name
            selected_type = 0
        elif name is not None:
            parameter = name
            selected_type = 0
        elif last_name is not None:
            parameter = last_name
            selected_type = 1
        elif cellphone is not None:
            parameter = cellphone
            selected_type = 2

        start = time()

        hashvalue = self.hashfunction(parameter, selected_type)

        register = None
        if parameter in self.container[hashvalue]:
            register = self.container[hashvalue][parameter]

        # register = self.container[hashvalue].search(parameter, selected_type)
        # if register is not None:
        #     return register
        # error("{0} doesn't exists".format(parameter, selected_type))

        end = time()
        verbose("Search time {0}".format(end - start))

        return register

    def dump(self):
        """TODO: Docstring for insert.

        :returns: TODO

        """
        raise Exception("Not implemented")
        # with open("hash_dump.json", "r") as db:
        #     for item in self.container:
        #         pass


if __name__ == "__main__":
    raise Exception("This is a handle, not a standalone script")
else:
    # We want to calculate this from the start
    base64Values()
