# Regex utility functions
from re import Pattern
from typing import Any, Dict


def multi_replace(value: str, regex: Pattern[Any], valuator):
    """Replace regex matches with a value"""
    txt = ""
    endidx = 0
    res = regex.finditer(value)
    for exp in res:
        txt += value[endidx : exp.start(0)] + valuator(exp)
        endidx = exp.end(0)
    return txt + value[endidx:]


def stringify(val: Any):
    """Stringify a value"""

    if isinstance(val, str):
        return val
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        val = float(f"{val:10.3f}")
        if val.is_integer():
            return str(int(val))
        else:
            return str(val)
    else:
        return str(val)

def concat_dict(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Concatenate two dictionaries"""
    dict1.update(dict2)
    return dict1