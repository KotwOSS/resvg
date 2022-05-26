# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from transform import Transform
from .attribute import *
from .component import *


def register():
    """Register the default transformers"""
    Transform.register_default_transformer(AttributeTransformer)
    Transform.register_default_transformer(ComponentTransformer)
