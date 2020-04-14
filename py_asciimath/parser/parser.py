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

    def translate(self, s, from_file=False, to_file=None, *args, **kwargs):
        """Translates an input expression `s`

        Args:
            s (str): String to translate. If from_file is `True`, then `s`
                must represent the file's path
            from_file (bool, optional): If `True`, load the string to translate
                from the file specified by `s`. Defaults to False.
            to_file (str, optional): If specified, save the translation to
                `to_file`. Defaults to None.

        Returns:
            str: Translated expression
        """
        if from_file:
            s = self._from_file(s)
        logging.info("Translating...")
        s = self._translate(s, *args, **kwargs)
        if to_file is not None:
            self._to_file(s, to_file)
        return s


class ASCIIMathTranslator(Translator):
    """Class that handle the translation from ASCIIMath.

    An ASCIIMathTranslator translates an ASCIIMath string into another
    language, specified by the `transformer` parameter

    Args:
        grammar (str): ASCIIMath grammar
        transformer (lark.Transformer): A transformer to transform parsed
            input. See `~lark.Transformer`
        lexer (str, optional): Lexer used during parsing. See `~lark.Lark`.
            Defaults to "contextual".
        log (bool, optional): If True log the parsing process.
            Defaults to False.
        inplace (bool, optional): If True, parse the input inplace.
            See `~lark.Lark`. Defaults to True.
        parser (str, optional): Parser algorithm. See `~lark.Lark`.
            Defaults to "lalr".
        *args: Additional variable length argument list
            to the `~lark.Lark` class.
        **kwargs: Additional keyword arguments to the `~lark.Lark` class.
    """

    def __init__(
        self,
        grammar,
        transformer,
        lexer="contextual",
        log=False,
        inplace=True,
        parser="lalr",
        *args,
        **kwargs
    ):
        super(ASCIIMathTranslator, self).__init__()
        self.inplace = inplace
        self.grammar = grammar
        self.transformer = transformer
        if inplace:
            kwargs.update({"transformer": transformer})
        self.parser = Lark(
            grammar, *args, parser=parser, lexer=lexer, **kwargs
        )

    def _translate(self, s, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)


class ASCIIMath2Tex(ASCIIMathTranslator):
    """Class that handle the translation from ASCIIMath to LaTeX

    Args:
        transformer (lark.Transformer): A transformer to transform parsed
            input. See `~lark.Transformer`
        lexer (str, optional): Lexer used during parsing. See `~lark.Lark`.
            Defaults to "contextual".
        log (bool, optional): If True log the parsing process.
            Defaults to False.
        inplace (bool, optional): If True, parse the input inplace.
            See `~lark.Lark`. Defaults to True.
        parser (str, optional): Parser algorithm. See `~lark.Lark`.
            Defaults to "lalr".
        *args: Additional variable length argument list
            to the `~lark.Lark` class.
        **kwargs: Additional keyword arguments to the `~lark.Lark` class.
    """

    def __init__(self, *args, **kwargs):
        super(ASCIIMath2Tex, self).__init__(
            asciimath_grammar,
            LatexTransformer(log=kwargs.pop("log", False)),
            *args,
            **kwargs
        )

    def _translate(self, s, displaystyle=False, pprint=False):
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

    def translate(
        self,
        s,
        displaystyle=False,
        from_file=False,
        pprint=False,
        to_file=None,
    ):
        """Translates an ASCIIMath string to LaTeX

        Args:
            s (str): String to translate. If from_file is `True`, then `s`
                must represent the file's path
            displaystyle (bool, optional): Add displaystyle attribute.
                Defaults to False.
            from_file (bool, optional): If `True`, load the string to translate
                from the file specified by `s`. Defaults to False.
            pprint (bool, optional): Abstract Syntax Tree pretty print.
                Defaults to False.
            to_file (str, optional): If specified, save the translation to
                `to_file`. Defaults to None.

        Returns:
            str: LaTeX translated expression
        """
        return super(ASCIIMath2Tex, self).translate(
            s,
            displaystyle=displaystyle,
            from_file=from_file,
            pprint=pprint,
            to_file=to_file,
        )


