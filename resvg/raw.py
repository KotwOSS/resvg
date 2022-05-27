# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from expression import SafeExpression
from statement import SafeStatement
from typing import Type, TypeVar
from evaluator import Evaluator
import transform

T = TypeVar("T")


class Raw(Evaluator[T]):
    def __init__(self, expected: Type[T], *args):
        self.expected = expected
        self.args = args

    def parse(self, transformer: transform.Transform, txt: str) -> T:
        if self.expected == SafeExpression:
            return SafeExpression(txt, transformer.vars, self.args[0])
        elif self.expected == SafeStatement:
            return SafeStatement(txt, transformer.vars)
        elif self.expected == str:
            return txt
        elif self.expected == int:
            return int(txt)
        elif self.expected == float:
            return float(txt)
        elif self.expected == bool:
            return bool(txt)
