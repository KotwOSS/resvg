# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component
from statement import SafeStatement


class Run(Component):
    def run(self):
        SafeStatement(self.el.text, self.transformer.vars).exec()
        self.destroy()