#!/usr/bin/env python3
# coding:utf-8

import argparse
# from time import time
from logger.messages import status
from logger.messages import error
from logger.messages import verbose
from logger import messages
from database.data import MAIN_MENU
# from database.data import elements
# from database.data import translits
from database.handler import HashDataBase
from database.handler import hashAscii
from database.handler import hashBase64
# from cli.functions import get_next_id
# from cli.functions import print_to_console
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

__version__ = "0.1.1"


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
                        help="Enable verbose messages",
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
    parser.add_argument("-s",
                        "--hash",
                        help="Shows the version",
                        required=False,
                        type=int,
                        dest="hash")
    parser.add_argument("-j",
                        "--json",
                        help="JSON file with thr initial registers",
                        required=False,
                        type=str,
                        dest="json")
    parser.add_argument("--version",
                        help="Shows the version",
                        required=False,
                        dest="version",
                        action="store_true")

    cli_args = parser.parse_args()

    return cli_args


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

    if cli_args.hash == 1:
        hashfunction = hashAscii
    else:
        hashfunction = hashBase64

    verbose("Hash function {0}".format(repr(hashfunction.__name__)))

    action = ""

    table = HashDataBase(hashfunction=hashfunction, json_db=cli_args.json)

    # While True is always a bad idea
    while action.upper() != "E":
        action = input(MAIN_MENU)
        if action == "1":
            table.insert()
        elif action == "2":
            result = table.search()
            if result is not None and len(result) == 0:
                status("Register: {0}".format(result))
            elif result is not None and len(result) > 0:
                for item in result:
                    status("Register: {0}".format(item))
            else:
                error("Element was not found")
        elif action == "3":
            table.update()
        elif action == "4":
            table.delete()
        elif action == "5":
            for item in table.container:
                for name, register in item.items():
                    status("Register: {0}".format(register))
        elif action.upper() != "E":
            status("Sin acción en {action}".format(action=action))


if __name__ == "__main__":
    main()
else:
    raise Exception("Main file is just an executable, not a module")
