# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from .repeat import *
from .run import *
from .conditions import *
from .lib import *


def register():
    """Register the components"""
    Component.define_ns("lib", Lib)
    Component.define_ns("run", Run)
    Component.define_ns("repeat", Repeat)
