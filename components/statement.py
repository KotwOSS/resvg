import math, random, re
from components.settings import Settings

from components.logging import Logger


class RawStatement:
    greater_regex = re.compile("\sgreater\s")
    smaller_regex = re.compile("\ssmaller\s")
    smequal_regex = re.compile("\ssmequal\s")
    grequal_regex = re.compile("\sgrequal\s")

    globals = {
        "import": None,
        "__import__": None,
        "open": None,
        "exec": None,
        "eval": None,
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
    }

    import_regex = re.compile(r"import\s+.+")

    def transform(code: str):
        code = RawStatement.greater_regex.sub(">", code)
        code = RawStatement.smaller_regex.sub("<", code)
        code = RawStatement.grequal_regex.sub(">=", code)
        code = RawStatement.smequal_regex.sub("<=", code)
        return code

    def parse(self, stmt: str, transformer):
        self.stmt = stmt.strip()
        self.transformer = transformer
        return self

    def exec(self):
        if not Settings.trust_stmt:
            Logger.logger.exit_fatal(
                "Statement trust mode not enabled but code contains statements! Perhaps you might wanna add the §o--trust-stmt§R switch to your command line?"
            )

        if self.import_regex.search(self.stmt):
            Logger.logger.exit_fatal(f"Run component may not contain imports!")
        else:
            exec(RawStatement.transform(self.stmt), self.globals, self.transformer.vars)
