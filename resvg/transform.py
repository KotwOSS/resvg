# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from component import Component
from array import array
from typing import Any, Callable, Dict
from lxml import etree
from expression import SafeExpression
from settings import Settings
import re, reutil, logging


class Transformer:
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")

    root: etree._Element
    vars: Dict[str, Any]
    queue: array[etree._Element | Callable]

    def __init__(self, root: etree._Element):
        self.root = root
        self.queue = list(root.getiterator())
        self.vars = {}

    def has_next(self):
        """Check if there are more elements to parse"""
        return len(self.queue) > 0

    def next(self):
        """Parse the next item of the queue"""
        item = self.queue.pop(0)
        if isinstance(item, etree._Element):
            self.parse_element(item)
        elif isinstance(item, Callable):
            item()

    def parse_element(self, el: etree._Element):
        """Parse an element from the queue"""
        for attr in el.attrib.items():
            attrname = attr[0]
            attrval = attr[1]

            attrval = reutil.multi_replace(
                attrval,
                self.expression_regex,
                lambda exp: reutil.stringify(
                    SafeExpression(exp.group(1), self.vars, Any).eval()
                ),
            )

            if attrname.startswith(Settings.resvg_namespace):
                name = attrname[len(Settings.resvg_namespace) :]
                el.attrib[name] = reutil.stringify(
                    SafeExpression(attrval, self.vars, Any).eval()
                )
                del el.attrib[attrname]
            else:
                el.attrib[attrname] = attrval

        if el.tag in Component.components:
            comp = Component.components[el.tag](self, el)
            comp.parse()

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
        self.queue.insert(0, job)

    def transform(self):
        """Transform the tree"""
        while self.has_next():
            self.next()
