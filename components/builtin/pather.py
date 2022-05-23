from typing import Dict
from components import register_component
from components.component import Component
from components.expression import Expression, MultiExpression, Raw
from components.statement import RawStatement
from components.logging import Logger


class AppendComponent(Component):
    arguments = { "d": Raw(str) }

    def run(self, args):
        self.transformer.paths.append(args["d"])

        self.destroy()

register_component("append", AppendComponent)


class CloseComponent(Component):
    arguments = {}

    def run(self, args):
        self.transformer.paths.append("Z")

        self.destroy()

register_component("close", CloseComponent)


class LineComponent(Component):
    arguments = {
        "?from": MultiExpression(float, float),
        "?fx": Expression(float),
        "?fy": Expression(float),
        "?to": MultiExpression(float, float),
        "?tx": Expression(float),
        "?ty": Expression(float),
    }

    def run(self, args):
        arg_from = args["from"] if "from" in args else [args["fx"], args["fy"]] \
            if "fx" in args and "fy" in args else None
        arg_to = args["to"] if "to" in args else [args["tx"], args["ty"]] \
            if "tx" in args and "ty" in args else None

        str_from = f"{self.stringify(arg_from[0])} {self.stringify(arg_from[1])}" if arg_from else None
        str_to = f"{self.stringify(arg_to[0])} {self.stringify(arg_to[1])}" if arg_to else None

        if str_from: self.transformer.paths.append("M " + str_from)
        elif len(self.transformer.paths) == 0 and str_to:
            self.transformer.paths.append("M " + str_to)
        if str_to: self.transformer.paths.append("L " + str_to)

        self.destroy()

register_component("line", LineComponent)


class PatherComponent(Component):
    arguments = { "*": Raw(str) }

    def run(self, args):
        self.insert_nodes_before(self.childnodes())

        # self.transformer.paths.append("Z")

        el = self.transformer.doc.createElement("path")
        el.setAttribute("d", " ".join(self.transformer.paths))

        for arg in args["*"]:
            el.setAttribute(arg.name, arg.value)

        self.insert_before(el)

        self.destroy()

register_component("pather", PatherComponent)