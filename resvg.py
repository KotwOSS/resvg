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
def compile(src, dest):
    start = time()

    doc = minidom.parse(src)

    root = doc.documentElement

    transformer = NodeTransform(root)
    transformer.transform()

    pretty_xml = doc.documentElement.toprettyxml(
        newl=Settings.newl, indent=Settings.indent
    )
    if Settings.newl != "":
        pretty_xml = os.linesep.join(
            [s for s in pretty_xml.split(Settings.newl) if s.strip()]
        )
    dest.write(pretty_xml)

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


def unescape_string(string):
    return string.encode("latin-1", "backslashreplace").decode("unicode-escape")


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Process ReSVG files.", formatter_class=help_formatter
    )

    args = {
        "input;i": ["the input file", str],
        "output;o": ["the output file", str],
        "compile;c": ["compile a file", "store_true"],
        "version;v": ["show the version", "store_true"],
        "silent;s": ["run in silent mode", "store_true"],
        "pretty;p": ["pretty print the svg", "store_true"],
        "only-errors;e": ["only print errors and fatals", "store_true"],
        "log": ["specify a log file", str],
        "level": ["specify a log level", int, 0],
        "indent": ["specify the indentation", int],
        "newl": ["specify the newline character", str],
        "trust-exp": ["enable trust for expressions", "store_true"],
        "trust-stmt": ["enable trust for statements", "store_true"],
        "trust": ["enable trust for statements and expressions", "store_true"],
        "hide-logo": ["hide logo", "store_true"],
        "comments": ["keep the comments from the ReSVG file", "store_true"],
    }

    for arg, info in args.items():
        parts = arg.split(";")
        kwargs = {
            "help": info[0],
        }
        kwargs["action" if isinstance(info[1], str) else "type"] = info[1]
        kwargs["default"] = info[2] if len(info) > 2 else None
        kwargs["dest"] = parts[0].replace("-", "_")
        if len(parts) == 2:
            parser.add_argument(f"-{parts[1]}", f"--{parts[0]}", **kwargs)
        else:
            parser.add_argument(f"--{parts[0]}", **kwargs)

    args = parser.parse_args()

    loglevel = Logger.ERROR if args.only_errors else args.level

    std_logger = None
    if not args.silent:
        std_logger = PrettyLogger(loglevel, sys.stdout, False)

    file_logger = None
    if args.log:
        file_logger = SimpleLogger(loglevel, open(args.log, "a"), args.silent)

    Logger.logger = CombinedLogger([file_logger, std_logger])

    Settings.trust_exp = args.trust_exp or args.trust
    Settings.trust_stmt = args.trust_stmt or args.trust
    Settings.pretty = args.pretty
    Settings.newl = (
        "\n"
        if args.pretty and args.newl == None
        else unescape_string(args.newl)
        if args.newl
        else ""
    )
    Settings.indent = " " * (
        4 if args.pretty and args.indent == None else args.indent if args.indent else 0
    )
    Settings.comments = args.pretty or args.comments
    Settings.hide_logo = args.silent or args.only_errors or args.hide_logo

    if args.version:
        cmd_version()
        sys.exit(0)

    if args.compile:
        if not Settings.hide_logo:
            print_logo()

        input_file = args.input
        output_file = args.output

        output_stream = open(output_file, "w") if output_file else sys.stdout

        Logger.logger.info(
            f"Compiling §o'{input_file}'§R to §o'{output_file if output_file else 'stdout'}'§R"
        )

        took = compile(input_file, output_stream)

        if not output_file:
            print()

        Logger.logger.info(f"Compilation took §o{round(took * 1000)} ms.§R")

        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
