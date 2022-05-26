# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import logging
import math, random, numpy, reutil, domlib
from typing import Any, Callable
from xrange import xrange

class NotAllowed(Callable):
    def __init__(self, name: str):
        self.name = name
        
    def __call__(self, *args):
        raise RuntimeError(f"The function '§o{self.name}§R' was disabled for security reasons!")
        
class Settings:
    # Generic information
    version = "0.0.0alpha3"
    authors = ["KotwOSS"]
    license = "MIT"
    year = 2022

    resvg_namespace: str = "{http://oss.kotw.dev/resvg}"

    no_color: bool
    comments: bool
    min_time: float
    pretty: bool
    compile: bool
    watch: str
    trust_exp: bool
    trust_stmt: bool
    silent: bool
    hide_logo: bool
    input: str
    output: str
    ext = []
    log: str
    level: int
    
    transformer: Any

    globals = {
        "__import__": NotAllowed("__import__"),
        "__builtins__": NotAllowed("__builtins__"),
        "open": NotAllowed("open"),
        "eval": NotAllowed("eval"),
        "exec": NotAllowed("exec"),
        "math": math,
        "random": random,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "atan2": math.atan2,
        "sqrt": math.sqrt,
        "ceil": math.ceil,
        "floor": math.floor,
        "pow": math.pow,
        "abs": math.fabs,
        "log": math.log,
        "log10": math.log10,
        "range": range,
        "xrange": xrange,
        "numpy": numpy,
        "print": print,
        "logging": logging,
    }
    
    exp_globals = reutil.concat_dict(globals.copy(), {
        
    })
    
    stmt_globals = reutil.concat_dict(globals.copy(), {
        "dom": domlib.ProxiedDom
    })