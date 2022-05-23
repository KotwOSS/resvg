import os
from typing import Any
from xml.dom import minidom
from components import register_component
from components.component import Component
from components.expression import Expression, Raw
from components.logging import Logger


class IncludeComponent(Component):
    arguments = {"path": Raw(str), "*": Expression(Any)}

    def run(self, args):
        path = args["path"]

        if os.path.exists(path):
            Logger.logger.debug(f"Including §o'{path}'§R")
            node = minidom.parse(path).documentElement

            for arg in args["*"]:
                self.set_var(arg.name, arg.value)

            self.transformer.append_slot(self.childnodes_or_empty())

            self.insert_before(self.transform_node(node))

            self.transformer.pop_slot()

            Logger.logger.debug(f"Successfully included §o'{path}'§R")
        else:
            Logger.logger.exit_fatal(f"File §o'{path}'§R doesn't exist!")

        self.destroy()


register_component("include", IncludeComponent)
