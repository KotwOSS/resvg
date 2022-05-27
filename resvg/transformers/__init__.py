# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from transform import Transform
from .attribute import *
from .components import *
from .custom import *

def register():
    """Register the default transformers"""
    Transform.register_default_transformer(AttributeTransformer)
    Transform.register_default_transformer(ComponentTransformer)
    Transform.register_default_transformer(CustomTransformer)
