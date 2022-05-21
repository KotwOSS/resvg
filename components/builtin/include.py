import os
from typing import Any
from xml.dom import minidom
from components import register_component
from components.component import Component
from components.expression import Expression, Raw
from util.logging import Logger


class IncludeComponent(Component):
    arguments = {"path": Raw[str], "*": Expression[Any]}

    def run(self, args):
        path = args["path"]

        if os.path.exists(path):
            Logger.logger.debug(f"Including §o'{path}'§R")
            node = minidom.parse(path).documentElement

            for arg in args["*"]:
                self.set_var(arg.name, arg.value)

            self.insert_before(self.transform_node(node))

            Logger.logger.debug(f"Successfully included §o'{path}'§R")
        else:
            Logger.logger.exit_fatal(f"File §o'{path}'§R doesn't exist!")

        self.destroy()


register_component("include", IncludeComponent)
