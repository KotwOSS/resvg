# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from .loops import *
from .run import *
from .conditions import *
from .lib import *
from .comp import *
from .slot import *
from .fragment import *
from .include import *

def register():
    """Register the components"""
    Component.define_ns("repeat", Repeat)
    Component.define_ns("while", While)
    Component.define_ns("run", Run)
    Component.define_ns("if", If)
    Component.define_ns("lib", Lib)
    Component.define_ns("comp", Comp)
    Component.define_ns("slot", Slot)
    Component.define_ns("fragment", Fragment)
    Component.define_ns("include", Include)
