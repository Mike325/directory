#!/usr/bin/env python

import argparse
from logger.messages import status
from logger.messages import error
from logger.messages import verbose
from logger import messages

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
                        metavar='TSIZE',
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


if __name__ == "__main__":
    main()
else:
    raise Exception("Main file is just an executable, not a module")
