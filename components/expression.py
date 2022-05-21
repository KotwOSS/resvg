import math, re, random
from typing import Any, Generic, TypeVar
from components.settings import Settings

from util.logging import Logger

# Expression class
T = TypeVar("T")


class Expression(Generic[T]):
    greater_regex = re.compile("\sgreater\s")
    smaller_regex = re.compile("\ssmaller\s")
    expression_globals = {
        "__import__": None,
        "open": None,
        "exec": None,
        "eval": None,
        "math": math,
        "random": random,
    }

    def __init__(self, transformer) -> None:
        super().__init__()

        self.transformer = transformer

    def parse(self, exp: str) -> T:
        return (
            RawExpression[
                self.__orig_class__.__args__[0]
                if hasattr(self, "__orig_class__")
                and len(self.__orig_class__.__args__) >= 1
                else None
            ](self.transformer)
            .parse(exp)
            .eval()
        )


class RawExpression(Generic[T]):
    greater_regex = re.compile("\sgreater\s")
    smaller_regex = re.compile("\ssmaller\s")
    expression_globals = {
        "__import__": None,
        "open": None,
        "exec": None,
        "eval": None,
        "math": math,
        "random": random,
    }

    def __init__(self, transformer) -> None:
        super().__init__()

        self.transformer = transformer

    def parse(self, exp: str):
        self.exp = exp.strip()
        return self

    def eval(self) -> T:
        if not Settings.trust_exp:
            Logger.logger.exit_fatal(
                "Expression trust mode not enabled but code contains expressions! Perhaps you might wanna add the §o--trust-exp§R switch to your command line?"
            )

        self.exp = self.greater_regex.sub(">", self.exp)
        self.exp = self.smaller_regex.sub("<", self.exp)

        try:
            val = eval(self.exp, self.expression_globals, self.transformer.vars)
            if (
                hasattr(self, "__orig_class__")
                and len(self.__orig_class__.__args__) >= 1
            ):
                expected_type = self.__orig_class__.__args__[0]
                if expected_type == Any or isinstance(val, expected_type):
                    return val
                else:
                    Logger.logger.exit_fatal(
                        f"Mismatched expression result! Expected type §o'{expected_type}'§R!"
                    )
            else:
                Logger.logger.exit_fatal(
                    f"Expression instance doesn't have enough type arguments!"
                )
        except Exception as e:
            Logger.logger.exit_fatal(
                f"Error while evaluating expression §o'{self.exp}'§R: {e}"
            )


# Raw class
T = TypeVar("T")


class Raw(Generic[T]):
    def __init__(self, transformer) -> T:
        super().__init__()

        self.transformer = transformer

    def parse(self, val: str) -> T:
        try:
            expected_type = self.__orig_class__.__args__[0]
            if expected_type == str:
                return val
            elif expected_type == int:
                return int(val)
            elif expected_type == float:
                return float(val)
            else:
                Logger.logger.exit_fatal(
                    f"Unknown expected raw type §o'{expected_type}'§R!"
                )
        except Exception as e:
            Logger.logger.exit_fatal(
                f"Error while parsing value §o'{val}' to raw type {expected_type}§R: {e}"
            )
