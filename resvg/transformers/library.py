# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from copy import deepcopy
from transformer import Transformer
from lxml import etree
from components.library import Library

class LibraryTransformer(Transformer):
    def add_jobs(self, el: etree._Element, include_self: bool = True):
        """Add child jobs"""
        for child in el.iter():
            if include_self or child != el:
                self.transformer.add_job(child)
    
    def __call__(self, el: etree._Element) -> bool:
        qname = etree.QName(el.tag)
        ns = qname.namespace
        ln = qname.localname
        if ns in Library.libraries:
            lib = Library.libraries[ns]
            if ln in lib.components:
                comp = lib.components[ln]
                for child in comp:
                    clone = deepcopy(child)
                    self.add_jobs(clone)
                    el.addprevious(clone)
                el.getparent().remove(el)
