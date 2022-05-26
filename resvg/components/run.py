# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from statement import SafeStatement
from settings import Settings


class Run(Component):
    use_after = True

    def run(self):
        SafeStatement(self.el.text, self.transformer.vars).exec()

    def after(self):
        self.destroy()


Component.define_ns("run", Run)
