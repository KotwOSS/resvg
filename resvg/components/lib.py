# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Dict, List
from component import Component
import logging
from raw import Raw
from lxml import etree


class Library:
    components: Dict[str, List[etree._Element]]
    ns: str

    def __init__(self, ns):
        self.components = {}
        self.ns = ns


class Lib(Component):
    use_last = True
    use_data = ["libraries"]
    arguments = {
        "ns": (lambda an, av: an == "ns", Raw(str), True),
    }

    def run(self):
        if not self.data.has("library"):
            ns = self.ns[1]

            logging.debug("start library §o%s§R", ns)

            if ns in self.libraries:
                library = self.libraries[ns]
            else:
                logging.info("Registered library §o%s§R", ns)
                library = Library(ns)
                self.libraries[ns] = library

            self.data.set("library", library)
        else:
            raise RuntimeError("Library component can not be in another library")

    def last(self):
        logging.debug("end library")
        self.data.remove("library")
        self.destroy(children=False)
