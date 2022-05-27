# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List, Tuple
from component import Component
from raw import Raw
from expression import MultiExpression
from settings import Settings

from .operations import *


class Path(Component):
    use_last = True
    use_data = ["paths"]
    arguments = {
        "translate": (
            lambda an, av: an == Settings.resvg_namespace + "translate",
            MultiExpression(float, float),
            False,
        ),
        "args*": (lambda an, av: True, Raw(str), True),
    }

    args: List[Tuple[str, str]]
    paths: List[List[PathOperation]]

    def run(self):
        path: List[PathOperation] = []
        self.paths.append(path)
        self.data.set("path", path)

    def last(self):
        # TODO: Rotate the paths list
        path = self.paths.pop()

        if hasattr(self, "translate"):
            x, y = self.translate[1]
            [p.translate(x, y) for p in path]
            del self.el.attrib[self.translate[0]]

        pathl = len(self.paths)
        if pathl > 0:
            path_p = self.paths[pathl - 1]
            self.data.set("path", path_p)
            path_p.extend(path)

            self.destroy(children=False)
        else:
            self.data.remove("path")

            path_d = " ".join([p.tostring() for p in path])

            self.el.tag = Settings.svg_namespace + "path"
            self.el.attrib["d"] = path_d
