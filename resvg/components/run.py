# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

import logging
from component import Component
from evaluator import SafeStatement


class Run(Component):
    def run(self):
        logging.debug("run codeblock")
        
        SafeStatement(self.el.text, self.transform.vars).exec()
        self.destroy()
