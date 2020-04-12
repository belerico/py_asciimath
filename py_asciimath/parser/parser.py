from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import logging

import lxml.etree

# from future import standard_library
from lark import Lark

from .. import PROJECT_ROOT
from ..transformer.transformer import LatexTransformer, MathMLTransformer
from ..utils.utils import check_connection, get_dtd, validate_dtd

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

# standard_library.install_aliases()


class Translator(object):
    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__()

    def translate(self, s):
        raise NotImplementedError


class ASCIIMathTranslator(Translator):
    def __init__(self, grammar, *args, **kwargs):
        super(ASCIIMathTranslator, self).__init__(*args, **kwargs)
        if "transformer" in kwargs:
            transformer = kwargs["transformer"]
            del kwargs["transformer"]
        else:
            transformer = LatexTransformer(log=True)
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
        if "log" in kwargs:
            log = kwargs["log"]
            del kwargs["log"]
        else:
            log = False
        super(ASCIIMath2Tex, self).__init__(
            grammar, *args, transformer=LatexTransformer(log=log), **kwargs
        )

    def translate(self, s, displaystyle=False, pprint=False):
        logging.info("TRANSLATING...")
        if displaystyle:
            return (
                "\\["
                + super(ASCIIMath2Tex, self).translate(s, pprint=pprint)
                + "\\]"
            )
        else:
            return (
                "$"
                + super(ASCIIMath2Tex, self).translate(s, pprint=pprint)
                + "$"
            )


class ASCIIMath2MathML(ASCIIMathTranslator):
    def __init__(self, grammar, *args, **kwargs):
        if "log" in kwargs:
            log = kwargs["log"]
            del kwargs["log"]
        else:
            log = False
        super(ASCIIMath2MathML, self).__init__(
            grammar, *args, transformer=MathMLTransformer(log=log), **kwargs
        )

    def translate(
        self,
        s,
        displaystyle=False,
        dtd=None,
        dtd_validation=False,
        network=False,
        pprint=False,
        xml_pprint=True,
    ):
        if displaystyle:
            dstyle = '<mstyle displaystyle="true">{}</mstyle>'
        else:
            dstyle = "{}"
        if network:
            if check_connection():
                dtd_head = get_dtd(dtd, True)
            else:
                network = False
                dtd_head = get_dtd(dtd, False)
                logging.info("NO CONNECTION AVAILABLE...")
        else:
            dtd_head = get_dtd(dtd, False)
        parsed = dtd_head + (
            (
                '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                if dtd != "mathml1"
                else "<math>"
            )
            + dstyle.format(super(ASCIIMath2MathML, self).translate(s, pprint))
            + "</math>"
        )
        if dtd_validation or xml_pprint:
            parsed = validate_dtd(parsed, dtd_validation, network)
            parsed = lxml.etree.tostring(
                parsed, pretty_print=xml_pprint, doctype=dtd_head,
            ).decode()
        return parsed


class MathML2Tex(Translator):
    def __init__(self, *args, **kwargs):
        super(MathML2Tex, self).__init__(*args, **kwargs)
        transformer = lxml.etree.parse(
            open(PROJECT_ROOT + "/translation/mathml2tex/mmltex.xsl", "rb")
        )
        self.transformer = lxml.etree.XSLT(transformer)

    def translate(
        self, s, dtd_validation=False, network=False,
    ):
        if network:
            if not check_connection():
                network = False
                logging.info("NO CONNECTION AVAILABLE...")
        return str(
            self.transformer(
                validate_dtd(s, dtd_validation, network, resolve_entities=True)
            )
        )
