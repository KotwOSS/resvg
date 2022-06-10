# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any, Dict, List
from component import Component
from evaluator import Expression
from lxml import etree


class Slot(Component):
    use_data = ["slots"]
    use_last = True
    
    scope: Dict[str, Any]

    def run(self):
        slot_l = len(self.slots)
        if slot_l > 0:
            slot: List[etree._Element] = self.slots[slot_l - 1]
            slot_cl = len(slot)
            
            self.scope = self.transform.pop_scope()
            
            copy = self.scope.copy()
            copy.update(self.transform.vars)
            self.transform.insert_scope(copy)

            if slot_cl > 0:
                cloned = [self.clone(el, add_jobs=True) for el in slot]
                self.insert_before(cloned)
                self.destroy(children=True)
            else:
                self.move_before()
                self.destroy(children=False)
        else:
            raise RuntimeError("Slot component can only be in a §ocomp§R component")

    def last(self):
        self.transform.pop_scope()
        self.transform.insert_scope(self.scope)