# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List
from component import Component
from expression import Expression
from lxml import etree

class Slot(Component):
    use_data = ["slots"]

    def run(self):
        slot_l = len(self.slots)
        if slot_l > 0:
            slot: List[etree._Element] = self.slots[slot_l - 1]
            slot_cl = len(slot)
            
            if slot_cl > 0:
                cloned = [self.clone(el, add_jobs=True) for el in slot]
                self.insert_before(cloned)
                self.destroy(children=True)
            else:
                self.move_before()
                self.destroy(children=False)
        else:
            self.destroy(children=True)
