# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List
from component import Component
from transformer import Transformer
from lxml import etree

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

class CustomTransformer(Transformer):
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
                comp = Custom(self.transform, el)
                comp.comp = lib.components[ln]
                comp.parse()
                return True
