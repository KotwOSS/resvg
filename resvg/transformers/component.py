# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from transformer import Transformer
from component import Component
from lxml import etree


class ComponentTransformer(Transformer):
    def __call__(self, el: etree._Element) -> bool:
        if el.tag in Component.components:
            comp = Component.components[el.tag](self.transformer, el)
            comp.parse()
            return True
