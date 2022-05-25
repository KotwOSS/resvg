# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
import transform

T = TypeVar("T")


class Evaluator(ABC, Generic[T]):
    @abstractmethod
    def parse(self, transformer: transform.Transformer, txt: str) -> T:
        pass
