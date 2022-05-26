# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any
from lxml import etree


class ProxiedDomSettings:
    transformer: Any


class ProxiedDom:
    def create(tag: str, attrib: Any = None, nsmap: Any = None, *_extra):
        """Create an element with the given name."""
        return etree.Element(tag, attrib=attrib, nsmap=nsmap, *_extra)

    def insert_before(el: etree._Element):
        """Insert element before the active node"""
        ProxiedDomSettings.transformer.active.addprevious(el)
