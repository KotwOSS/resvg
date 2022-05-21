import math, random, re

from util.logging import Logger


class RawStatement:
    exec_globals = {
        "import": None,
        "__import__": None,
        "open": None,
        "exec": None,
        "eval": None,
        "math": math,
        "random": random,
    }

    import_regex = re.compile(r"import\s+.+")

    def __init__(self, transformer):
        self.transformer = transformer

    def parse(self, stmt: str):
        self.stmt = stmt.strip()
        return self

    def exec(self):
        if self.import_regex.search(self.stmt):
            Logger.logger.exit_fatal(f"Run component may not contain imports!")
        else:
            exec(self.stmt, self.exec_globals, self.transformer.vars)
    