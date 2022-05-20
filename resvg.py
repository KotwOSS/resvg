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


# colors
red = "\033[38;2;255;100;100m"
blue = "\033[38;2;100;100;255m"
orange = "\033[38;2;255;150;0m"
yellow = "\033[38;2;255;205;50m"
gray = "\033[38;2;180;180;180m"
reset = "\033[0m"
bold = "\033[1m"


# Import the required modules
try:
    from argparse import HelpFormatter
    import sys, re
    from xml.dom import minidom
    from time import time
    from argparse import SUPPRESS
    import argparse
except ImportError as e:
    print(f"{red}ERROR{reset} missing required module: {e}")
    sys.exit(1)


# Color formating
colors = {
    "§B": bold,
    "§R": reset,
    "§r": red,
    "§o": orange,
    "§b": blue,
    "§y": yellow,
    "§g": gray,
}

colors_regex = re.compile("§[a-zA-Z]")

# Remove all the color codes in a string
def remove_colors(text):
    return colors_regex.sub("", text)


# Format all the color codes in a string
def format_colors(text):
    for key, value in colors.items():
        text = text.replace(key, value)
    return text


# Logging
logger = None

# Logger class
class Logger:
    DEBUG = -1
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    def __init__(self, level, stream):
        self.level = level
        self.stream = stream

    def call(self, level, message):
        if self.level <= level:
            self.stream.write(message)


# CombinedLogger to combine multiple loggers
class CombinedLogger(Logger):
    def __init__(self, loggers):
        self.loggers = loggers

    def call(self, name, message):
        return [
            getattr(logger, name)(message) if logger else None
            for logger in self.loggers
        ]

    def debug(self, message):
        return self.call("debug", message)

    def info(self, message):
        return self.call("info", message)

    def warning(self, message):
        return self.call("warning", message)

    def error(self, message):
        return self.call("error", message)

    def fatal(self, message):
        return self.call("fatal", message)


# SimpleLogger for log files
class SimpleLogger(Logger):
    def debug(self, message):
        self.call(Logger.DEBUG, f"[DEBUG] {remove_colors(message)}\n")

    def info(self, message):
        self.call(Logger.INFO, f"[INFO] {remove_colors(message)}\n")

    def warning(self, message):
        self.call(Logger.WARNING, f"[WARNING] {remove_colors(message)}\n")

    def error(self, message):
        self.call(Logger.ERROR, f"[ERROR] {remove_colors(message)}\n")

    def fatal(self, message):
        self.call(Logger.FATAL, f"[FATAL] {remove_colors(message)}\n")


# PrettyLogger for stdout
class PrettyLogger(Logger):
    def debug(self, message):
        self.call(Logger.DEBUG, f"{gray}{bold}DEBUG{reset} {format_colors(message)}\n")

    def info(self, message):
        self.call(Logger.INFO, f"{blue}{bold}INFO{reset} {format_colors(message)}\n")

    def warning(self, message):
        self.call(
            Logger.WARNING, f"{yellow}{bold}WARNING{reset} {format_colors(message)}\n"
        )

    def error(self, message):
        self.call(Logger.ERROR, f"{red}{bold}ERROR{reset} {format_colors(message)}\n")

    def fatal(self, message):
        self.call(Logger.FATAL, f"{red}{bold}FATAL{reset} {format_colors(message)}\n")


