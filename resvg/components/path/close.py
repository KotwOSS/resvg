# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import List
from component import Component

from .operations import *

class Close(Component):
    use_data = ["path"]
    
    path: List[PathOperation]
    
    def run(self):
        self.path.append(CloseOperation())
        self.destroy()
