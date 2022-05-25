# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import logging, compiler, os, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from settings import Settings


def watch():
    if (
        Settings.input
        and os.path.exists(Settings.input)
        and Settings.watch
        and os.path.exists(Settings.watch)
    ):
        observer = Observer()

        observer.schedule(WatchHandler(), Settings.watch, recursive=True)
        ext_str = "§g, §y'.".join(Settings.ext)
        logging.info(
            "Watching §o'%s'§R for changes on §g[§y'.%s'§g]§R...",
            Settings.watch,
            ext_str,
        )

        compiler.compile()

        observer.start()

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("Observer stopped.")

        observer.join()
    else:
        if Settings.input:
            logging.exit_fatal("Input file not found.")
        else:
            logging.exit_fatal("No input file specified")


class WatchHandler(FileSystemEventHandler):
    compiling = False

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "modified":
            if (
                not WatchHandler.compiling
                and event.src_path.split(".").pop() in Settings.ext
            ):
                logging.warning("File updated! Recompiling...")
                WatchHandler.compiling = True
                compiler.compile()
                WatchHandler.compiling = False
