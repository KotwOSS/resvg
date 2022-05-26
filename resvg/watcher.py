# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import logging, compiler, os, time, colors
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

        if not Settings.silent:
            print(
                colors.format(
                    f"""\
§g[ ------ §yCommands§g ------ ]§R
§g[ §B§ocls§R §g->§R clear screen    §g]§R
§g[ §B§ore§R  §g->§R force recompile §g]§R
§g[ §B§oq§R   §g->§R quit            §g]§R
§g[ ------ §yCommands§g ------ ]§R
                \n"""
                )
            )

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
                op = input().lower()
                print("\033[F\033[K\033[1A")
                if op == "re":
                    logging.warning("Recompile forced...")
                    compiler.compile()
                elif op == "cls":
                    print("\033[2J\033[1;1H")
                elif op == "q":
                    raise KeyboardInterrupt()
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
    def __init__(self) -> None:
        super().__init__()

        self.last_time = 0

    def on_modified(self, event):
        if not event.is_directory:

            tm = time.time()
            if tm - self.last_time > Settings.min_time:
                self.last_time = tm

                if event.src_path.split(".").pop() in Settings.ext:
                    logging.warning("File updated! Recompiling...")
                    WatchHandler.compiling = True
                    compiler.compile()
                    WatchHandler.compiling = False
