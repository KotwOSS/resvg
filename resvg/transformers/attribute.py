# Created on Thu May 26 2022
#
# Copyright (c) 2022 KotwOSS

from typing import Any
from transformer import Transformer
from expression import SafeExpression
from settings import Settings
from lxml import etree
import reutil, re


class AttributeTransformer(Transformer):
    expression_regex = re.compile(r"{([a-zA-Z0-9.*/+-^()\"' ]+)}")

    """Transform expressions in attributes"""

    def __call__(self, el: etree._Element) -> bool:
        for attr in el.attrib.items():
            attrname = attr[0]
            attrval = attr[1]

            attrval = reutil.multi_replace(
                attrval,
                self.expression_regex,
                lambda exp: reutil.stringify(
                    SafeExpression(exp.group(1), self.transformer.vars, Any).eval()
                ),
            )

            if attrname.startswith(Settings.resvg_namespace):
                name = attrname[len(Settings.resvg_namespace) :]
                el.attrib[name] = reutil.stringify(
                    SafeExpression(attrval, self.transformer.vars, Any).eval()
                )
                del el.attrib[attrname]
            else:
                el.attrib[attrname] = attrval
        return False
