# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from component import Component
from raw import Raw
from components.lib import Library

class Comp(Component):
    arguments = {
        "name": (lambda an, av: an == "name", Raw(str)),
    }

    def run(self):
        if self.data.has("library"):
            self.data.get("library", Library).components[self.name[1]] = self.clone_children(add_jobs=False)
        else:
            raise RuntimeError("Comp components can only be in a library")

        self.destroy()