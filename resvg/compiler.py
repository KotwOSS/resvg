# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import os, logging, time
from settings import Settings
from lxml import etree
from transform import Transformer


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
                    remove_blank_text=not Settings.pretty,
                )
                parser.feed(file.read())
                root = parser.close()

                transformer = Transformer(root)
                transformer.transform()

                result = etree.tostring(root, pretty_print=Settings.pretty)

                if Settings.output:
                    with open(Settings.output, "wb") as file:
                        file.write(result)
                else:
                    print()
                    print(result.decode("utf-8"))
                    print()
            end = time.time()
            took = end - start
            logging.info("Finished Compiling! Took §o%sms§R", round(took * 1000))
            print()
    except Exception as e:
        logging.critical(f"Error occured while compiling: {e}")
