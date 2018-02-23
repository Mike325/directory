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


class Person(object):
    """Main class from the directory"""

    VALID_FIELD = ["name", "lastname", "number", "address", "mail", "social"]

    def __init__(self, person=None):
        super(Person, self).__init__()
        if type(person) is Person:
            self.data["name"] = person["name"]
            self.data["lastname"] = person["lastname"]
            self.data["number"] = person["number"]
            self.data["address"] = person["address"]
            self.data["mail"] = person["mail"]
            self.data["social"] = person["social"]
        else:
            self.data["name"] = ""
            self.data["lastname"] = ""
            self.data["number"] = 0
            self.data["address"] = ""
            self.data["mail"] = ""
            self.data["social"] = ""

    def update(self, field, value):
        """TODO: Docstring for update.

        :field: TODO
        :value: TODO
        :returns: TODO

        """
        success = False

        if field in self.VALID_FIELD:
            self.data[field] = value
            success = True

        return success

    def __str__(self):
        """String representation of a person
        :returns: TODO

        """
        pass


if __name__ == "__main__":
    raise Exception("This is a module not a main executable")
