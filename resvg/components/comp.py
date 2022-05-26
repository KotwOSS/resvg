# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Dict
from component import Component
from raw import Raw
from components.library import Library

class Comp(Component):
    arguments = {
        "name": (lambda an, av: an == "name", Raw(str)),
    }

    def run(self):
        if Library.library:
            Library.library.components[self.name[1]] = self.clone_children(add_jobs=False)
        else:
            raise RuntimeError("Comp components can only be in a library")

        self.destroy()