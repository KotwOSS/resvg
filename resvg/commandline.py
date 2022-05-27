# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import argparse, colors, logger, compiler, watcher, logging, components, transformers, default_data
from settings import Settings

components.register()
transformers.register()
default_data.register()

def silent_print_logo():
    """Print the logo if not in silent mode."""

    if not Settings.hide_logo:
        print_logo()


def print_logo():
    """Print the logo."""

    print(
        colors.format(
            """§o
░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█ 
░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄ 
░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
    §R"""
        )
    )
    print(colors.format(f"ReSVG version §b{Settings.version}§R"))

    print("\n")
    print(
        colors.format(
            f"Written by §b{', '.join(Settings.authors)}§R \
licensed under §b{Settings.license}§R."
        )
    )
    print("")
    print(
        colors.format(
            f"§r(c)§R Copyright {Settings.year} \
§b{', '.join(Settings.authors)}§R"
        )
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
        "min-time": ["minimum time between compiles", float, 1.0],
        "version;v": ["show the version", "store_true"],
        "silent;s": ["run in silent mode", "store_true"],
        "pretty;p": ["pretty print the svg", "store_true"],
        "no-color": ["disable color", "store_true"],
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
    Settings.comments = args.comments
    Settings.hide_logo = args.silent or args.hide_logo
    Settings.level = logging.ERROR if args.silent else args.level
    Settings.log = args.log
    Settings.silent = args.silent
    Settings.compile = args.compile
    Settings.watch = args.watch
    Settings.min_time = args.min_time
    Settings.no_color = args.no_color

    logger.setup_logger()

    if Settings.compile:
        silent_print_logo()
        compiler.compile()
    elif Settings.watch:
        silent_print_logo()
        watcher.watch()
    else:
        parser.print_help()
