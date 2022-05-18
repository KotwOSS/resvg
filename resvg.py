#! /usr/bin/python3

# ██████╗░███████╗░██████╗██╗░░░██╗░██████╗░
# ██╔══██╗██╔════╝██╔════╝██║░░░██║██╔════╝░
# ██████╔╝█████╗░░╚█████╗░╚██╗░██╔╝██║░░██╗░
# ██╔══██╗██╔══╝░░░╚═══██╗░╚████╔╝░██║░░╚██╗
# ██║░░██║███████╗██████╔╝░░╚██╔╝░░╚██████╔╝
# ╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░░╚═════╝░
#
# ReSVG is a advanced SVG compiler which includes many features.
#
# It is licensed under the MIT license.
#
# (c) Copyright 2022 KotwOSS


version = "0.0.0alpha0"
authors = ["KotwOSS"]
license = "MIT"
year = 2022


# colors
red = "\033[38;2;255;100;100m"
blue = "\033[38;2;100;100;255m"
orange = "\033[38;2;255;150;0m"
yellow = "\033[38;2;255;205;50m"
reset = "\033[0m"


import sys, re
from xml.dom import minidom
from time import time

# Transform nodes
class NodeTransform:
    expression_regex = re.compile("{([a-zA-Z0-9.*/+-^()]+)}")
    expression_vars_regex = re.compile("([a-zA-Z]+)")
    vars = {}

    def __init__(self, root):
        self.root = root

    def repeat(self, node, parent, before):
        range = node.getAttribute("range").strip()
        var = node.getAttribute("var").strip()
        start, end, step = range.split(";")

        start = float(start)
        end = float(end)
        step = float(step)

        drc = start <= end

        self.vars[var] = start
        while (self.vars[var] <= end if drc else self.vars[var] >= end):
            for child in list(node.childNodes):
                clone = child.cloneNode(True)
                transformed = self.transform_node(clone, parent, node)

                if transformed:
                    parent.insertBefore(transformed, before if before else node)

            self.vars[var] += step
        
        if not before:
            parent.removeChild(node)

    def define(self, node, parent, before):
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

                print(f"{blue}DEFINED{reset} Variable {orange}'{var}'{reset} with value {orange}'{value}'{reset}")

        if not before:
            parent.removeChild(node)


    def transform_node(self, node, parent, before):
        if node.nodeType == node.TEXT_NODE:
            node.data = node.data.strip()
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
                    txt += val[endidx:exp.start(0)]
                    endidx = exp.end(0)
                    exp = exp.group(1)

                    exp_vars = self.expression_vars_regex.finditer(exp)

                    exp_endidx = 0
                    exp_txt = ""
                    for var in exp_vars:
                        exp_txt += exp[exp_endidx:var.start(0)]
                        exp_endidx = var.end(0)
                        var = var.group(1)

                        if var in self.vars:
                            exp_txt += str(self.vars[var])
                        else:
                            print(f"{red}NOT_FOUND{reset} Variable '{var}' not found! Inserting as text...")
                            exp_txt += var

                    exp_txt += exp[exp_endidx:]
                    
                    try:
                        txt += f"{eval(exp_txt):10.3f}".strip()
                    except Exception as e:
                        print(f"Error while evaluating expression '{exp_txt}'! Inserting as text...")
                        txt += exp_txt

                attr.value = txt + val[endidx:]

        if node.nodeName == "repeat":
            self.repeat(node, parent, before)
            return None
        elif node.nodeName == "define":
            self.define(node, parent, before)
            return None
        elif node.hasChildNodes():
            for child in list(node.childNodes):
                self.transform_node(child, parent, before)
        
        return node

    def transform(self):
        self.transform_node(self.root, self.root, None)



arglen = len(sys.argv)

def require_arg(name, index):
    if arglen <= index:
        print(f"{red}ERROR:{reset} Required argument '{name}' is missing.")
        sys.exit(1)
    else:
        return sys.argv[index]

def require_arg_or(index, func):
    if arglen <= index:
        func()
        sys.exit(1)
    else:
        return sys.argv[index]


def compile(src, dest):
    print_logo()

    print(f"{red}COMPILING{reset} {src} -> {dest}\n")

    start = time()

    with open(src, "rb") as src:
        doc = minidom.parse(src)

        root = doc.documentElement
        
        transformer = NodeTransform(root)
        transformer.transform()
        
        #print(transformer.root.toprettyxml())

        with open(dest, "w") as dest:
            doc.documentElement.writexml(dest)

        doc.unlink()

    took = time() - start

    print(f"\n{yellow}FINISHED{reset} Took {orange}{round(took * 1000)}ms{reset}")
    print("")


def print_logo():
    print(f"""{orange}
░█▀▀█ █▀▀ ░█▀▀▀█ ░█  ░█ ░█▀▀█ 
░█▄▄▀ █▀▀  ▀▀▀▄▄  ░█░█  ░█ ▄▄ 
░█ ░█ ▀▀▀ ░█▄▄▄█   ▀▄▀  ░█▄▄█
    {reset}""")
    print(f"ReSVG version {blue}{version}{reset}")
    print("\n")
    print(f"Written by {blue}{', '.join(authors)}{reset} licensed under {blue}{license}{reset}.")
    print("")
    print(f"{red}(c){reset} Copyright {year} {blue}{', '.join(authors)}{reset}")
    print("\n")


def cmd_compile():
    src = require_arg("src", 2)
    dest = require_arg("dest", 3)
    compile(src, dest)


def cmd_help():
    print_logo()
    print(f"{sys.argv[0]} {orange}help{reset}")
    print("\tShows this help.\n")
    print(f"{sys.argv[0]} {orange}compile{reset} <source> <destination>")
    print("\tCompiles the SVG file.\n")
    print(f"{sys.argv[0]} {orange}version{reset}")
    print("\tShows the version.\n")


def cmd_version():
    print(version)


operand = require_arg_or(1, cmd_help)
operands = {
    "compile": cmd_compile,
    "help": cmd_help,
    "version": cmd_version
}

if operand in operands:
    operands[operand]()
else:
    print(f"{red}ERROR:{reset} Unknown opperand '{operand}'")