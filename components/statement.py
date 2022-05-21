import math, random, re
from components.settings import Settings

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
        if not Settings.trust_stmt:
            Logger.logger.exit_fatal(
                "Statement trust mode not enabled but code contains statements! Perhaps you might wanna add the §o--trust-stmt§R switch to your command line?"
            )

        if self.import_regex.search(self.stmt):
            Logger.logger.exit_fatal(f"Run component may not contain imports!")
        else:
            exec(self.stmt, self.exec_globals, self.transformer.vars)