# Transform nodes
class NodeTransform:
    expression_regex = re.compile("{([a-zA-Z0-9.*/+-^()\"' ]+)}")
    expression_vars_regex = re.compile("([a-zA-Z]+)")
    greater_regex = re.compile("\sgreater\s")
    smaller_regex = re.compile("\ssmaller\s")

    # Constructor
    def __init__(self, root):
        self.root = root
        self.vars = {}

    # Stringify a value
    def stringify(self, object):
        if isinstance(object, float):
            return f"{object:10.3f}".strip()
        else:
            return str(object)

    # Execute an expression
    def exec_expression(self, exp):
        exp = self.greater_regex.sub(">", exp)
        exp = self.smaller_regex.sub("<", exp)

        exp_vars = self.expression_vars_regex.finditer(exp)

        endidx = 0
        txt = ""
        for var in exp_vars:
            txt += exp[endidx : var.start(0)]
            endidx = var.end(0)
            var = var.group(1)

            print

            if var in self.vars:
                txt += str(self.vars[var])
            else:
                logger.debug(f"Variable §o'{var}'§R not found! Inserting as text...")
                txt += var

        txt += exp[endidx:]

        try:
            return eval(txt)
        except Exception as e:
            logger.fatal(f"Error while evaluating expression §o'{txt}'§R: {e}")
            sys.exit(1)

    # Repeat component
    def comp_repeat(self, node, parent, before):
        if node.hasAttributes():
            attr = node.attributes.item(0)
            var = attr.name.strip()
            range = attr.value.strip()
            start, end, step = range.split(";")

            start = float(start)
            end = float(end)
            step = float(step)

            drc = start <= end

            self.vars[var] = start
            while self.vars[var] <= end if drc else self.vars[var] >= end:
                for child in list(node.childNodes):
                    clone = child.cloneNode(True)
                    transformed = self.transform_node(clone, parent, node)

                    if transformed:
                        parent.insertBefore(transformed, before if before else node)

                self.vars[var] += step
        else:
            logger.warning("Repeat component should have attributes! Skipping...")

        if not before:
            parent.removeChild(node)

    # Define component
    def comp_define(self, node, parent, before):
        if node.hasAttributes():
            attrs = node.attributes
            for i in range(0, attrs.length):
                attr = attrs.item(i)
                var = attr.name
                value = attr.value

                if value.isnumeric():
                    self.vars[var] = float(value)
                else:
                    self.vars[var] = value

                logger.debug(f"Defined variable §o'{var}'§R with value §o'{value}'§R")
        else:
            logger.warning("Define component should have attributes! Skipping...")

        if not before:
            parent.removeChild(node)

    # If component
    def comp_if(self, node, parent, before):
        condition = node.getAttribute("cond").strip()

        result = self.exec_expression(condition)

        if isinstance(result, bool):
            if result:
                for child in list(node.childNodes):
                    clone = child.cloneNode(True)
                    transformed = self.transform_node(clone, parent, node)

                    if transformed:
                        parent.insertBefore(transformed, before if before else node)
        else:
            logger.warning(
                f"If condition §o'{condition}'§R didn't return a boolean value! Ignoring..."
            )

        if not before:
            parent.removeChild(node)

    # The available components
    components = {"if": comp_if, "repeat": comp_repeat, "define": comp_define}

    # Transform a node
    def transform_node(self, node, parent, before):
        if node.nodeType == node.TEXT_NODE:
            node.data = node.data.strip()
            return

        if node.nodeType == node.COMMENT_NODE:
            if not before:
                parent.removeChild(node)
            return

        if node.hasAttributes():
            attrs = node.attributes
            for i in range(0, attrs.length):
                attr = attrs.item(i)
                val = attr.value

                res = self.expression_regex.finditer(attr.value)

                endidx = 0
                txt = ""
                for exp in res:
                    txt += val[endidx : exp.start(0)]
                    endidx = exp.end(0)
                    exp = exp.group(1)

                    txt += self.stringify(self.exec_expression(exp))

                attr.value = txt + val[endidx:]

        if node.nodeName in self.components:
            return self.components[node.nodeName](self, node, parent, before)
        elif node.hasChildNodes():
            for child in list(node.childNodes):
                self.transform_node(child, node, before)

        return node

    def transform(self):
        self.transform_node(self.root, self.root, None)


# Compile a file
def compile(src, dest):
    start = time()

    doc = minidom.parse(src)

    root = doc.documentElement

    transformer = NodeTransform(root)
    transformer.transform()

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
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process some integers.", formatter_class=help_formatter
    )

    parser.add_argument("--log", dest="log", help="specify a log file", type=str)

    parser.add_argument(
        "--level", dest="level", help="specify a log level", type=int, default=0
    )

    parser.add_argument(
        "-s", "--silent", dest="silent", help="run in silent mode", action="store_true"
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

    loglevel = args.level

    std_logger = None
    if not args.silent:
        std_logger = PrettyLogger(loglevel, sys.stdout)

    file_logger = None
    if args.log:
        file_logger = SimpleLogger(loglevel, open(args.log, "a"))

    logger = CombinedLogger([file_logger, std_logger])

    if args.version:
        cmd_version()
        sys.exit(0)

    if args.compile:
        if not args.silent:
            print_logo()

        input_file = args.input
        output_file = args.output

        output_stream = open(output_file, "w") if output_file else sys.stdout

        logger.info(
            f"Compiling §o'{input_file}'§R to §o'{output_file if output_file else 'stdout'}'§R"
        )

        took = compile(input_file, output_stream)

        if not output_file:
            print()

        logger.info(f"Compilation took §o{round(took * 1000)} ms.§R")

        sys.exit(0)
