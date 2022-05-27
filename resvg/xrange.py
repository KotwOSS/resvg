# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS


class xrange:
    start: float
    stop: float
    step: float

    def __init__(self, *args) -> None:
        argslen = len(args)
        self.start = args[0] if argslen > 1 else 0
        self.stop = args[1] if argslen > 1 else args[0] if argslen == 1 else 0
        self.step = args[2] if argslen > 2 else 1