class ASCIIMath2MathML(ASCIIMathTranslator):
    """Class that handle the translation from ASCIIMath to MathML

    Args:
        transformer (lark.Transformer): A transformer to transform parsed
            input. See `~lark.Transformer`
        lexer (str, optional): Lexer used during parsing. See `~lark.Lark`.
            Defaults to "contextual".
        log (bool, optional): If True log the parsing process.
            Defaults to False.
        inplace (bool, optional): If True, parse the input inplace.
            See `~lark.Lark`. Defaults to True.
        parser (str, optional): Parser algorithm. See `~lark.Lark`.
            Defaults to "lalr".
        *args: Additional variable length argument list
            to the `~lark.Lark` class.
        **kwargs: Additional keyword arguments to the `~lark.Lark` class.
    """

    def __init__(self, *args, **kwargs):
        super(ASCIIMath2MathML, self).__init__(
            asciimath_grammar,
            MathMLTransformer(log=kwargs.pop("log", False)),
            *args,
            **kwargs
        )

    def _translate(
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

    def translate(
        self,
        s,
        displaystyle=False,
        dtd=None,
        dtd_validation=False,
        from_file=False,
        network=False,
        pprint=False,
        to_file=None,
        xml_pprint=True,
    ):
        """Translates an ASCIIMath string to MathML

        Args:
            s (str): String to translate. If from_file is `True`, then `s`
                must represent the file's path
            displaystyle (bool, optional): Add displaystyle attribute.
                Defaults to False.
            dtd (str, optional): MathML DTD version to validate the output
                against. It can be: `mathml1`, `mathml2` or `mathml3`.
                Defaults to None.
            dtd_validation (bool, optional): If `True` validate output against
                the DTD version specified by `dtd`.
                Defaults to False.
            from_file (bool, optional): If `True`, load the string to translate
                from the file specified by `s`. Defaults to False.
            network (bool, optional): If `True` validate the output against
                a remote DTD.
                Defaults to False.
            pprint (bool, optional): Abstract Syntax Tree pretty print.
                Defaults to False.
            to_file (str, optional): If specified, save the translation to
                `to_file`. Defaults to None.
            xml_pprint (bool, optional): XML pretty print. Defaults to True.

        Returns:
            str: MathML translated expression
        """
        return super(ASCIIMath2MathML, self).translate(
            s,
            displaystyle=displaystyle,
            dtd=dtd,
            dtd_validation=dtd_validation,
            from_file=from_file,
            network=network,
            pprint=pprint,
            to_file=to_file,
            xml_pprint=xml_pprint,
        )


class MathML2Tex(Translator):  # pragma: no cover
    """Class that handle the translation from MathML to LaTeX

    The translation from MathML to LaTeX is done via the XSLT provided by
    https://sourceforge.net/projects/xsltml/
    """

    def __init__(self):
        super(MathML2Tex, self).__init__()
        transformer = lxml.etree.parse(
            open(PROJECT_ROOT + "/translation/mathml2tex/mmltex.xsl", "rb")
        )
        self.transformer = lxml.etree.XSLT(transformer)
        self.doctype_pattern = re.compile(
            r"(<!DOCTYPE math ([A-Z]+).*?mathml(\d)?\.dtd\">)"
        )

    def _translate(self, s, network=False):
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

    def translate(self, s, from_file=False, network=False, to_file=None):
        """Translates a MathML string to LaTeX

        Args:
            s (str): String to translate. If from_file is `True`, then `s`
                must represent the file's path
            from_file (bool, optional): If `True`, load the string to translate
                from the file specified by `s`. Defaults to False.
            network (bool, optional): If `True` validate the output against
                a remote DTD.
                Defaults to False.
            to_file (str, optional): If specified, save the translation to
                `to_file`. Defaults to None.

        Returns:
            str: LaTeX translated expression
        """
        return super(MathML2Tex, self).translate(
            s, from_file=from_file, network=network, to_file=to_file
        )
