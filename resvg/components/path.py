# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List, Tuple
from component import Component
from evaluator import MultiExpression, Raw, Expression
from settings import Settings
from abc import ABC, abstractmethod
import reutil

# ANCHOR: PathOperation
class PathOperation(ABC):
    @abstractmethod
    def tostring(self) -> str:
        pass

    @abstractmethod
    def translate(self, x: float, y: float) -> None:
        pass

    def __format__(self, __format_spec: str) -> str:
        return self.tostring()

# ANCHOR: MoveToOperation
class MoveToOperation(PathOperation):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tostring(self) -> str:
        return "M" + reutil.stringify(self.x) + " " + reutil.stringify(self.y)

    def translate(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

# ANCHOR: LineToOperation
class LineToOperation(PathOperation):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tostring(self) -> str:
        return "L" + reutil.stringify(self.x) + " " + reutil.stringify(self.y)

    def translate(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

# ANCHOR: CloseOperation
class CloseOperation(PathOperation):
    def tostring(self) -> str:
        return "Z"

    def translate(self, x: float, y: float) -> None:
        pass

# ANCHOR: path
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

# ANCHOR: LineTo
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

# ANCHOR: Line
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

# ANCHOR: MoveTo
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

# ANCHOR: Close
class Close(Component):
    use_data = ["path"]

    path: List[PathOperation]

    def run(self):
        self.path.append(CloseOperation())
        self.destroy()
