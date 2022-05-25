import math, re, random
from typing import Any
from components.settings import Settings

from components.logging import Logger
from components.statement import RawStatement


class MultiExpression:
    def __init__(self, *types) -> None:
        self.types = types

    def parse(self, exp: str, transformer):
        exps = exp.split(";")

        if len(self.types) == len(exps):
            for i in range(0, len(exps)):
                exps[i] = (
                    RawExpression(self.types[i]).parse(exps[i], transformer).eval()
                )
        else:
            Logger.logger.exit_fatal(
                f"Invalid number of arguments for multi expression! Expected {len(self.types)} but got {len(exps)}!"
            )

        return exps


class Expression:
    def __init__(self, type) -> None:
        self.type = type

    def parse(self, exp: str, transformer):
        return RawExpression(self.type).parse(exp, transformer).eval()


class RawExpression:
    def __init__(self, type) -> None:
        self.type = type

    def parse(self, exp: str, transformer):
        self.exp = exp.strip()
        self.transformer = transformer
        return self

    def eval(self) -> Any:
        if not Settings.trust_exp:
            Logger.logger.exit_fatal(
                "Expression trust mode not enabled but code contains expressions! Perhaps you might wanna add the §o--trust-exp§R switch to your command line?"
            )

        try:
            val = eval(
                RawStatement.transform(self.exp),
                RawStatement.globals,
                self.transformer.vars,
            )
            if self.type:
                if self.type == Any or isinstance(val, self.type):
                    return val
                elif self.type == float and isinstance(val, int):
                    return float(val)
                else:
                    Logger.logger.exit_fatal(
                        f"Mismatched expression result! Expected type §o'{self.type}'§R!"
                    )
            else:
                Logger.logger.exit_fatal(
                    f"Expression instance doesn't have enough type arguments!"
                )
        except Exception as e:
            Logger.logger.exit_fatal(
                f"Error while evaluating expression §o'{self.exp}'§R: {e}"
            )


class Raw:
    def __init__(self, type) -> None:
        self.type = type

    def parse(self, val: str, transformer) -> Any:
        try:
            if self.type == str:
                return val
            elif self.type == int:
                return int(val)
            elif self.type == float:
                return float(val)
            else:
                Logger.logger.exit_fatal(f"Unknown raw type §o'{self.type}'§R!")
        except Exception as e:
            Logger.logger.exit_fatal(
                f"Error while parsing value §o'{val}' to raw type {self.type}§R: {e}"
            )
