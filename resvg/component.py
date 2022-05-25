# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from inspect import getattr_static
from typing import Callable, Dict, List, Type
from lxml import etree
from evaluator import Evaluator
import transform


class Component(ABC):
    components: Dict[str, Type[Component]] = {}
    arguments: Dict[str, (Callable[[str, str], bool], Evaluator)]
    transformer: "transform.Transformer"
    el: etree._Element
    jobs: List[transform.TransformJob | etree._Element]

    def __init__(self, transformer: transform.Transformer, el: etree._Element):
        self.transformer = transformer
        self.el = el
        self.jobs = []

    def define(name: str, comp: Type[Component]):
        """Define a component"""
        Component.components[name] = comp

    def parse(self):
        """Parse the component"""
        for an, av in self.el.attrib.items():
            for n, (k, v) in self.arguments.items():
                if k(an, av):
                    setattr(self, n, (an, v.parse(self.transformer, av)))
                    break

        val = self.setup()
        if val:
            self.jobs.append(val if isinstance(val, Callable) else self.run)
            self._complete_jobs()

    @abstractmethod
    def run(self) -> bool | transform.TransformJob | None:
        """The run method will be ran as long as it returns True"""
        pass

    @abstractmethod
    def setup(self) -> bool | transform.TransformJob | None:
        """The run method will be ran as long as it returns True"""
        pass

    def _complete_jobs(self):
        """Append the temporary job queue to the actual job queue. Only call at the end of the job"""
        for job in self.jobs[::-1]:
            self.transformer.add_job(job)
        self.jobs = []

    def run_job(self, job_d: Callable):
        """Runs a job"""
        self.jobs.append(job_d)
        self._complete_jobs()

    def clone_before(self):
        """Clone children before the component"""
        for child in self.el.getchildren():
            clone = deepcopy(child)
            self.el.addprevious(clone)
            self.jobs.append(clone)
