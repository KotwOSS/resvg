# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from transform import Data

def register():
    """Register the default data"""
    Data.default("libraries", {})
    Data.default("slots", [])
    Data.default("paths", [])