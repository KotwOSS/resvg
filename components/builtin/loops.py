from typing import Any
from components import register_component
from components.component import Component
from components.expression import Expression, Raw, RawExpression
from components.statement import RawStatement
from util.logging import Logger


class RepeatComponent(Component):
    arguments = {"*:1": Expression[int]}

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
    arguments = {"cond": RawExpression[str]}

    def run(self, args):
        nodes = self.childnodes()
        cond = args["cond"]

        while cond.eval():
            self.insert_nodes_before(nodes)

        self.destroy()


register_component("while", WhileComponent)


class ForComponent(Component):
    arguments = {
        "*:1": Raw[str]
    }

    def run(self, args):
        nodes = self.childnodes()

        statement = args["*"][0]

        variable = statement.name

        segments = statement.value.split(";")

        if len(segments) == 3:
            start = RawExpression[Any](self.transformer).parse(segments[0]).eval()
            cond = RawExpression[bool](self.transformer).parse(segments[1])
            after = RawStatement(self.transformer).parse(segments[2])

            self.transformer.set_var(variable, start)
            while cond.eval():
                self.insert_nodes_before(nodes)
                after.exec()
        else:
            Logger.logger.exit_fatal(f"Bad formated for statement: §o'{statement}'§R!")

        self.destroy()


register_component("for", ForComponent)
