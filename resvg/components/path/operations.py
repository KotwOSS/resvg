# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from abc import ABC, abstractmethod
import reutil

class PathOperation(ABC):
    @abstractmethod
    def tostring(self) -> str:
        pass
    
    @abstractmethod
    def translate(self, x: float, y: float) -> None:
        pass
    
    def __format__(self, __format_spec: str) -> str:
        return self.tostring()
    
    def __repr__(self):
        return self.tostring()

class MoveToOperation(PathOperation):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def tostring(self) -> str:
        return "M" + reutil.stringify(self.x) \
             + " " + reutil.stringify(self.y)
    
    def translate(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

class LineToOperation(PathOperation):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def tostring(self) -> str:
        return "L" + reutil.stringify(self.x) \
             + " " + reutil.stringify(self.y)
    
    def translate(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

class CloseOperation(PathOperation):
    def tostring(self) -> str:
        return "Z"
    
    def translate(self, x: float, y: float) -> None:
        pass