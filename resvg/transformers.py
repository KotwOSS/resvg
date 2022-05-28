# Created on Sat May 28 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, List
from transformer import Transformer
from evaluator import SafeExpression
from settings import Settings
from component import Component
from lxml import etree
from transform import Transform
import reutil, re

# ANCHOR: AttributeTransformer
class AttributeTransformer(Transformer):
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")

    """Transform expressions in attributes"""

    def __call__(self, el: etree._Element) -> bool:
        for attr in el.attrib.items():
            attrname = attr[0]
            attrval = attr[1]

            attrval = reutil.multi_replace(
                attrval,
                self.expression_regex,
                lambda exp: reutil.stringify(
                    SafeExpression(exp.group(1), self.transform.vars, Any).eval()
                ),
            )

            if attrname.startswith(Settings.exp_namespace):
                name = attrname[len(Settings.exp_namespace) :]
                el.attrib[name] = reutil.stringify(
                    SafeExpression(attrval, self.transform.vars, Any).eval()
                )
                del el.attrib[attrname]
            else:
                el.attrib[attrname] = attrval
        return False

# ANCHOR: ComponentTransformer
class ComponentTransformer(Transformer):
    def __call__(self, el: etree._Element) -> bool:
        if el.tag in Component.components:
            comp = Component.components[el.tag](self.transform, el)
            comp.parse()
            return True
        

# ANCHOR: CustomTransformer
class CustomTransformer(Transformer):
    # ANCHOR: Custom
    class Custom(Component):
        arguments = {}
        # use_last = True
        use_data = ["slots"]

        comp: List[etree._Element]
        el: etree._Element

        def run(self):
            self.slots.append(self.el.getchildren())

            cloned = [self.clone(el, add_jobs=True) for el in self.comp]
            self.insert_before(cloned)

            self.destroy(children=True)

            self.add_job(self._last, complete=True)

        def last(self):
            self.slots.pop()
    
    def add_jobs(self, el: etree._Element, include_self: bool = True):
        """Add child jobs"""
        for child in el.iter():
            if include_self or child != el:
                self.transform.add_job(child)

    def __call__(self, el: etree._Element) -> bool:
        qname = etree.QName(el.tag)
        ns = qname.namespace
        ln = qname.localname
        libraries = self.data.get("libraries")
        if ns in libraries:
            lib = libraries[ns]
            if ln in lib.components:
                comp = CustomTransformer.Custom(self.transform, el)
                comp.comp = lib.components[ln]
                comp.parse()
                return True


def register():
    """Register the default transformers"""
    Transform.register_default_transformer(AttributeTransformer)
    Transform.register_default_transformer(ComponentTransformer)
    Transform.register_default_transformer(CustomTransformer)
