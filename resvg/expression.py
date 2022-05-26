# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Dict, Type, TypeVar
from evaluator import Evaluator
import logging, math, random, transform, numpy


T = TypeVar("T")


class ExpressionEvaluator(Evaluator[T]):
    def __init__(self, expected: Type[T]):
        self.expected = expected

    def parse(self, transformer: transform.Transformer, txt: str) -> T:
        return SafeExpression(txt, transformer.vars, self.expected).eval()


class xrange:
    start: float
    stop: float 
    step: float
    
    def __init__(self, *args) -> None:
        argslen = len(args)
        self.start = args[0] if argslen > 1 else 0
        self.stop = args[1] if argslen > 1 else \
            args[0] if argslen == 1 else 0
        self.step = args[2] if argslen > 2 else 1
    

class SafeExpression:
    globals = {
        "__import__": None,
        "__builtins__": None,
        "open": None,
        "eval": None,
        "exec": None,
        "math": math,
        "random": random,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "atan2": math.atan2,
        "sqrt": math.sqrt,
        "ceil": math.ceil,
        "floor": math.floor,
        "pow": math.pow,
        "abs": math.fabs,
        "log": math.log,
        "log10": math.log10,
        "range": range,
        "xrange": xrange,
        "numpy": numpy,
    }

    def __init__(self, expression: str, locals: Dict[str, Any], expected: Type[T]):
        self.expression = expression
        self.locals = locals
        self.expected = expected

    def eval(self) -> T:
        try:
            result = eval(self.expression, SafeExpression.globals, self.locals)

            if self.expected == Any or isinstance(result, self.expected):
                return result
            else:
                raise TypeError(
                    "Expression did not return type '%s'" % self.expected.__name__
                )
        except Exception as e:
            logging.critical(
                "Error while evaluating expression §o%s§R: %s", self.expression, e
            )
            raise e
