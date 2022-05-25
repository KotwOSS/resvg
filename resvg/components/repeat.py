# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, Callable, Dict, Tuple
from component import Component
from evaluator import Evaluator
from expression import ExpressionEvaluator
from settings import Settings


class Repeat(Component):
    arguments: Dict[str, Tuple[Callable[[str, str], bool], Evaluator[Any]]] = {
        "var": (lambda an, av: True, ExpressionEvaluator(int)),
    }

    def setup(self):
        self.num = 0
        self.count = self.var[1]
        self.var = self.var[0]

        return self.count > self.num

    def run(self):
        self.clone_before()

        self.transformer.set_var(self.var, self.num)

        self.num += 1
        if self.count > self.num:
            self.run_job(self.run)
        else:
            self._complete_jobs()
            self.el.getparent().remove(self.el)


Component.define(Settings.resvg_namespace + "repeat", Repeat)
