# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Dict, Type, TypeVar
from evaluator import Evaluator
import logging, transform
from settings import Settings

T = TypeVar("T")
class ExpressionEvaluator(Evaluator[T]):
    def __init__(self, expected: Type[T]):
        self.expected = expected

    def parse(self, transformer: transform.Transformer, txt: str) -> T:
        return SafeExpression(txt, transformer.vars, self.expected).eval()


class SafeExpression:
    def __init__(self, expression: str, locals: Dict[str, Any], expected: Type[T]):
        self.expression = expression
        self.locals = locals
        self.expected = expected

    def eval(self) -> T:
        try:
            if Settings.trust_exp:
                result = eval(self.expression, Settings.exp_globals, self.locals)

                if self.expected == Any or isinstance(result, self.expected):
                    return result
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
