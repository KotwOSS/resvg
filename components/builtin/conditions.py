from components import register_component
from components.component import Component
from components.expression import Expression

class IfComponent(Component):
    arguments = {
        "cond": Expression[bool]
    }

    def run(self, args):
        if args["cond"]:
            self.insert_nodes_before(self.childnodes())

        self.destroy()

register_component("if", IfComponent)