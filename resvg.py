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
version = "0.0.0alpha2"
authors = ["KotwOSS"]
license = "MIT"
year = 2022

from .util import *
from .components import *

# Import the required modules
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import sys, argparse
    from argparse import HelpFormatter
    from xml.dom import minidom
    import time
    from argparse import SUPPRESS
except ImportError as e:
    print(f"{red}ERROR{reset} missing required module: {e}")
    sys.exit(1)

# Compile a file
def compile(src, dest):
    start = time.time()

    doc = minidom.parse(src)

    root = doc.documentElement

    transformer = NodeTransform(doc, root)
    transformer.transform()

    pretty_xml = root.toprettyxml(newl=Settings.newl, indent=Settings.indent)
    if Settings.newl != "":
        pretty_xml = os.linesep.join(
            [s for s in pretty_xml.split(Settings.newl) if s.strip()]
        )
    dest.write(pretty_xml)

    doc.unlink()

    return time.time() - start


# Compile command
def cmd_compile():
    try:
        output_stream = open(Settings.output, "w") if Settings.output else sys.stdout

        Logger.logger.info(
            f"Compiling §o'{Settings.input}'§R to §o'{Settings.output if Settings.input else 'stdout'}'§R"
        )

        took = compile(Settings.input, output_stream)

        if not Settings.output:
            print()

        Logger.logger.info(f"Compilation took §o{round(took * 1000)} ms§R.")
    except Exception as e:
        Logger.logger.exit_fatal(f"Error occured while compiling: {e}")


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


class WatchHandler(FileSystemEventHandler):
    compiling = False

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "modified":
            if (
                not WatchHandler.compiling
                and event.src_path.split(".").pop() in Settings.ext
            ):
                Logger.logger.warning("File updated! Recompiling...")
                WatchHandler.compiling = True
                cmd_compile()
                WatchHandler.compiling = False


# Main function
def main():
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
        "level": ["specify a log level", int, 0],
        "indent": ["specify the indentation", int],
        "newl": ["specify the newline character", str],
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

    loglevel = Logger.ERROR if args.only_errors else args.level

    std_logger = None
    if not args.silent:
        std_logger = PrettyLogger(loglevel, sys.stdout, False)

    file_logger = None
    if args.log:
        file_logger = SimpleLogger(loglevel, open(args.log, "a"), args.silent)

    Logger.logger = CombinedLogger([file_logger, std_logger])

    Settings.input = args.input
    Settings.output = args.output
    Settings.trust_exp = args.trust_exp or args.trust
    Settings.trust_stmt = args.trust_stmt or args.trust
    Settings.pretty = args.pretty
    Settings.ext = args.ext.split(",")
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

    if args.watch:
        Settings.fatal_exit = False

        if not Settings.hide_logo:
            print_logo()

        if (
            args.input
            and os.path.exists(args.input)
            and args.watch
            and os.path.exists(args.watch)
        ):
            observer = Observer()

            observer.schedule(WatchHandler(), args.watch, recursive=True)
            ext_str = "§g, §y'.".join(Settings.ext)
            Logger.logger.info(
                f"Watching §o'{args.watch}'§R for changes on §g[§y'.{ext_str}'§g]§R..."
            )

            cmd_compile()

            observer.start()

            try:
                while True:
                    time.sleep(5)
            except KeyboardInterrupt:
                observer.stop()
                Logger.logger.info("Observer stopped.")

            observer.join()
        else:
            if args.input:
                Logger.logger.exit_fatal("Input file not found.")
            else:
                Logger.logger.exit_fatal("No input file specified")

        sys.exit(0)

    if args.compile:
        if not Settings.hide_logo:
            print_logo()

        cmd_compile()

        sys.exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
