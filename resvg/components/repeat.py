# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Tuple
from component import Component
from expression import Expression
from xrange import xrange


class Repeat(Component):
    use_before = True
    use_after = True
    arguments = {
        "var": (lambda an, av: True, Expression(int | range | xrange)),
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
        if isinstance(varv, range) or isinstance(varv, xrange):
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
