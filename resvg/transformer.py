# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from abc import ABC, abstractmethod
from lxml import etree
import transform


class Transformer(ABC):
    transform: "transform.Transform"
    data: "transform.Data"

    def __init__(self, transform: transform.Transform):
        self.transform = transform
        self.data = transform.data

    @abstractmethod
    def __call__(self, el: etree._Element) -> bool:
        pass
