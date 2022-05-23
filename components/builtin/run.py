from components import register_component
from components.component import Component
from components.expression import Expression
from components.statement import RawStatement
from components.logging import Logger


class RunComponent(Component):
    arguments = {}

    def run(self, args):
        nodes = self.childnodes()

        code = ""

        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                code += node.data
            else:
                Logger.logger.exit_fatal(f"Run component may only contain text!")

        RawStatement().parse(code, self.transformer).exec()

        self.destroy()


register_component("run", RunComponent)
