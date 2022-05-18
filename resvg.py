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
yellow = "\033[38;2;255;255;0m"
reset = "\033[0m"


import sys, re
from xml.dom import minidom

# Transform nodes
class NodeTransform:
    expression_regex = re.compile("{([a-zA-Z0-9.*/+-^()]+)}")
    vars = {}

    def __init__(self, root):
        self.root = root

    def repeat(self, node):
        parent = node.parentNode

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
                cloned = child.cloneNode(True)
                self.transform_node(cloned)

                parent.insertBefore(cloned, node)

            self.vars[var] += step
        
        parent.removeChild(node)


    def transform_node(self, node):
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

                    for (var, value) in self.vars.items():
                        exp = exp.replace(var, str(value))
                    
                    txt += f"{eval(exp):10.3f}".strip()

                attr.value = txt + val[endidx:]

        if node.nodeName == "repeat":
            self.repeat(node)
        elif node.hasChildNodes():
            for child in list(node.childNodes):
                self.transform_node(child)

    def transform(self):
        self.transform_node(self.root)



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
    with open(src, "rb") as src:
        doc = minidom.parse(src)

        root = doc.documentElement
        
        transformer = NodeTransform(root)
        transformer.transform()
        
        #print(transformer.root.toprettyxml())

        with open(dest, "w") as dest:
            doc.documentElement.writexml(dest)

        doc.unlink()



def cmd_compile():
    src = require_arg("src", 2)
    dest = require_arg("dest", 3)
    compile(src, dest)


def cmd_help():
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
    print(f"{sys.argv[0]} {orange}help{reset}")
    print("\tShows this help.\n")
    print(f"{sys.argv[0]} {orange}compile{reset} <source> <destination>")
    print("\tCompiles the SVG file.\n")
    print(f"{sys.argv[0]} {orange}version{reset}")
    print("\tShows the version.\n")


def cmd_version():
    print(version)


operand = require_arg_or(1, help)
operands = {
    "compile": cmd_compile,
    "help": cmd_help,
    "version": cmd_version
}

if operand in operands:
    operands[operand]()
else:
    print(f"{red}ERROR:{reset} Unknown opperand '{operand}'")