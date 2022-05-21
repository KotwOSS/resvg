import math, random, re
from components import register_component
from components.component import Component
from components.expression import Expression
from util.logging import Logger

class RunComponent(Component):
    arguments = {
    }

    exec_globals = {
        "import": None,
        "__import__": None,
        "open": None,
        "exec": None,
        "eval": None,
        "math": math,
        "random": random,
    }

    import_regex = re.compile(r"import\s+.+")

    def run(self, args):
        nodes = self.childnodes()

        code = ""

        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                code += node.data
            else:
                Logger.logger.exit_fatal(f"Run component may only contain text!")

        if self.import_regex.search(code):
            Logger.logger.exit_fatal(f"Run component may not contain imports!")
        else:
            exec(code, self.exec_globals, self.transformer.vars)

        self.destroy()

register_component("run", RunComponent)