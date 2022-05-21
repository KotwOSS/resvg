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


# Details
version = "0.0.0alpha1"
authors = ["KotwOSS"]
license = "MIT"
year = 2022

from util import *
from components import *


# Import the required modules
try:
    import sys, argparse
    from argparse import HelpFormatter
    from xml.dom import minidom
    from time import time
    from argparse import SUPPRESS
except ImportError as e:
    print(f"{red}ERROR{reset} missing required module: {e}")
    sys.exit(1)

# Compile a file
def compile(src, dest, pretty):
    start = time()

    doc = minidom.parse(src)

    root = doc.documentElement

    transformer = NodeTransform(root, pretty)
    transformer.transform()

    if pretty:
        pretty_xml = doc.documentElement.toprettyxml(indent="    ")
        pretty_xml = os.linesep.join([s for s in pretty_xml.splitlines() if s.strip()])
        dest.write(pretty_xml)
    else:
        doc.documentElement.writexml(dest)

    doc.unlink()

    return time() - start


# Print the logo
def print_logo():
    print(
        f"""{orange}
░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█ 
░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄ 
░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
    {reset}"""
    )
    print(f"ReSVG version {blue}{version}{reset}")
    print("\n")
    print(
        f"Written by {blue}{', '.join(authors)}{reset} licensed under {blue}{license}{reset}."
    )
    print("")
    print(f"{red}(c){reset} Copyright {year} {blue}{', '.join(authors)}{reset}")
    print("\n")


# Print the version
def cmd_version():
    print(version)


# Custom help formatter
class help_formatter(HelpFormatter):
    def format_help(self):
        print_logo()
        return super().format_help() + "\n"

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is not SUPPRESS:
            self.add_text(
                f"{blue}[USAGE]{reset} {self._format_usage(usage, actions, groups, '')}"
            )


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Process ReSVG files.", formatter_class=help_formatter
    )

    parser.add_argument("--log", dest="log", help="specify a log file", type=str)

    parser.add_argument(
        "--level", dest="level", help="specify a log level", type=int, default=0
    )

    parser.add_argument(
        "-s", "--silent", dest="silent", help="run in silent mode", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--pretty",
        dest="pretty",
        help="pretty print the svg",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--only-errors",
        dest="only_errors",
        help="Only display errors and fatals",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--compile",
        dest="compile",
        help="compile input file",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--version", dest="version", help="show the version", action="store_true"
    )

    parser.add_argument("-i", "--input", dest="input", help="the input file", type=str)
    parser.add_argument(
        "-o", "--output", dest="output", help="the output file", type=str
    )

    args = parser.parse_args()

    loglevel = Logger.ERROR if args.only_errors else args.level

    std_logger = None
    if not args.silent:
        std_logger = PrettyLogger(loglevel, sys.stdout, False)

    file_logger = None
    if args.log:
        file_logger = SimpleLogger(loglevel, open(args.log, "a"), args.silent)

    Logger.logger = CombinedLogger([file_logger, std_logger])

    if args.version:
        cmd_version()
        sys.exit(0)

    if args.compile:
        if not args.silent and not args.only_errors:
            print_logo()

        input_file = args.input
        output_file = args.output

        output_stream = open(output_file, "w") if output_file else sys.stdout

        Logger.logger.info(
            f"Compiling §o'{input_file}'§R to §o'{output_file if output_file else 'stdout'}'§R"
        )

        took = compile(input_file, output_stream, args.pretty)

        if not output_file:
            print()

        Logger.logger.info(f"Compilation took §o{round(took * 1000)} ms.§R")

        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
