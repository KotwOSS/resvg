# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Dict, List, Type, TypeVar
from evaluator import Evaluator
from settings import Settings
import logging, transform, re

class MultiExpression(Evaluator[Any]):
    def __init__(self, *expected: List[Type[Any]]):
        self.expected = expected

    def parse(self, transformer: transform.Transform, txt: str) -> Any:
        parts = txt.split(";")
        if len(parts) == len(self.expected):
            for i, p in enumerate(parts):
                parts[i] = SafeExpression(p, transformer.vars, self.expected[i]).eval()
        return parts
    
T = TypeVar("T")
class Expression(Evaluator[T]):
    def __init__(self, expected: Type[T]):
        self.expected = expected

    def parse(self, transformer: transform.Transform, txt: str) -> T:
        return SafeExpression(txt, transformer.vars, self.expected).eval()


class SafeExpression:    
    def __init__(self, expression: str, locals: Dict[str, Any], expected: Type[T]):
        self.expression = Settings.proccess_operation(expression)
        self.locals = locals
        self.expected = expected

    def eval(self) -> T:
        try:
            if Settings.trust_exp:
                result = eval(self.expression, Settings.exp_globals, self.locals)

                if self.expected == Any or isinstance(result, self.expected):
                    return result
                elif self.expected == float and isinstance(result, int):
                    return float(result)
                else:
                    raise TypeError(
                        "Expression did not return type '%s'" % self.expected.__name__
                    )
            else:
                raise RuntimeError(
                    "Code contains expressions but §o--trust-exp§R is disabled!"
                )
        except Exception as e:
            logging.critical(
                "Error while evaluating expression '§o%s§R': %s", self.expression, e
            )
            raise e
