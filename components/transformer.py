import re
from typing import Any

from components.settings import Settings
from components.logging import Logger
from util.regex import multi_replace
from .expression import RawExpression
from . import components

# Transform nodes
class NodeTransform:
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")
    text_expression_regex = re.compile(r"\${([a-zA-Z0-9.*/+-^()\"' ]+)}")
    # Constructor
    def __init__(self, doc, root):
        self.root = root
        self.doc = doc
        self.vars = {}
        self.comps = {}
        self.slots = []
        self.paths = []

    # Stringify a value
    def stringify(self, object):
        if isinstance(object, float):
            return f"{object:10.3f}".strip()
        else:
            return str(object)

    def set_var(self, name, value):
        Logger.logger.debug(f"Set variable §o'{name}'§R to §o'{value}'§R")

        self.vars[name] = value

    def define_comp(self, name, nodes):
        Logger.logger.debug(f"Define comp §o'{name}'§R")

        self.comps[name] = nodes

    def append_slot(self, slot):
        Logger.logger.debug(f"Append slot")

        self.slots.append(slot)

    def pop_slot(self):
        Logger.logger.debug(f"Pop slot")

        return self.slots.pop()

    def get_slot(self):
        return self.slots[-1] if len(self.slots) > 0 else None

    def transform_attributes(self, node):
        if node.hasAttributes():
            attrs = node.attributes
            for i in range(0, attrs.length):
                attr = attrs.item(i)

                attr.value = multi_replace(
                    attr.value.strip(),
                    self.expression_regex,
                    lambda exp: self.stringify(
                        RawExpression(Any).parse(exp.group(1), self).eval()
                    ),
                )

    # Transform a node
    def transform_node(self, node, parent, before):
        if node.nodeType == node.TEXT_NODE:
            node.data = multi_replace(
                node.data.strip(),
                self.text_expression_regex,
                lambda exp: self.stringify(
                    RawExpression(Any).parse(exp.group(1), self).eval()
                ),
            )
            return node

        if node.nodeType == node.COMMENT_NODE:
            if not Settings.comments:
                if not before:
                    parent.removeChild(node)
                return None
            else:
                return node

        self.transform_attributes(node)

        if node.nodeName in components:
            return components[node.nodeName](node, parent, before, self).transform()
        elif node.nodeName in self.comps:
            self.append_slot(list(node.childNodes) if node.hasChildNodes() else [])

            if node.hasAttributes():
                for i in range(0, node.attributes.length):
                    attr = node.attributes.item(i)
                    self.set_var(attr.name, RawExpression(Any).parse(attr.value, self).eval())

            nodes = self.comps[node.nodeName]
            for child in nodes:
                clone = child.cloneNode(True)
                transformed = self.transform_node(
                    clone, parent, before if before else node
                )
                if transformed:
                    parent.insertBefore(transformed, before if before else node)

            if not before:
                parent.removeChild(node)

            self.pop_slot()
        elif node.hasChildNodes():
            for child in list(node.childNodes):
                self.transform_node(child, node, before)

        return node

    def transform(self):
        self.transform_node(self.root, self.root, None)
