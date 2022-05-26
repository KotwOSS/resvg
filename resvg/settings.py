# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS


class Settings:
    # Generic information
    version = "0.0.0alpha3"
    authors = ["KotwOSS"]
    license = "MIT"
    year = 2022

    resvg_namespace: str = "{http://oss.kotw.dev/resvg}"

    no_color: bool
    comments: bool
    min_time: float
    pretty: bool
    compile: bool
    watch: str
    trust_exp: bool
    trust_stmt: bool
    silent: bool
    hide_logo: bool
    input: str
    output: str
    ext = []
    log: str
    level: int
