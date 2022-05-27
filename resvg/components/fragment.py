# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from component import Component


class Fragment(Component):
    def run(self):
        self.move_before()
        self.destroy(children=False)