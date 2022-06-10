# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, Dict, List
from component import Component
from evaluator import Expression, Raw
from lxml import etree

from settings import Settings


class Default(Component):
    arguments = {
        "any_re*": (lambda an, av: an.startswith(Settings.resvg_namespace), Expression(Any), True),
        "any*": (lambda an, av: True, Raw(str), True)
    }
    
    def run(self):
        resvg_ns_l = len(Settings.resvg_namespace)
        for (an, av) in self.any_re:
            an = an[resvg_ns_l:].replace("-", "_")
            if not an in self.transform.vars:
                self.transform.set_var(an, av)
        
        for (an, av) in self.any:
            an = an.replace("-", "_")
            if not an in self.transform.vars:
                self.transform.set_var(an, av)
                
        self.destroy()