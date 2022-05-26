# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from typing import Any, Callable, Dict, List, Type
from lxml import etree
from domlib import ProxiedDomSettings
from transformer import Transformer
import logging


class Transform:
    default_transformers: List[Type[Transformer]] = []

    @staticmethod
    def register_default_transformer(transformer: Transformer):
        """Register a default transformer"""
        Transform.default_transformers.append(transformer)

    transformers: List[Transformer]
    root: etree._Element
    vars: Dict[str, Any]
    queue: List[etree._Element | Callable]
    active: etree._Element

    def __init__(self, root: etree._Element):
        self.root = root
        self.queue = list(root.iter())
        self.queue.reverse()
        self.vars = {}
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
        if isinstance(item, etree._Element):
            self.parse_element(item)
        elif isinstance(item, Callable):
            item()

    def parse_element(self, el: etree._Element):
        """Parse an element from the queue"""
        self.active = el
        for transformer in self.transformers:
            if transformer(el):
                return

    def set_var(self, name: str, value: Any):
        """Set a variable"""
        logging.debug("Setting §o%s§R to §o%s§R", name, value)
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
