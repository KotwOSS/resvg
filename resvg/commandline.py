# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import argparse, colors, logger, compiler, watcher, logging, components  # This import is not unused. It loads the builtin components
from settings import Settings


def silent_print_logo():
    """Print the logo if not in silent mode."""

    if not Settings.silent:
        print_logo()


def print_logo():
    """Print the logo."""

    print(
        f"""{colors.orange}
░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█ 
░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄ 
░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
    {colors.reset}"""
    )
    print(f"ReSVG version {colors.blue}{Settings.version}{colors.reset}")
    print("\n")
    print(
        f"Written by {colors.blue}{', '.join(Settings.authors)}{colors.reset} licensed under {colors.blue}{Settings.license}{colors.reset}."
    )
    print("")
    print(
        f"{colors.red}(c){colors.reset} Copyright {Settings.year} {colors.blue}{', '.join(Settings.authors)}{colors.reset}"
    )
    print("\n")


class help_formatter(argparse.HelpFormatter):
    """Custom help formatter."""

    def format_help(self):
        print_logo()
        return super().format_help() + "\n"

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is not argparse.SUPPRESS:
            self.add_text(
                f"{colors.blue}[USAGE]{colors.reset} {self._format_usage(usage, actions, groups, '')}"
            )


def parse():
    """Parse the commandline arguments."""

    parser = argparse.ArgumentParser(
        description="Process ReSVG files.", formatter_class=help_formatter
    )

    args = {
        "input;i": ["the input file", str],
        "output;o": ["the output file", str],
        "compile;c": ["compile a file", "store_true"],
        "watch;w": ["watch a file and compile on change", str],
        "version;v": ["show the version", "store_true"],
        "silent;s": ["run in silent mode", "store_true"],
        "pretty;p": ["pretty print the svg", "store_true"],
        "only-errors;e": ["only print errors and fatals", "store_true"],
        "log": ["specify a log file", str],
        "level": ["specify a log level", int, 20],
        "ext": ["specify the extensions which will be watched", str, "rsvg"],
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

    Settings.input = args.input
    Settings.output = args.output
    Settings.trust_exp = args.trust_exp or args.trust
    Settings.trust_stmt = args.trust_stmt or args.trust
    Settings.pretty = args.pretty
    Settings.ext = args.ext.split(",")
    Settings.comments = args.pretty or args.comments
    Settings.hide_logo = args.silent or args.only_errors or args.hide_logo
    Settings.level = logging.ERROR if args.only_errors else args.level
    Settings.log = args.log
    Settings.silent = args.silent
    Settings.compile = args.compile
    Settings.watch = args.watch

    logger.setup_logger(Settings.level, stdout=not Settings.silent, file=Settings.log)

    if Settings.compile:
        silent_print_logo()
        compiler.compile()
    elif Settings.watch:
        silent_print_logo()
        watcher.watch()
    else:
        parser.print_help()