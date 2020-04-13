from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import logging
import os
import re

import lxml.etree

# from future import standard_library
from lark import Lark

from .. import PROJECT_ROOT
from ..grammar.asciimath_grammar import asciimath_grammar
from ..transformer.transformer import LatexTransformer, MathMLTransformer
from ..utils.utils import check_connection, get_dtd, validate_dtd

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

# standard_library.install_aliases()


class Translator(object):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__()

    def _from_file(self, from_file):
        if os.path.exists(from_file):
            logging.info("Loading file '" + from_file + "'...")
            with open(from_file) as f:
                s = f.read()
                f.close()
            return s
        else:
            raise FileNotFoundError("File '" + from_file + "' not found")

    def _to_file(self, s, to_file):
        logging.info("Writing translation to '" + to_file + "'...")
        with open(to_file, "w") as f:
            f.write(s)
            f.close()

    def _translate(self, s, *args, **kwargs):
        raise NotImplementedError

    def translate(self, s, *args, **kwargs):
        if "from_file" in kwargs:
            from_file = kwargs["from_file"]
            del kwargs["from_file"]
        else:
            from_file = False
        if "to_file" in kwargs:
            to_file = kwargs["to_file"]
            del kwargs["to_file"]
        else:
            to_file = None
        if from_file:
            s = self._from_file(s)
        logging.info("Translating...")
        s = self._translate(s, *args, **kwargs)
        if to_file is not None:
            self._to_file(s, to_file)
        return s


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

    def _translate(self, s, *args, **kwargs):
        if "pprint" in kwargs:
            pprint = kwargs["pprint"]
            del kwargs["pprint"]
        else:
            pprint = False
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)


class ASCIIMath2Tex(ASCIIMathTranslator):
    def __init__(self, *args, **kwargs):
        if "log" in kwargs:
            log = kwargs["log"]
            del kwargs["log"]
        else:
            log = False
        super(ASCIIMath2Tex, self).__init__(
            asciimath_grammar,
            *args,
            transformer=LatexTransformer(log=log),
            **kwargs
        )

    def _translate(self, s, *args, **kwargs):
        if "pprint" in kwargs:
            pprint = kwargs["pprint"]
            del kwargs["pprint"]
        else:
            pprint = False
        if "displaystyle" in kwargs:
            displaystyle = kwargs["displaystyle"]
            del kwargs["displaystyle"]
        else:
            displaystyle = False
        if displaystyle:
            return (
                "\\["
                + super(ASCIIMath2Tex, self)._translate(s, pprint=pprint)
                + "\\]"
            )
        else:
            return (
                "$"
                + super(ASCIIMath2Tex, self)._translate(s, pprint=pprint)
                + "$"
            )


class ASCIIMath2MathML(ASCIIMathTranslator):
    def __init__(self, *args, **kwargs):
        if "log" in kwargs:
            log = kwargs["log"]
            del kwargs["log"]
        else:
            log = False
        super(ASCIIMath2MathML, self).__init__(
            asciimath_grammar,
            *args,
            transformer=MathMLTransformer(log=log),
            **kwargs
        )

    def _translate(self, s, *args, **kwargs):
        if "xml_pprint" in kwargs:
            xml_pprint = kwargs["xml_pprint"]
            del kwargs["xml_pprint"]
        else:
            xml_pprint = True
        if "pprint" in kwargs:
            pprint = kwargs["pprint"]
            del kwargs["pprint"]
        else:
            pprint = False
        if "network" in kwargs:
            network = kwargs["network"]
            del kwargs["network"]
        else:
            network = False
        if "dtd_validation" in kwargs:
            dtd_validation = kwargs["dtd_validation"]
            del kwargs["dtd_validation"]
        else:
            dtd_validation = False
        if "dtd" in kwargs:
            dtd = kwargs["dtd"]
            del kwargs["dtd"]
        else:
            dtd = None
        if "displaystyle" in kwargs:
            displaystyle = kwargs["displaystyle"]
            del kwargs["displaystyle"]
        else:
            displaystyle = False
        if displaystyle:
            dstyle = '<mstyle displaystyle="true">{}</mstyle>'
        else:
            dstyle = "{}"
        if network:  # pragma: no cover
            if check_connection():
                dtd_head = get_dtd(dtd, True)
            else:
                network = False
                dtd_head = get_dtd(dtd, False)
                logging.warn("No connection available...")
        else:
            dtd_head = get_dtd(dtd, False)
        parsed = dtd_head + (
            (
                '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                if dtd != "mathml1"
                else "<math>"
            )
            + dstyle.format(
                super(ASCIIMath2MathML, self)._translate(s, pprint=pprint)
            )
            + "</math>"
        )
        if dtd_validation or xml_pprint:
            parsed = validate_dtd(parsed, dtd_validation, network)
            parsed = lxml.etree.tostring(
                parsed, pretty_print=xml_pprint, doctype=dtd_head,
            ).decode()
        return parsed


class MathML2Tex(Translator):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        super(MathML2Tex, self).__init__(*args, **kwargs)
        transformer = lxml.etree.parse(
            open(PROJECT_ROOT + "/translation/mathml2tex/mmltex.xsl", "rb")
        )
        self.transformer = lxml.etree.XSLT(transformer)
        self.doctype_pattern = re.compile(
            r"(<!DOCTYPE math ([A-Z]+).*?mathml(\d)?\.dtd\">)"
        )

    def _translate(self, s, *args, **kwargs):
        if "network" in kwargs:
            network = kwargs["network"]
            del kwargs["network"]
        else:
            network = False
        if network:
            if not check_connection():
                network = False
                logging.warn("No connection available...")
        match = re.match(self.doctype_pattern, s)
        if match is not None:
            if match.group(3) is None or match.group(3) == "1":
                raise NotImplementedError(
                    "Translation from MathML1 is not supported"
                )
            if match.group(2) == "PUBLIC" and not network:
                logging.warn(
                    "Remote DTD found and network is False: "
                    "replacing with local DTD"
                )
                s = (
                    get_dtd("mathml" + match.group(3), False)
                    + s[match.span(1)[1] :]
                )
            elif match.group(2) == "SYSTEM" and network:
                logging.warn(
                    "Local DTD found and network is True: "
                    "no need to bother your ISP"
                )
                network = False
        else:
            logging.warn(
                "No DTD declaration found: "
                "validating against local MathML3 DTD"
            )
            s = get_dtd("mathml3", False) + s
        parsed = validate_dtd(s, True, network, resolve_entities=True)
        logging.info("Translating...")
        return str(self.transformer(parsed))
