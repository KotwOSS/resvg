import re
from typing import Any

from util.logging import Logger
from util.regex import multi_replace
from .expression import Expression
from . import components

# Transform nodes
class NodeTransform:
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")
    text_expression_regex = re.compile(r"\${([a-zA-Z0-9.*/+-^()\"' ]+)}")
    # Constructor
    def __init__(self, root):
        self.root = root
        self.vars = {}

    # Stringify a value
    def stringify(self, object):
        if isinstance(object, float):
            return f"{object:10.3f}".strip()
        else:
            return str(object)

    # Transform a node
    def transform_node(self, node, parent, before):
        if node.nodeType == node.TEXT_NODE:
            node.data = multi_replace(node.data.strip(), self.text_expression_regex, 
                lambda exp: self.stringify(Expression[Any](self).parse(exp.group(1))))
            return node

        if node.nodeType == node.COMMENT_NODE:
            if not before:
                parent.removeChild(node)
            return node

        if node.hasAttributes():
            attrs = node.attributes
            for i in range(0, attrs.length):
                attr = attrs.item(i)

                attr.value = multi_replace(attr.value.strip(), self.expression_regex, 
                    lambda exp: self.stringify(Expression[Any](self).parse(exp.group(1))))

        if node.nodeName in components:
            return components[node.nodeName](node, parent, before, self).transform()
        elif node.hasChildNodes():
            for child in list(node.childNodes):
                self.transform_node(child, node, before)

        return node

    def transform(self):
        self.transform_node(self.root, self.root, None)
