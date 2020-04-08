from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import lxml.etree

# from future import standard_library
from lark import Lark

from ..transformer.transformer import LatexTransformer, MathMLTransformer

# standard_library.install_aliases()


class ASCIIMathTranslator(object):
    def __init__(self, grammar, *args, **kwargs):
        if "log" in kwargs:
            log = kwargs["log"]
            del kwargs["log"]
        else:
            log = False
        if "transformer" in kwargs:
            transformer = kwargs["transformer"]
            del kwargs["transformer"]
        else:
            transformer = LatexTransformer(log=log)
        if "lexer" in kwargs:
            lexer = kwargs["lexer"]
            del kwargs["lexer"]
        else:
            lexer = "contextual"
        if "parser" in kwargs:
            parser = kwargs["parser"]
            del kwargs["parser"]
        else:
            parser = "lalr"
        if "inplace" in kwargs:
            inplace = kwargs["inplace"]
            del kwargs["inplace"]
        else:
            inplace = False
        self.inplace = inplace
        self.grammar = grammar
        self.transformer = transformer
        if inplace:
            kwargs.update({"transformer": transformer})
        self.parser = Lark(
            grammar, *args, parser=parser, lexer=lexer, **kwargs
        )

    def translate(self, s, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)


class ASCIIMath2Tex(ASCIIMathTranslator):
    def __init__(self, grammar, *args, **kwargs):
        super(ASCIIMath2Tex, self).__init__(
            grammar, *args, transformer=LatexTransformer(), **kwargs
        )


class ASCIIMath2MathML(ASCIIMathTranslator):
    def __init__(self, grammar, *args, **kwargs):
        super(ASCIIMath2MathML, self).__init__(
            grammar, *args, transformer=MathMLTransformer(), **kwargs
        )

    def translate(self, s, displaystyle=True, xml=False, pprint=False):
        if displaystyle:
            dstyle = "<mstyle displaystyle='true'>{}</mstyle>"
        else:
            dstyle = "{}"
        parsed = (
            '<!DOCTYPE math PUBLIC "-//W3C//DTD MathML 3.0//EN" "http://www.w3.org/Math/DTD/mathml3/mathml3.dtd">'
            + "<math xmlns='http://www.w3.org/1998/Math/MathML'>"
            + dstyle
            + "</math>"
        ).format(super(ASCIIMath2MathML, self).translate(s, pprint))
        if xml:
            return lxml.etree.fromstring(
                parsed,
                lxml.etree.XMLParser(dtd_validation=True, no_network=False),
            )
        else:
            return parsed
