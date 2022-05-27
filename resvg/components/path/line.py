# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List
from components import Component
from expression import Expression

from .operations import *


class LineTo(Component):
    use_data = ["path"]

    path: List[PathOperation]

    arguments = {
        "x": (lambda an, av: an == "x", Expression(float), True),
        "y": (lambda an, av: an == "y", Expression(float), True),
    }

    def run(self):
        self.path.append(LineToOperation(self.x[1], self.y[1]))
        self.destroy()


class Line(Component):
    use_data = ["path"]

    path: List[PathOperation]

    arguments = {
        "fx": (lambda an, av: an == "fx", Expression(float), True),
        "fy": (lambda an, av: an == "fy", Expression(float), True),
        "tx": (lambda an, av: an == "tx", Expression(float), True),
        "ty": (lambda an, av: an == "ty", Expression(float), True),
    }

    def run(self):
        self.path.append(
            (LineToOperation if self.path else MoveToOperation)(self.fx[1], self.fy[1])
        )
        self.path.append(LineToOperation(self.tx[1], self.ty[1]))
        self.destroy()
