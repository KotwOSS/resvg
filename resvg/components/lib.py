# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from raw import Raw


class Lib(Component):
    use_after = True
    arguments = {
        "ns": (lambda an, av: an == "ns", Raw(str)),
    }

    def run(self):
        self.ns = self.ns[1]

    def after(self):
        self.destroy()
