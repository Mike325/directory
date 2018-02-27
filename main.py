#!/usr/bin/env python
# coding:utf-8

import argparse
from logger.messages import status
from logger import messages
from database.data import MAIN_MENU
from database.data import elements
from database.data import translits
from cli.functions import get_next_id
from cli.functions import print_to_console
# from database.data import spaces
# from cli.functions import get_spaces
# from logger.messages import error
# from logger.messages import verbose

__header__ = """
                              -`
              ...            .o+`
           .+++s+   .h`.    `ooo/
          `+++%++  .h+++   `+oooo:
          +++o+++ .hhs++. `+oooooo:
          +s%%so%.hohhoo"  "oooooo+:
          `+ooohs+h+sh++`/:  ++oooo+:
           hh+o+hoso+h+`/++++.+++++++:
            `+h+++h.+ `/++++++++++++++:
                     `/+++ooooooooooooo/`
                    ./ooosssso++osssssso+`
                   .oossssso-````/osssss::`
                  -osssssso.      :ssss``to.
                 :osssssss/  Mike  osssl   +
                /ossssssss/   8a   +sssslb
              `/ossssso+/:-        -:/+ossss".-
             `+sso+:-`                 `.-/+oso:
            `++:.                           `-/+/
            .`                                 `/
"""

__version__ = "0.1.0"


def __parse_arguments():
    """ Function to parse CLI args
    :returns: object with the CLI arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--tree_size",
                        help="The T size of the tree",
                        required=False,
                        default=2,
                        metavar="TSIZE",
                        dest="tsize",
                        type=int)
    parser.add_argument("-v",
                        "--verbose",
                        help="Enable debug messages",
                        required=False,
                        dest="verbose",
                        action="store_true")
    parser.add_argument("-l",
                        "--logger",
                        help="Enable logger",
                        required=False,
                        dest="logger",
                        action="store_true")
    parser.add_argument("-q",
                        "--quiet",
                        help="Silence all stout output",
                        required=False,
                        dest="quiet",
                        action="store_true")
    parser.add_argument("--version",
                        help="Shows the version",
                        required=False,
                        dest="version",
                        action="store_true")

    cli_args = parser.parse_args()

    return cli_args


# ==================== CREATE ====================
def create_record():
    name = raw_input("Enter name: ")
    last_name = raw_input("Enter last name: ")
    address = raw_input("Enter address: ")
    cellphone = raw_input("Enter cellphone: ")
    email = raw_input("Enter email address: ")
    social_network = raw_input("Enter social network: ")
    for record in elements:
        if set([name, last_name, address, cellphone, email, social_network]).issubset(record.values()):
            print("Record: {name} {last_name} {cellphone} is already in the database")
            return
    if name and last_name and cellphone:
        elements.append({"id": get_next_id(),
                         "name": name,
                         "last_name": last_name,
                         "address": address,
                         "cellphone": cellphone,
                         "email": email,
                         "social_network": social_network})
        print("User added successfully")
    else:
        print("You have added empty values")


# ==================== UPDATE ====================
def update_record():
    if elements:
        print_to_console()
        record_id = raw_input("Input the user key: ")
        for record in elements:
            if record["id"] == record_id:
                for key, value in record.items():
                    if key == "id":
                        continue
                    new_record = raw_input("Actual Value -> {current_name}: {current_record}, Enter new value or leave it empty: ".format(current_name=translits.get(key), current_record=value))
                    if new_record:
                        record[key] = new_record
                        print("User updated successfully")
                break
        else:
            print("User not found")
    else:
        print("No elements to show")


# ==================== DELETE ====================
def delete_record():
    if elements:
        print_to_console()
        record_id = raw_input("Enter user ID: ")
        for record in elements:
            if record["id"] == record_id:
                elements.remove(record)
                print("User deleted successfully")
                break
        else:
            print("User not found")
    else:
        print("No elements to show")


def main():
    """Main CLI function
    :returns: TODO

    """
    global debug_mode
    global start_time

    cli_args = __parse_arguments()

    if cli_args.version:
        status("Current version {0}".format(__version__))
        return 0

    messages.debug_mode = cli_args.verbose
    messages.quiet = cli_args.quiet
    messages.logger = cli_args.logger

    action = ""

    # While True is always a bad idea
    while action.upper() != "E":
        action = raw_input(MAIN_MENU)
        if action == "1":
            create_record()
        elif action == "2":
            print_to_console()
        elif action == "3":
            update_record()
        elif action == "4":
            delete_record()
        elif action.upper() != "E":
            print("Sin acción en {action}".format(action=action))


if __name__ == "__main__":
    main()
else:
    raise Exception("Main file is just an executable, not a module")
