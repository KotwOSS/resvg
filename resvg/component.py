# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable, Dict, List, Type, cast
from lxml import etree
from evaluator import Evaluator
import transform


class Component(ABC):
    components: Dict[str, Type[Component]] = {}
    arguments: Dict[str, (Callable[[str, str], bool], Evaluator)]
    use_before: bool = False
    use_after: bool = False
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

        (self._before if self.use_before else self._run)()
            
    @abstractmethod
    def before(self) -> bool | transform.TransformJob | None:
        """The before function will be run before the run method"""
        pass
    
    def _before(self):
        """Before job handler"""
        val = self.before()
        if val: self.append_job(val if isinstance(val, Callable) else self._run)
        elif self.use_after: self.append_job(self._after)
        self._complete_jobs()
    
    @abstractmethod
    def run(self) -> bool | transform.TransformJob | None:
        """The run method will be ran as long as it returns True"""
        pass
    
    def _run(self):
        """Run job handler"""
        val = self.run()
        if val: self.append_job(val if isinstance(val, Callable) else self._run)
        elif self.use_after: self.append_job(self._after)
        self._complete_jobs()
    
    @abstractmethod
    def after(self) -> bool | transform.TransformJob | None:
        """The before function will be run after the run method"""
        pass
    
    def _after(self):
        """After job handler"""
        self.after()
        self._complete_jobs()

    def _complete_jobs(self):
        """Append the temporary job queue to the actual job queue. Only call at the end of the job"""
        self.jobs.reverse()
        for job in self.jobs:
            self.transformer.add_job(job)
        self.jobs = []
        
    def append_job(self, job: Callable | etree._Element, complete: bool = False):
        """Appends a job"""
        self.jobs.append(job)
        if complete: self._complete_jobs()

    def clone(self, el: etree._Element, add_job: bool = True):
        """Clones an element"""
        clone = deepcopy(el)
        if add_job: self.append_job(clone)
        return clone

    def clone_before(self, add_job: bool = True):
        """Clone children and move them before the component"""
        for child in self.el.getchildren():
            self.el.addprevious(self.clone(child, add_job=add_job))

    def destroy(self):
        """Destroy the component node"""
        for c in self.el.iter():
            if c in self.transformer.queue:
                self.transformer.queue.remove(c)
        return self.el.getparent().remove(self.el)