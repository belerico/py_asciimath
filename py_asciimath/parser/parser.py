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
from ..utils.utils import check_connection

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
        xml_declaration=False,
        xml_pprint=True,
        **kwargs
    ):
        if displaystyle:
            dstyle = '<mstyle displaystyle="true">{}</mstyle>'
        else:
            dstyle = "{}"
        if network:  # pragma: no cover
            if check_connection():
                doctype = MathMLParser.get_doctype(dtd, True)
            else:
                network = False
                doctype = MathMLParser.get_doctype(dtd, False)
                logging.warn("No connection available...")
        else:
            doctype = MathMLParser.get_doctype(dtd, False)
        parsed = (
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
        if dtd_validation or xml_pprint or xml_declaration:
            parsed = MathMLParser.parse(
                parsed, dtd, dtd_validation, network, **kwargs
            )
            encoding = parsed.getroottree().docinfo.encoding
            parsed = lxml.etree.tostring(
                parsed,
                pretty_print=xml_pprint,
                doctype=(doctype if dtd_validation else None),
                xml_declaration=xml_declaration,
                encoding=encoding,
            ).decode(encoding)
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
        xml_declaration=False,
        xml_pprint=True,
        **kwargs
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
                `to_file`.
                Defaults to None.
            xml_declaration (bool, optional): If True, include the XML
                declaration at the beginning of the file.
                Defaults to False.
            xml_pprint (bool, optional): XML pretty print. Defaults to True.
            **kwargs: Additional ~lxml.extree.XMLParser options

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
            xml_declaration=xml_declaration,
            xml_pprint=xml_pprint,
            **kwargs
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

    def _translate(self, s, network=False, **kwargs):
        if network:
            if not check_connection():
                network = False
                logging.warn("No connection available...")
        mml_version = MathMLParser.get_doctype_version(s)
        if mml_version is None or mml_version == "1":
            raise NotImplementedError(
                "Translation from MathML1 is not supported"
            )
        parsed = MathMLParser.parse(
            s,
            dtd_validation=True,
            network=network,
            resolve_entities=True,
            **kwargs
        )
        logging.info("Translating...")
        return str(self.transformer(parsed))

    def translate(
        self, s, from_file=False, network=False, to_file=None, **kwargs
    ):
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
            **kwargs: ~lxml.extree.XMLParser options

        Returns:
            str: LaTeX translated expression
        """
        return super(MathML2Tex, self).translate(
            s, from_file=from_file, network=network, to_file=to_file, **kwargs
        )


class MathMLParser(object):

    xml_decl_pattern = re.compile(
        r"(<\?xml.*?(encoding=(?:'|\")(.*?)(?:'|\"))?\?>)"
    )
    doctype_pattern = re.compile(
        r"(<!DOCTYPE math ([A-Z]+).*?mathml(\d)?\.dtd\">)", re.MULTILINE
    )

    def __init__(self, *args, **kwargs):
        super(MathMLParser, self).__init__()

    @classmethod
    def get_encoding(cls, s):
        r"""Get the encoding from the XML declaration

        The XML declaration is supposed to match the following
        pattern: (<\\?xml.*?(encoding=(?:'|\\")(.*?)(?:'|\\"))?\\?>).
        If the XML declaration is not found, then `None` will be returned

        Args:
            s (str): XML string

        Raises:
            Exception: If the XML declaration is not at the beginning
                of the string

        Returns:
            str: Encoding of the XML document
        """
        xml_decl_match = re.match(cls.xml_decl_pattern, s)
        if xml_decl_match is not None:
            if xml_decl_match.span(1)[0] != 0:
                raise Exception(
                    "XML declaration must be at the beginning of the file"
                )
            encoding = xml_decl_match.group(3)
            logging.info("Encoding from XML declaration: " + encoding)
        else:
            encoding = None
            logging.warn(
                "No XML declaration with 'encoding' attribute set: "
                "default encoding to None"
            )
        return encoding

    @classmethod
    def set_doctype(cls, s, network, dtd=None):
        r"""Set MathML DOCTYPE of the XML document

        The DOCTYPE field is supposed to match the following
        pattern: (<!DOCTYPE math ([A-Z]+).*?mathml(\\d)?\\.dtd\\">).
        If the MathML DOCTYPE is not found, then the MathML3 DTD
        will be returned

        Args:
            s (str): XML string
            network (bool): If True, return the PUBLIC MathML DTD;
                otherwise use the local MathML DTD
            dtd (str): Version of the default MathML DTD, If the DTD is not
                found. If None will be used MathML3 DTD
                Defaults to None

        Raises:
            Exception: If the XML declaration is not at the beginning
                of the string

        Returns:
            str, str: s replaced with the DTD following the specifications
                and the MathML version
        """
        doctype_match = list(re.finditer(cls.doctype_pattern, s))
        if len(doctype_match) > 1:
            raise Exception("Multiple DOCTYPE declarations found")
        if doctype_match != []:
            doctype_match = doctype_match[0]
            if doctype_match.group(2) == "PUBLIC" and not network:
                logging.warn(
                    "Remote DTD found and network is False: "
                    "replacing with local DTD"
                )
                s = (
                    s[: doctype_match.span(1)[0]]
                    + cls.get_doctype("mathml" + doctype_match.group(3), False)
                    + s[doctype_match.span(1)[1] :]
                )
            elif "http" not in doctype_match.group(1) and network:
                logging.warn(
                    "Local DTD found and network is True: "
                    "no need to bother your ISP"
                )
        else:
            logging.warn(
                "No DTD declaration found: "
                "set to local {} DTD".format(
                    dtd if dtd is not None else "mathml3"
                )
            )
            xml_decl_match = re.match(cls.xml_decl_pattern, s)
            if xml_decl_match is None:
                start = 0
            else:
                start = xml_decl_match.span(1)[1]
            if dtd is not None:
                doctype = cls.get_doctype(dtd, False)
            else:
                doctype = cls.get_doctype("mathml3", False)
            s = s[:start] + doctype + s[start:]
        return s

    @classmethod
    def get_doctype_version(cls, xml):
        """Get the MathML DTD version from DOCTYPE declaration

        Args:
            xml (str): XML document

        Raises:
            Exception: If multiple DOCTYPE declarations are found

        Returns:
            str: MathML DTD version (1,2,3); None if DOCTYPE is not found
        """
        doctype_match = list(re.finditer(cls.doctype_pattern, xml))
        if len(doctype_match) > 1:
            raise Exception("Multiple DOCTYPE declarations found")
        elif doctype_match != []:
            return doctype_match[0].group(3)
        else:
            return None

    @staticmethod
    def get_doctype(dtd, network):
        """Get a MathML DOCTYPE declaration

        Args:
            dtd (str): MathML DTD type. Must be on of the following:
                `mathml1`, `mathml2` or `mathml3`
            network (bool): If True, get a public DTD; otherwise a local
                DTD declaration will be set

        Raises:
            NotImplementedError: Other DTD declarations but MathML
                will be discarded

        Returns:
            str: DOCTYPE declaration following the specifics
        """
        doctype = "<!DOCTYPE math {}>"
        if dtd is None or dtd.lower() == "mathml3":
            doctype = doctype.format(
                'PUBLIC "-//W3C//DTD MathML 3.0//EN" '
                + '"http://www.w3.org/Math/DTD/mathml3/mathml3.dtd"'
                if network
                else "SYSTEM "
                + '"'
                + PROJECT_ROOT
                + '/dtd/mathml3/mathml3.dtd"'
            )
        elif dtd.lower() == "mathml1":
            doctype = doctype.format(
                "SYSTEM "
                + (
                    '"http://www.w3.org/Math/DTD/mathml1/mathml.dtd"'
                    if network
                    else '"' + PROJECT_ROOT + '/dtd/mathml1/mathml1.dtd"'
                )
            )
        elif dtd.lower() == "mathml2":
            doctype = doctype.format(
                'PUBLIC "-//W3C//DTD MathML 2.0//EN" '
                + '"http://www.w3.org/Math/DTD/mathml2/mathml2.dtd"'
                if network
                else "SYSTEM "
                + '"'
                + PROJECT_ROOT
                + '/dtd/mathml2/mathml2.dtd"'
            )
        else:
            raise NotImplementedError(
                "DTD validation only against MathML DTD 1, 2 or 3"
            )
        return doctype

    @staticmethod
    def get_parser(
        dtd_validation=True,
        network=False,
        ns_clean=True,
        resolve_entities=False,
        **kwargs
    ):
        """Create a MathML XML parser

        Args:
            dtd_validation (bool, optional): Validate XML against DTD during
                parsing. Defaults to True.
            network (bool, optional): Validate against remote DTD.
                Defaults to False.
            ns_clean (bool, optional): Clean up redundant namespace
                declarations. Defaults to True.
            resolve_entities (bool, optional): replace entities by their text
                value. Defaults to False.
            **kwargs: Additional ~lxml.extree.XMLParser options

        Returns:
            str: Parsed and possibly validated MathML XML
        """
        return lxml.etree.XMLParser(
            dtd_validation=dtd_validation,
            no_network=(not network),
            resolve_entities=resolve_entities,
            ns_clean=ns_clean,
            **kwargs
        )

    @staticmethod
    def parse(
        xml,
        dtd=None,
        dtd_validation=True,
        network=False,
        ns_clean=True,
        resolve_entities=False,
        **kwargs
    ):  # pragma: no cover
        """Parse a MathML XML

        Args:
            xml (str): String representing a MathML XML.
            dtd_validation (bool, optional): Validate XML against DTD during
                parsing. Defaults to True.
            network (bool, optional): Validate against remote DTD.
                Defaults to False.
            ns_clean (bool, optional): Clean up redundant namespace
                declarations. Defaults to True.
            resolve_entities (bool, optional): replace entities by their text
                value. Defaults to False.
            **kwargs: Additional ~lxml.extree.XMLParser options

        Returns:
            str: Parsed and possibly validated MathML XML

        Todo:
            * Load xml from file
        """
        encoding = MathMLParser.get_encoding(xml)
        if encoding is None:
            logging.warning("The XML encoding is None: default to UTF-8")
            encoding = "UTF-8"
        xml = MathMLParser.set_doctype(xml, network, dtd=dtd)
        xml = xml.encode(encoding)
        if dtd_validation:
            if network:
                logging.info("Validating against remote dtd...")
            else:
                logging.info("Validating against local dtd...")
            logging.info("Loading dtd and validating...")
        mathml_parser = MathMLParser.get_parser(
            dtd_validation=dtd_validation,
            network=network,
            ns_clean=ns_clean,
            resolve_entities=False,
            **kwargs
        )
        return lxml.etree.fromstring(xml, mathml_parser)
