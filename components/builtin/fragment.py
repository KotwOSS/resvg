from components import register_component
from components.component import Component


class FragmentComponent(Component):
    arguments = {}

    def run(self, args):
        self.insert_nodes_before(self.childnodes())

        self.destroy()


register_component("fragment", FragmentComponent)
