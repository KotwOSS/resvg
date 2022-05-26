# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, Callable, Dict, Tuple
from component import Component
from evaluator import Evaluator
from expression import ExpressionEvaluator, xrange
from settings import Settings


class Repeat(Component):
    use_before: bool = True
    use_after: bool = True
    arguments: Dict[str, Tuple[Callable[[str, str], bool], Evaluator[Any]]] = {
        "var": (lambda an, av: True, ExpressionEvaluator(int | range | xrange)),
    }
    
    start: float
    stop: float
    step: float
    num: float
    direction: bool
    
    var: Tuple[str, int | range | xrange] | str
    
    def should_run(self):
        return self.num < self.stop if self.direction \
            else self.num > self.stop

    def before(self):
        (self.var, varv) = self.var
        if isinstance(varv, range) \
        or isinstance(varv, xrange):
            self.start = varv.start
            self.stop = varv.stop
            self.step = varv.step
        else:
            self.start = 0
            self.stop = varv
            self.step = 1
        
        self.num = self.start
        self.direction = self.step > 0
        
        return self.should_run()

    def run(self):
        self.clone_before()

        self.transformer.set_var(self.var, self.num)

        self.num += self.step
        
        return self.should_run()
    
    def after(self): self.destroy()


Component.define(Settings.resvg_namespace + "repeat", Repeat)
