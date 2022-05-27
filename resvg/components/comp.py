# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from component import Component
from raw import Raw
from components.lib import Library
import logging


class Comp(Component):
    arguments = {
        "name": (lambda an, av: an == "name", Raw(str), True),
    }

    def run(self):
        if self.data.has("library"):
            name = self.name[1]
            library: Library = self.data.get("library")
            logging.info("Registered component §o%s§R:§o%s§R", library.ns, name)
            library.components[name] = self.clone_children(add_jobs=False)
        else:
            raise RuntimeError("§ocomp§R components can only be in a library")

        self.destroy()
