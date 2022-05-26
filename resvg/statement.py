# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Dict
from settings import Settings
import logging, re


class SafeStatement:
    import_regex = re.compile(r"import\s+.+")

    def __init__(self, statement: str, locals: Dict[str, Any]):
        self.statement = statement.strip()
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
