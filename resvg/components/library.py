# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Dict, List
from component import Component
from raw import Raw
from lxml import etree

class Library:
    libraries: Dict[str, Library] = {}
    library: Library | None = None
    
    def reset():
        Library.libraries = {}
        Library.library = None
        
    components: Dict[str, List[etree._Element]]
    def __init__(self):
        self.components = {}

class Lib(Component):
    use_last = True
    arguments = {
        "ns": (lambda an, av: an == "ns", Raw(str)),
    }

    def run(self):
        if not Library.library:
            lib = self.ns[1]
            Library.library = Library()
            Library.libraries[lib] = Library.library
        else:
            raise RuntimeError("Library component can not be in another library")

    def last(self):
        Library.library = None
        self.destroy(children=False)