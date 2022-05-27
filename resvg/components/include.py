# Created on Fri May 27 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Tuple
from component import Component
from settings import Settings
from raw import Raw
from lxml import etree
import requests, os, re, logging


class Include(Component):
    url_regex = re.compile("/+")

    arguments = {
        "url": (lambda an, av: an == "url", Raw(str), False),
        "kup": (lambda an, av: an == "kup", Raw(str), False),
        "path": (lambda an, av: an == "path", Raw(str), False),
    }

    url: Tuple[str, bool]
    kup: Tuple[str, bool]
    path: Tuple[str, bool]

    def run(self):
        if not os.path.isdir(Settings.lib_dir):
            os.mkdir(Settings.lib_dir)

        url: str | None = None
        if hasattr(self, "url"):
            url = self.url[1]
        elif hasattr(self, "kup"):
            url = "https://u.kotw.dev/api/d/" + self.kup[1]

        if url:
            filename = ":".join(self.url_regex.split(url)[1:])
            lib_path = os.path.join(Settings.lib_dir, filename)
            if not os.path.isfile(lib_path):
                logging.info("Fetching library from §o%s§R", url)
                response = requests.get(url)
                logging.info("Saving library to §o%s§R", lib_path)
                with open(lib_path, "wb") as f:
                    f.write(response.content)
        elif hasattr(self, "path"):
            lib_path = self.path[1]
        else:
            raise RuntimeError(
                "§oinclude§R components must have an §ourl§R or §okup§R or §opath§R argument"
            )

        logging.info("Including library from §o%s§R", lib_path)
        with open(lib_path, "r") as f:
            parser = etree.XMLParser(
                remove_comments=not Settings.comments, remove_blank_text=True
            )
            parser.feed(f.read())
            el = parser.close()

            self.el.addprevious(el)
            self.add_jobs(el)

        self.destroy()
