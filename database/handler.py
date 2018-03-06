#!/usr/bin/env python3

import json
from os import path
from time import time
from logger.messages import verbose
from logger.messages import error
from logger.messages import status
# from btree.btree import BTree

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

    hashvalue = sum(ord(x) for x in encode)
    end = time()
    verbose("Hash: {0}".format(hashvalue))
    verbose("Hashing time: {0}".format(end - start))
    return hashvalue % 4


def hashAscii(string, tsize=4):
    start = time()
    if type(string) != str:
        raise Exception(
            "Only strings are allow to be used in this hash function")
    hashvalue = sum(ord(x) for x in string)
    end = time()
    verbose("Hash: {0}".format(hashvalue))
    verbose("Hashing time: {0}".format(end - start))
    return hashvalue % tsize


class HashDataBase(object):
    """  Simple data base with N number of register, each one with its own tree"""

    class Register(object):
        """docstring for Register"""

        def __init__(self, name, last_name, address, cellphone, email,
                     social_network):
            self.name = name
            self.last_name = last_name
            self.address = address
            self.cellphone = cellphone
            self.email = email
            self.social_network = social_network

        def __str__(self):
            """String representation of the register
            :returns: TODO

            """
            return "\nName: {0} {1}\nAddress: {2}\nCellphone: {3}\nEmail: {4}\nSocial: {5}".format(
                self.name, self.last_name, self.address, self.cellphone,
                self.email, self.social_network)

        def __nq__(self, register):
            return (self.name.lower() != register.name.lower())

        def __eq__(self, register):
            return (self.name.lower() == register.name.lower())

        def __le__(self, register):
            return (self.name.lower() <= register.name.lower())

        def __lt__(self, register):
            return (self.name.lower() < register.name.lower())

        def __ge__(self, register):
            return (self.name.lower() >= register.name.lower())

        def __gt__(self, register):
            return (self.name.lower() > register.name.lower())

        def __len__(self):
            return 0

    def __init__(self, size=4, json_db=None, hashfunction=None):
        super(HashDataBase, self).__init__()
        self.size = size
        self.container = []
        self.collisions = []
        self.numbers = {}
        self.last_names = {}

        for item in range(0, size):
            # self.container.append(BTree())
            self.container.append({})
            self.collisions.append(0)

        self.hashfunction = hashBase64 if hashfunction is None else hashfunction

        if json_db is not None and path.isfile(json_db):
            with open(json_db, "r") as database:
                data = json.load(database)
                for rid, register in data.items():
                    verbose("Register: {0}".format(register))
                    element = self.Register(
                        name=register["name"],
                        last_name=register["last_name"],
                        address=register["address"],
                        cellphone=register["cellphone"],
                        email=register["email"],
                        social_network=register["social_network"])
                    self.insert(register=element)
        elif json_db is not None and not path.isfile(json_db):
            error("{0} must be a valid json file to load the registers")

    def insert(self, register=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO

        """
        if register is None:
            valid = False
            while not valid:
                name = input("Enter name: ")
                last_name = input("Enter last name: ")
                address = input("Enter address: ")
                cellphone = input("Enter cellphone: ")
                if cellphone in self.numbers:
                    error("This cellphone is already in use")
                    continue
                valid = True
                email = input("Enter email address: ")
                social_network = input("Enter social network: ")
            register = self.Register(name, last_name, address, cellphone,
                                     email, social_network)
        rc = False
        start = time()

        hashvalue = self.hashfunction(register.name)

        isEmpty = False

        # TODO: This must be changed for the tree
        if len(self.container[hashvalue]) == 0:
            isEmpty = True

        # TODO: This must be changed for the tree
        self.container[hashvalue][register.name] = register

        self.numbers[register.cellphone] = hashvalue
        if register.last_name not in self.last_names:
            self.last_names[register.last_name] = [hashvalue]
        else:
            self.last_names[register.last_name].append(hashvalue)

        if not isEmpty:
            self.collisions[hashvalue] += 1

        verbose("Collisions in container {0}: {1}".format(
            hashvalue, self.collisions[hashvalue]))

        rc = True
        status("Register inserted")

        end = time()
        verbose("Insertion time {0}".format(end - start))

        return rc

    def _update_field(self, register):
        """Update a specific field of the register

        :register: TODO
        :returns: TODO

        """
        status("Please select the field you want to update")
        valid = False
        while not valid:
            answer = input("""Please select a valid option:
                    1) Last name
                    2) Address
                    3) Cellphone
                    4) Email
                    5) Social Network
                    6) All
                    : """)
            try:
                value = int(answer)
                if value < 1 or value > 6:
                    error("Not a valid option {0}".format(value))
                    continue
                if value == 6:
                    register.last_name = input("Enter last name: ")
                    register.address = input("Enter address: ")
                    register.cellphone = input("Enter cellphone: ")
                    register.email = input("Enter email address: ")
                    register.social_network = input("Enter social network: ")
                else:
                    if value == 1:
                        register.last_name = input("enter last name: ")
                    elif value == 2:
                        register.address = input("Enter address: ")
                    elif value == 3:
                        register.cellphone = input("Enter cellphone: ")
                    elif value == 4:
                        register.email = input("Enter email address: ")
                    elif value == 5:
                        register.social_network = input(
                            "Enter social network: ")

                valid = True

            except Exception:
                error("Please select a valid option from the menu from 1 to 6")

        return register

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
                            3) {2}
                            : """.format(types[0], types[1], types[2]))
        if selection != "1" and selection != "2" and selection != "3":
            error("Please select a valid option {0}".format(selection))

        search_element = input("Enter the {0}: ".format(types[int(selection) - 1]))

        return (search_element, int(selection) - 1)

    def search(self, register=None, name=None, last_name=None, cellphone=None):
        """TODO: Docstring for insert.

        :register: TODO
        :returns: TODO
        """
        selected_type = -1
        if register is None and name is None and last_name is None and cellphone is None:
            parameter, selected_type = self._select_search_type()
        elif register is not None and type(register) is self.Register:
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
        else:
            # We fall here if register is not None and is not a Register type
            raise Exception("Unknown type {0}".format(repr(register)))

        start = time()

        register = None

        verbose("Searching for: {0}".format(parameter))
        if selected_type == 0:
            hashvalue = self.hashfunction(parameter)

            # TODO: This must be changed for the tree
            verbose("Name {0}".format(parameter))
            if parameter in self.container[hashvalue]:
                register = self.container[hashvalue][parameter]
            else:
                error("The register {0} doesn't exists".format(parameter))
        elif selected_type == 1:
            if parameter in self.last_names:
                verbose("Last name {0}".format(parameter))
                containers = self.last_names[parameter]
                verbose("List of containers {0}".format(containers))
                # Since last names are not unic, the dictionary has a list with all the containers with the last name
                register = []
                for container in containers:
                    # TODO: This must be changed for the tree
                    for key, value in self.container[container].items():
                        if value.last_name == parameter:
                            register.append(
                                self.container[container][parameter])

                # status("Please select a register")
            else:
                error("The register {0} doesn't exists".format(parameter))
        elif selected_type == 2:
            if parameter in self.numbers:
                verbose("Number to find {0}".format(parameter))
                # TODO: This must be changed for the tree
                container = self.numbers[parameter]
                for key, value in self.container[container].items():
                    if value.cellphone == parameter:
                        register = self.container[container][parameter]
                        break
            else:
                error("The register {0} doesn't exists".format(parameter))
        else:
            raise Exception("Not a valid option {0}".format(selected_type))

        # register = self.container[hashvalue].search(parameter, selected_type)
        # if register is not None:
        #     return register
        # error("{0} doesn't exists".format(parameter, selected_type))

        end = time()
        verbose("Search time {0}".format(end - start))

        return register

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
            register = self.container[hashvalue][parameter]
            register = self._update_field(register)
            self.container[hashvalue][parameter] = register
            status("Register updated")
        else:
            # if register is None:
            error("{0} doesn't exists".format(parameter, selected_type))
        # else:
        #     pass

        end = time()
        verbose("Update time {0}".format(end - start))

        return rc

    def _delete_register(self, register, hashvalue):
        """TODO: Docstring for _delete_register.

        :register: TODO
        :returns: TODO

        """
        # TODO: This must be changed for the tree
        self.container[hashvalue].pop(register.name, None)
        if self.collisions[hashvalue] > 0:
            self.collisions[hashvalue] -= 1

        self.numbers.pop(register.cellphone, None)
        for container in self.last_names[register.last_name]:
            if container == hashvalue:
                self.last_names[register.last_name].remove(hashvalue)
                break

        verbose("Collisions in container {0}: {1}".format(
            hashvalue, self.collisions[hashvalue]))
        status("Register deleted: {0}".format(register))

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

        if selected_type == 0:
            register = self.search(name=parameter)
        elif selected_type == 1:
            register = self.search(last_name=parameter)
        elif selected_type == 2:
            register = self.search(cellphone=parameter)

        if register is not None:
            # Register is not None so if its len is 0 then is just one register
            hashvalue = self.hashfunction(register.name)
            if len(register) == 0:
                self._delete_register(register, hashvalue)
            else:
                for item in register:
                    self._delete_register(item, hashvalue)
        else:
            error("{0} could not be deleted".format(parameter))

        end = time()
        verbose("Deletion time {0}".format(end - start))

        return rc

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
