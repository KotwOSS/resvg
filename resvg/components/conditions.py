# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from expression import ExpressionEvaluator

class If(Component):
    use_after = True
    arguments = {
        "cond": (lambda an, av: an == "cond", ExpressionEvaluator(bool)),
    }

    def run(self):
        if self.cond[1]:
            self.clone_before()

    def after(self):
        self.destroy()


Component.define_ns("if", If)
