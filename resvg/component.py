# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

from __future__ import annotations

from more_itertools import last
from transform import Transform
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Callable, Dict, List, Type
from lxml import etree
from evaluator import Evaluator
from settings import Settings


class Component(ABC):
    components: Dict[str, Type[Component]] = {}
    arguments: Dict[str, (Callable[[str, str], bool], Evaluator)]
    use_before: bool = False
    use_after: bool = False
    use_last: bool = False
    transformer: Transform
    el: etree._Element
    jobs: List[Callable | etree._Element]

    def __init__(self, transformer: Transform, el: etree._Element):
        self.transformer = transformer
        self.el = el
        self.jobs = []

    def define(name: str, comp: Type[Component]):
        """Define a component"""
        Component.components[name] = comp

    def define_ns(name: str, comp: Type[Component]):
        """Define a component in the default resvg namespace"""
        Component.define(Settings.resvg_namespace + name, comp)

    def parse(self):
        """Parse the component"""
        for an, av in self.el.attrib.items():
            for n, (k, v) in self.arguments.items():
                if k(an, av):
                    setattr(self, n, (an, v.parse(self.transformer, av)))
                    break
        
        (self._before if self.use_before else self._run)()

    def before(self) -> bool | Callable | None:
        """The before function will be run before the run method"""
        pass

    def _before(self):
        """Before job handler"""
        val = self.before()
        if val:
            self.append_job(val if isinstance(val, Callable) else self._run)
        elif self.use_after:
            self.append_job(self._after)
        elif self.use_last:
            self.append_job_last(self._last)
        self._complete_jobs()

    @abstractmethod
    def run(self) -> bool | Callable | None:
        """The run method will be ran as long as it returns True"""
        pass

    def _run(self):
        """Run job handler"""
        val = self.run()
        if val:
            self.append_job(val if isinstance(val, Callable) else self._run)
        elif self.use_after:
            self.append_job(self._after)
        elif self.use_last:
            self.append_job_last(self._last)
        self._complete_jobs()

    def after(self) -> bool | Callable | None:
        """The before function will be run after the run method"""
        pass

    def _after(self):
        """After job handler"""
        val = self.after()
        if isinstance(val, Callable):
            self.append_job(val)
        elif self.use_last:
            self.append_job_last(self._last)
        self._complete_jobs()
        
    def last(self) -> bool | Callable | None:
        """The last function will be run after all the children have been transformed"""
        pass

    def _last(self):
        """Last job handler"""
        val = self.last()
        if isinstance(val, Callable):
            self.append_job(val)
        self._complete_jobs()

    def _complete_jobs(self):
        """Append the temporary job queue to the actual job queue. Only call at the end of the job"""
        self.jobs.reverse()
        for job in self.jobs:
            self.transformer.add_job(job)
        self.jobs = []

    def append_job(self, job: Callable | etree._Element, complete: bool = False):
        """Appends a job to the temporary job queue"""
        self.jobs.append(job)
        if complete:
            self._complete_jobs()
    
    def append_job_last(self, job: Callable | etree._Element):
        """Appends a job to the main job queue after the last transform task"""
        itr = self.el.iter()
        lastchild = last(itr)
        if lastchild != None:
            indx = self.transformer.queue.index(lastchild)
            self.transformer.insert_job(job, indx)

    def clone(self, el: etree._Element, add_jobs: bool = True):
        """Clones an element"""
        clone = deepcopy(el)
        if add_jobs:
            self.add_jobs(clone)
        return clone
    
    def clone_children(self, add_jobs: bool = True) -> List[etree._Element]:
        """Clone the children of the component"""
        return [ self.clone(child, add_jobs=add_jobs) for child in self.el.getchildren() ]

    def clone_before(self, add_jobs: bool = True):
        """Clone children and move them before the component"""
        for child in self.el.getchildren():
            self.el.addprevious(self.clone(child, add_jobs=add_jobs))
        
    def move_before(self):
        """Move children before the component"""
        for child in self.el.getchildren():
            self.el.addprevious(child)
    
    def add_jobs(self, el: etree._Element, include_self: bool = True):
        """Add child jobs"""
        for child in el.iter():
            if include_self or child != el:
                self.append_job(child)
          
    def add_child_jobs(self):
        """Add child jobs"""
        for child in self.el.iter():
            if child != self.el:
                self.append_job(child)
            
    def remove_child_jobs(self):
        """Remove all child jobs"""
        for child in self.el.iter():
            if child in self.transformer.queue:
                self.transformer.queue.remove(child)

    def destroy(self, children: bool = True):
        """Destroy the component node"""
        if children:
            self.remove_child_jobs()
        return self.el.getparent().remove(self.el)
