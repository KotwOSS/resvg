from abc import ABC, abstractmethod
from typing import Any, Dict

from components.logging import Logger

# Component class
class Component(ABC):
    arguments: Dict[str, Any]

    def __init__(self, node, parent, before, transformer):
        self.node = node
        self.parent = parent
        self.before = before
        self.transformer = transformer

    def stringify(self, val: Any):
        """Stringify a value"""
        if isinstance(val, str):
            return val
        elif isinstance(val, int):
            return str(val)
        elif isinstance(val, float):
            if val.is_integer():
                return str(int(val))
            else:
                return str(float(f"{val:10.3f}"))
        else:
            return str(val)

    def destroy(self):
        """Destroy the component"""
        if not self.before:
            self.parent.removeChild(self.node)

    def childnodes(self):
        """Return the child nodes of the component as a list"""
        if self.node.hasChildNodes():
            return list(self.node.childNodes)
        else:
            Logger.logger.exit_fatal(
                f"Component §o{type(self).__name__}§R has to have childNodes!"
            )

    def childnodes_or_empty(self):
        """Return the child nodes of the component as a list or an empty list"""
        if self.node.hasChildNodes():
            return list(self.node.childNodes)
        else:
            return []

    def set_var(self, name, value):
        """Set a variable"""
        self.transformer.set_var(name, value)

    def insert_before(self, node):
        """Insert a node before the component"""
        if node:
            return self.parent.insertBefore(node, self.get_before())

    def insert_nodes_before(self, nodes):
        """Insert a list of nodes before the component. (This will clone the nodes)"""
        for node in nodes:
            clone = node.cloneNode(True)
            self.insert_before(self.transform_node(clone))

    def transform_node(self, node):
        """Transform a node"""
        return self.transformer.transform_node(node, self.parent, self.get_before())

    def transform(self) -> Any:
        attributes = self.node.attributes
        args: Dict[str, Any] = {}
        for (attrname, instance) in self.arguments.items():
            if attrname.startswith("*"):
                attrval = []
                for i in range(attributes.length):
                    attr = attributes.item(i)
                    if attr.name not in args:
                        attrval.append(
                            Argument.from_attr(attr, instance, self.transformer)
                        )
                args["*"] = attrval
                if len(attrname) > 1:
                    last = attrname[-1:]
                    min_or_max = last == "-" or last == "+"
                    count = len(attrval)
                    expected_count = int(attrname[2:-1] if min_or_max else attrname[2:])

                    if min_or_max:
                        if last == "-":
                            condition = count <= expected_count
                        elif last == "+":
                            condition = count >= expected_count
                    else:
                        condition = count == expected_count

                    if not condition:
                        Logger.logger.exit_fatal(
                            f"Expected §o'{expected_count}'{last if min_or_max else ''}§R arguments for component §o'{type(self).__name__}'§R but found §o'{count}'§R!"
                        )
            else:
                optional = attrname.startswith("?")
                if optional:
                    attrname = attrname[1:]

                attr = attributes.getNamedItem(attrname)
                if attr:
                    attrval = instance.parse(attr.value, self.transformer)
                    args[attrname] = attrval
                elif not optional:
                    Logger.logger.exit_fatal(
                        f"Component §o'{type(self).__name__}'§R has to have attribute §o'{attrname}'§R!"
                    )

        return self.run(args)

    @abstractmethod
    def run(self, args: Dict[str, Any]) -> Any:
        pass


class Argument:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def from_attr(attr, instance, transformer):
        return Argument(attr.name, instance.parse(attr.value, transformer))
