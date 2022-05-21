from components import register_component
from components.component import Component
from components.expression import Expression, Raw

class RepeatComponent(Component):
    arguments = {
        "*:1": Expression[int]
    }

    def run(self, args):
        nodes = self.childnodes()
        count_argument = args["*"][0]

        variable = count_argument["name"]
        if variable == "_":
            variable = None
        
        count = count_argument["value"]
        for i in range(count):
            if variable:
                self.transformer.vars[variable] = i
            self.insert_nodes_before(nodes)

        self.destroy()

register_component("repeat", RepeatComponent)

class WhileComponent(Component):
    arguments = {
        "cond": Raw[str]
    }

    def run(self, args):
        nodes = self.childnodes()
        cond = args["cond"]
        expressioner = Expression[bool](self.transformer)
        
        while expressioner.parse(cond):
            self.insert_nodes_before(nodes)

        self.destroy()

register_component("while", WhileComponent)