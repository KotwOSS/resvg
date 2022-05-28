# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Dict, List, Type
from settings import Settings
import transform, logging, transform, re

T = TypeVar("T")

# ANCHOR: Evaluator
class Evaluator(ABC, Generic[T]):
    @abstractmethod
    def parse(self, transformer: transform.Transform, txt: str) -> T:
        pass

# ANCHOR: MultiExpression
class MultiExpression(Evaluator[Any]):
    def __init__(self, *expected: List[Type[Any]]):
        self.expected = expected

    def parse(self, transformer: transform.Transform, txt: str) -> Any:
        parts = txt.split(";")
        if len(parts) == len(self.expected):
            for i, p in enumerate(parts):
                parts[i] = SafeExpression(p, transformer.vars, self.expected[i]).eval()
        return parts

# ANCHOR: Expression
class Expression(Evaluator[T]):
    def __init__(self, expected: Type[T]):
        self.expected = expected

    def parse(self, transformer: transform.Transform, txt: str) -> T:
        return SafeExpression(txt, transformer.vars, self.expected).eval()

# ANCHOR: SafeExpression
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

# ANCHOR: SafeStatement
class SafeStatement:
    import_regex = re.compile(r"import\s+.+")

    def __init__(self, statement: str, locals: Dict[str, Any]):
        self.statement = Settings.proccess_operation(statement)
        self.locals = locals

    def exec(self):
        try:
            if Settings.trust_stmt:
                if self.import_regex.match(self.statement) == None:
                    exec(self.statement, Settings.stmt_globals, self.locals)
                else:
                    raise RuntimeError("Import statements are not allowed")
            else:
                raise RuntimeError(
                    "Code contains statements but §o--trust-stmt§R is disabled!"
                )
        except Exception as e:
            logging.critical(
                "Error while executing statement '''\n§o%s§R\n''': %s",
                self.statement,
                e,
            )
            raise e

# ANCHOR: Raw
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
