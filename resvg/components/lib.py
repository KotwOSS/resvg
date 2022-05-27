# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Dict, List
from component import Component
from raw import Raw
from lxml import etree

class Library:
    components: Dict[str, List[etree._Element]]
    def __init__(self):
        self.components = {}

class Lib(Component):
    use_last = True
    use_data = ["libraries"]
    arguments = {
        "ns": (lambda an, av: an == "ns", Raw(str)),
    }

    def run(self):
        if not self.data.has("library"):
            library = Library()
            
            ns = self.ns[1]
            self.libraries[ns] = library
            
            self.data.set("library", library)
        else:
            raise RuntimeError("Library component can not be in another library")

    def last(self):
        self.data.remove("library")
        self.destroy(children=False)