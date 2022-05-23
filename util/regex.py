# Regex utility functions
def multi_replace(value, regex, valuator):
    txt = ""
    endidx = 0
    res = regex.finditer(value)
    for exp in res:
        txt += value[endidx : exp.start(0)] + valuator(exp)
        endidx = exp.end(0)
    return txt + value[endidx:]
