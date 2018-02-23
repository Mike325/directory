#!/usr/bin/env python3

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

quiet = False
debug_mode = False
logger = False


def status(message):
    """Print status message

    :message: TODO
    :returns: TODO

    """
    global quiet
    with open("messages.log", "a") as messages:
        if quiet is False:
            print("[*]  {0}".format(message))
        if logger:
            try:
                messages.write("[*]  {0}\n".format(message))
            except IOError as e:
                error("We couldn't write the logger, check your SO permissions")


def verbose(message):
    """TODO: Docstring for verbose.

    :message: TODO
    :returns: TODO

    """
    global debug_mode
    global quiet
    if debug_mode is True:
        with open("messages.log", "a") as messages:
            if quiet is False:
                print("[$]  ---- Debug: {0}".format(message))
            if logger:
                try:
                    messages.write("[$]  ---- Debug: {0}\n".format(message))
                except Exception as e:
                    error("We couldn't write the logger, check your SO permissions")


def warning(message):
    """TODO: Docstring for status_message.

    :message: TODO
    :returns: TODO

    """
    global quiet
    with open("messages.log", "a") as messages:
        if quiet is False:
            print("[!]  ---- Warning: {0}".format(message))
        if logger:
            try:
                messages.write("[!]  ---- Warning: {0}\n".format(message))
            except Exception as e:
                error("We couldn't write the logger, check your SO permissions")


def error(message):
    """TODO: Docstring for status_message.

    :message: TODO
    :returns: TODO

    """
    global quiet
    with open("messages.log", "a") as messages:
        if quiet is False:
            print("[X]  ---- Error: {0}".format(message))
        if logger:
            try:
                messages.write("[X]  ---- Error: {0}".format(message))
            except Exception as e:
                error("We couldn't write the logger, check your SO permissions")


if __name__ == "__main__":
    raise Exception("This script is intended to be used as a module")
else:
    # We clean the logger
    with open("messages.log", "w") as messages:
        try:
            messages.write("")
        except Exception as e:
            error("We couldn't write the logger, check your SO permissions")
