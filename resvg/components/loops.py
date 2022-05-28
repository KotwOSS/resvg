# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Tuple
from component import Component
from evaluator import Expression, SafeExpression, Raw
from ranges import xrange, brange


class Repeat(Component):
    use_before = True
    use_after = True
    arguments = {
        "var": (lambda an, av: True, Expression(int | range | xrange | brange), True),
    }

    start: float
    stop: float
    step: float
    num: float
    direction: bool

    var: Tuple[str, int | range | xrange] | str

    def should_run(self):
        return self.num < self.stop if self.direction else self.num > self.stop

    def before(self):
        (self.var, varv) = self.var
        if isinstance(varv, range | xrange | brange):
            self.start = varv.start
            self.stop = varv.stop
            self.step = varv.step
        else:
            self.start = 0
            self.stop = varv
            self.step = 1

        self.num = self.start
        self.direction = self.step > 0

        self.remove_child_jobs()

        return self.should_run()

    def run(self):
        self.clone_before()

        self.transform.set_var(self.var, self.num)

        self.num += self.step

        return self.should_run()

    def after(self):
        self.destroy()


class While(Component):
    use_after = True
    arguments = {
        "cond": (lambda an, av: an == "cond", Raw(SafeExpression, bool), True),
    }

    cond: Tuple[str, SafeExpression]

    def run(self):
        if self.cond[1].eval():
            self.clone_before()

            return True
        else:
            return False

    def after(self):
        self.destroy()
