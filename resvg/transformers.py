# Created on Sat May 28 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, Dict, List
from transformer import Transformer
from evaluator import SafeExpression, Expression, Raw
from settings import Settings
from component import Component
from lxml import etree
from transform import Transform
import reutil, re, logging


# ANCHOR: AttributeTransformer
class AttributeTransformer(Transformer):
    """Transform expressions in attributes"""
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")

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
                name = attrname[len(Settings.exp_namespace):]
                el.attrib[name] = reutil.stringify(
                    SafeExpression(attrval, self.transform.vars, Any).eval()
                )
                del el.attrib[attrname]
                continue
            elif attrname.startswith(Settings.resvg_namespace):
                name = attrname[len(Settings.resvg_namespace):]
                if name == "insert":
                    res = SafeExpression(attrval, self.transform.vars, Dict | List).eval()
                    
                    if isinstance(res, Dict):
                        res = res.items()
                    
                    for (n, v) in res:
                        el.attrib[n] = reutil.stringify(v)
                    del el.attrib[attrname]
                    continue
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
        
        use_data = ["slots"]

        slots: List[List[etree._Element]]
        comp: List[etree._Element]
        el: etree._Element
        
        arguments = {
            "any_re*": (lambda an, av: an.startswith(Settings.resvg_namespace), Expression(Any), True),
            "any*": (lambda an, av: True, Raw(str), True)
        }
        
        def run(self):
            self.transform.append_scope(clone=False)
            
            resvg_ns_l = len(Settings.resvg_namespace)
            for (an, av) in self.any_re:
                an = an[resvg_ns_l:].replace("-", "_")
                if not an in self.transform.vars:
                    self.transform.set_var(an, av)
            
            for (an, av) in self.any:
                an = an.replace("-", "_")
                if not an in self.transform.vars:
                    self.transform.set_var(an, av)
                    
            self.slots.append(self.el.getchildren())

            cloned = [self.clone(el, add_jobs=True) for el in self.comp]
            self.insert_before(cloned)

            self.destroy(children=True)

            self.add_job(self._last, complete=True)

        def last(self):
            self.slots.pop()
            
            self.transform.pop_scope()
    
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
                logging.debug("insert §o%s§R:§o%s§R", ns, ln)
                comp = CustomTransformer.Custom(self.transform, el)
                comp.comp = lib.components[ln]
                comp.parse()
                return True


def register():
    """Register the default transformers"""
    Transform.register_default_transformer(AttributeTransformer)
    Transform.register_default_transformer(ComponentTransformer)
    Transform.register_default_transformer(CustomTransformer)
