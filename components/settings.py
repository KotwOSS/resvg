class Settings:
    comments: bool = False
    indent: str = " " * 4
    newl: str = "\n"
    pretty: bool = False
    trust_exp: bool = False
    trust_stmt: bool = False
    hide_logo: bool = False
    input: str
    output: str
    ext = []
    fatal_exit: bool = True

    def __init__(self) -> None:
        pass
