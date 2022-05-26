# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from expression import Expression
from lxml import etree


class If(Component):
    arguments = {
        "cond": (lambda an, av: an == "cond", Expression(bool)),
    }

    def run(self):
        self.cond = self.cond[1]
        if self.cond:
            self.move_before()
        self.destroy(children=self.cond)
