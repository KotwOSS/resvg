# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List
from component import Component
from expression import Expression

from .operations import *


class MoveTo(Component):
    use_data = ["path"]

    path: List[PathOperation]

    arguments = {
        "x": (lambda an, av: an == "x", Expression(float), True),
        "y": (lambda an, av: an == "y", Expression(float), True),
    }

    def run(self):
        self.path.append(MoveToOperation(self.x[1], self.y[1]))
        self.destroy()
