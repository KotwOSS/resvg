from components import register_component
from components.component import Component
from components.expression import Raw


class CompComponent(Component):
    arguments = {"name": Raw(str)}

    def run(self, args):
        self.transformer.define_comp(args["name"], self.childnodes())

        self.destroy()


register_component("comp", CompComponent)
