# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Callable, Dict, List, Type, TypeVar
from lxml import etree
from domlib import ProxiedDomSettings
from transformer import Transformer
import logging

T = TypeVar("T")


class Data:
    """Datacontainer which is able to store and modify data"""

    defaults: Dict[str, Any] = {}

    def default(key: str, value: Any):
        """Set default data"""
        Data.defaults[key] = value

    def __init__(self) -> None:
        self._data = Data.defaults.copy()

    def set(self, key: str, value: Any):
        """Set the value of key"""
        self._data[key] = value

    def has(self, key: str) -> bool:
        """Return if key in data"""
        return key in self._data

    def get(self, key: str, default: T = None) -> T:
        """Get the value of key"""
        return self._data[key] if key in self._data else default

    def get_or_set(self, key: str, value: T) -> T:
        """Get or set the value of key"""
        if key in self._data:
            return self._data[key]
        else:
            self._data[key] = value
            return value

    def remove(self, key: str) -> bool:
        """Remove the key from data"""
        del self._data[key]


class Transform:
    default_transformers: List[Type[Transformer]] = []

    @staticmethod
    def register_default_transformer(transformer: Transformer):
        """Register a default transformer"""
        Transform.default_transformers.append(transformer)

    transformers: List[Transformer]
    root: etree._Element
    vars: Dict[str, Any]
    var_scopes: List[Dict[str, Any]]
    queue: List[etree._Element | Callable]
    active: etree._Element
    data: Data

    def __init__(self, root: etree._Element):
        self.root = root
        self.queue = list(root.iter())
        self.queue.reverse()
        self.vars = {}
        self.var_scopes = [self.vars]
        self.data = Data()
        self.transformers = []

        ProxiedDomSettings.transformer = self

    def register_default_transformers(self):
        """Register the default transformers"""
        for transformer in Transform.default_transformers:
            self.register_transformer(transformer(self))

    def register_transformer(self, transformer: Transformer):
        """Register an element transformer"""
        self.transformers.append(transformer)

    def has_next(self):
        """Check if there are more elements to parse"""
        return len(self.queue) > 0

    def next(self):
        """Parse the next item of the queue"""
        item = self.queue.pop()
        if isinstance(item, etree._Comment):
            logging.debug("Skipping comment '§g%s§R'", item.text.strip())
        elif isinstance(item, etree._Element):
            logging.debug("transforming §b%s§R", item.tag)
            self.parse_element(item)
        elif isinstance(item, Callable):
            logging.debug("running §y%s§R", item.__name__)
            item()

    def parse_element(self, el: etree._Element):
        """Parse an element from the queue"""
        self.active = el
        for transformer in self.transformers:
            if transformer(el):
                return
    
    def insert_scope(self, scope: Dict[str, Any]):
        """Insert a scope"""
        self.var_scopes.append(scope)
        self.vars = scope
    
    def append_scope(self, clone: bool = True):
        """Append a new scope"""
        scope = self.vars.copy() if clone else {}
        self.var_scopes.append(scope)
        self.vars = scope

    def pop_scope(self) -> Dict[str, Any]:
        """Pop a scope"""
        res = self.var_scopes.pop()
        self.vars = self.var_scopes[len(self.var_scopes) - 1]
        return res

    def set_var(self, name: str, value: Any):
        """Set a variable"""
        logging.debug("set §o%s§R to §o%s§R", name, value)
        self.vars[name] = value

    def add_job(self, job: Callable):
        """Add a job to the queue"""
        if isinstance(job, Callable):
            logging.debug("queue: run §o%s§R", job.__name__)
        else:
            logging.debug("queue: transform §o%s§R", job.tag)
        self.queue.append(job)

    def insert_job(self, job: Callable, index: int):
        """Insert a job into the queue"""
        if isinstance(job, Callable):
            logging.debug("queue: run §o%s§R at index §o%s§R", job.__name__, index)
        else:
            logging.debug("queue: transform §o%s§R at index §o%s§R", job.tag, index)
        self.queue.insert(index, job)

    def transform(self):
        """Transform the tree"""
        while self.has_next():
            self.next()
