from typing import Any
from components import register_component
from components.component import Component
from components.expression import Expression, Raw, RawExpression
from components.statement import RawStatement
from components.logging import Logger


class RepeatComponent(Component):
    arguments = {"*:1": Expression(int)}

    def run(self, args):
        nodes = self.childnodes()
        count_argument = args["*"][0]

        variable = count_argument.name
        if variable == "_":
            variable = None

        count = count_argument.value
        for i in range(count):
            if variable:
                self.transformer.vars[variable] = i
            self.insert_nodes_before(nodes)

        self.destroy()


register_component("repeat", RepeatComponent)


class WhileComponent(Component):
    arguments = {"cond": RawExpression(str)}

    def run(self, args):
        nodes = self.childnodes()
        cond = args["cond"]

        while cond.eval():
            self.insert_nodes_before(nodes)

        self.destroy()


register_component("while", WhileComponent)


class ForComponent(Component):
    arguments = {"*:1": Raw(str)}

    def run(self, args):
        nodes = self.childnodes()

        statement = args["*"][0]

        variable = statement.name

        segments = statement.value.split(";")

        if len(segments) == 3:
            start = RawExpression(Any).parse(segments[0], self.transformer).eval()
            cond = RawExpression(bool).parse(segments[1], self.transformer)
            after = RawStatement().parse(segments[2], self.transformer)

            self.transformer.set_var(variable, start)
            while cond.eval():
                self.insert_nodes_before(nodes)
                after.exec()
        elif len(segments) == 1:
            range_val = RawExpression(range).parse(segments[0], self.transformer).eval()

            for i in range_val:
                self.transformer.set_var(variable, i)
                self.insert_nodes_before(nodes)
        else:
            Logger.logger.exit_fatal(
                f"Bad formated for statement: §o'{statement.value}'§R!"
            )

        self.destroy()


register_component("for", ForComponent)
