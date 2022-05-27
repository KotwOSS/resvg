# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from expression import Expression


class If(Component):
    arguments = {
        "cond": (lambda an, av: an == "cond", Expression(bool)),
    }

    def run(self):
        cond = self.cond[1]
        if cond:
            self.move_before()
        self.destroy(children=not cond)
