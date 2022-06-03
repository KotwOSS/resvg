# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

import logging
from typing import List, Tuple
from component import Component
from evaluator import MultiExpression, Raw, Expression
from settings import Settings
import svgelements as se

# ANCHOR: path
class Path(Component):
    use_last = True
    use_data = ["paths"]
    arguments = {
        "transformation": (
            lambda an, av: an == Settings.resvg_namespace + "transform",
            Raw(str),
            False,
        ),
        "args*": (lambda an, av: True, Raw(str), True),
    }

    args: List[Tuple[str, str]]
    paths: List[se.Path]

    def run(self):
        # By default the current_point is 0, 0 not None
        self.data.get_or_set("current_point", se.Point(0, 0))
       
        path = se.Path()
       
        if hasattr(self, "transformation"):
            var, transformation = self.transformation
            logging.debug("adding transformation: §o%s§R", transformation)
            path *= se.Matrix().parse(transformation)
            
            del self.el.attrib[var]
        
        self.paths.append(path)
        self.data.set("path", path)

    def last(self):
        path = self.paths.pop()
        
        path.reify()

        pathl = len(self.paths)
        if pathl > 0:
            path_p = self.paths[-1]
            self.data.set("path", path_p)
            path_p.extend(path)

            self.destroy(children=False)
        else:
            self.data.remove("path")

            self.el.tag = Settings.svg_namespace + "path"
            self.el.attrib["d"] = path.d()
            
# ANCHOR: LineTo
class LineTo(Component):
    use_data = ["path"]

    path: se.Path

    arguments = {
        "point": (lambda an, av: an in ["p", "point"], MultiExpression(float, float), False),
        "x": (lambda an, av: an == "x", Expression(float), False),
        "y": (lambda an, av: an == "y", Expression(float), False),
    }

    def run(self):
        point = None
        if hasattr(self, "point"):
            point = self.point[1]
        elif hasattr(self, "x") and hasattr(self, "y"):
            point = self.x[1], self.y[1]

        self.path.line(point)
        self.destroy()

# ANCHOR: Line
class Line(Component):
    use_data = ["path"]

    path: se.Path

    arguments = {
        "point": (lambda an, av: an in ["p", "point"], MultiExpression(float, float, float, float), False),
        "from_p": (lambda an, av: an in ["f", "from", "from-p", "start"], MultiExpression(float, float), False),
        "from_x": (lambda an, av: an in ["fx", "from-x"], Expression(float), False),
        "from_y": (lambda an, av: an in ["fy", "from-y"], Expression(float), False),
        "to_p": (lambda an, av: an in ["t", "to", "to-p", "end"], MultiExpression(float, float), False),
        "to_x": (lambda an, av: an in ["tx", "to-x"], Expression(float), False),
        "to_y": (lambda an, av: an in ["ty", "to-y"], Expression(float), False),
    }

    def run(self):
        start, end = None, None
        if hasattr(self, "from_p"):
            start = self.from_p[1]
        elif hasattr(self, "from_x") and hasattr(self, "from_y"):
            start = self.from_x[1], self.from_y[1]
        
        if hasattr(self, "to_p"):
            end = self.to_p[1]
        elif hasattr(self, "to_x") and hasattr(self, "to_y"):
            end = self.to_x[1], self.to_y[1]
        
        if hasattr(self, "point"):
            start = self.point[1][:2]
            end = self.point[1][2:]
        
        self.path.move(start, end)
        self.destroy()

# ANCHOR: MoveTo
class MoveTo(Component):
    use_data = ["path"]

    path: se.Path

    arguments = {
        "point": (lambda an, av: an in ["p", "point"], MultiExpression(float, float), False),
        "x": (lambda an, av: an == "x", Expression(float), False),
        "y": (lambda an, av: an == "y", Expression(float), False),
    }

    def run(self):
        point = None
        if hasattr(self, "point"):
            point = self.point[1]
        elif hasattr(self, "x") and hasattr(self, "y"):
            point = self.x[1], self.y[1]

        self.path.move(point)
        self.destroy()

# ANCHOR: Close
class Close(Component):
    use_data = ["path"]

    path: se.Path

    def run(self):
        self.path.append(se.Close())
        self.destroy()

# ANCHOR: Bezier
class Bezier(Component):
    use_data = ["path"]

    path: se.Path
    
    arguments = {
        "point": (lambda an, av: an in ["p", "point"], MultiExpression(float, float, float, float), False),
        "point1": (lambda an, av: an in ["p1", "point1"], MultiExpression(float, float), False),
        "x1": (lambda an, av: an == "x1", Expression(float), False),
        "y1": (lambda an, av: an == "y1", Expression(float), False),
        "point2": (lambda an, av: an in ["p2", "point2"], MultiExpression(float, float), False),
        "x2": (lambda an, av: an == "x2", Expression(float), False),
        "y2": (lambda an, av: an == "y2", Expression(float), False),
    }

    def run(self):
        point1, point2 = None, None
        if hasattr(self, "point1"):
            point1 = self.point1[1]
        elif hasattr(self, "x1") and hasattr(self, "y1"):
            point1 = self.x1[1], self.y1[1]
        
        if hasattr(self, "point2"):
            point2 = self.point2[1]
        elif hasattr(self, "x2") and hasattr(self, "y2"):
            point2 = self.x2[1], self.y2[1]
            
        if hasattr(self, "point"):
            point1 = self.point[1][:2]
            point2 = self.point[1][2:]
        
        self.path.quad(point1, point2)
        self.destroy()

# ANCHOR: Reverse
class Reverse(Component):
    use_data = ["path", "current_point"]

    path: se.Path
    current_point: se.Point

    def run(self):
        # Placeholder needed for reversing lonely paths
        self.path.insert(0, se.Move(self.current_point) )
        # Remove the paths
        self.path.reverse()
        # Remove placeholder
        self.path.pop(0)
        self.destroy()
