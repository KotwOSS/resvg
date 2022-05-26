# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import os, logging, time
from components.library import Library
from settings import Settings
from lxml import etree
from transform import Transform

def compile():
    try:
        if Settings.input != None and os.path.isfile(Settings.input):
            logging.info(
                "Compiling §o%s§R > §o%s§R...",
                Settings.input,
                Settings.output if Settings.output else "stdout",
            )
            start = time.time()
            with open(Settings.input, "r") as file:
                parser = etree.XMLParser(
                    remove_comments=not Settings.comments,
                    remove_blank_text=True,
                )
                parser.feed(file.read())
                root = parser.close()

                Library.reset()
                transform = Transform(root)
                transform.register_default_transformers()
                transform.transform()

                etree.cleanup_namespaces(root)

                result = etree.tostring(root, pretty_print=Settings.pretty)

                if Settings.output:
                    with open(Settings.output, "wb") as file:
                        file.write(result)
                else:
                    if not Settings.silent:
                        print()
                    print(result.decode("utf-8"))
                    if not Settings.silent:
                        print()
            end = time.time()
            took = end - start
            millis = took * 1000
            logging.info(
                "Finished Compiling! Took §o%s§R ms", f"{millis:10.3f}".strip()
            )
    except Exception as e:
        logging.exception("Error occured while compiling: %s", e)

    if not Settings.silent:
        print()
