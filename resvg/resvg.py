#! /usr/bin/python3

# ░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█
# ░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄
# ░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
#
# ReSVG is a advanced SVG compiler which includes many features.
#
# It is licensed under the MIT license.
#
# (c) Copyright 2022 KotwOSS
#
# https://github.com/KotwOSS/ReSVG

import os, sys, colors

# The required modules
required_modules = ["lxml", "watchdog", "argparse", "numpy", "more_itertools"]

for required in required_modules:
    try:
        __import__(required)
    except ImportError as e:
        print(
            f"{colors.red}ERROR{colors.reset} missing required module {required}: {e}"
        )
        print(
            f"{colors.yellow}WARNING{colors.reset} do you want to install the requirements from {os.getcwd()}/../requirements.txt?"
        )

        choice = input("[Y/n] ")

        if choice.lower() == "y":
            os.system(f"python3 -m pip install -r {os.getcwd()}/../requirements.txt")
        else:
            print(
                f"{colors.blue}INFO{colors.reset} please install the requirements manually."
            )
            sys.exit(1)


# Parse the commandline arguments
import commandline

commandline.parse()
