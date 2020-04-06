import logging
import re
from functools import wraps
from .const import (
    left_parenthesis,
    right_parenthesis,
    binary_functions,
    unary_functions,
    smb,
)

from lark import Lark, Transformer

from ..utils.log import Log
from ..utils.utils import UtilsMat, concat

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
"""
    Search regex: (\s*)(\S+(\s\S+)?)(\s*)
    Replace regex: $1"\"$2\"": "$2",
"""


class LatexTransformer(Transformer):
    """Trasformer class, read `lark.Transformer`."""

    def __init__(self, log=True, visit_tokens=False):
        super(LatexTransformer, self).__init__(visit_tokens=visit_tokens)
        formatted_left_parenthesis = "|".join(
            ["\\(", "\\(:", "\\[", "\\{", "\\{:"]
        )
        formatted_right_parenthesis = "|".join(
            ["\\)", ":\\)", "\\]", "\\}", ":\\}"]
        )
        self.start_end_par_pattern = re.compile(
            r"^(?:\\left(?:(?:\\)?({})))"
            r"(.*?)"
            r"(?:\\right(?:(?:\\)?({})))$".format(
                formatted_left_parenthesis, formatted_right_parenthesis,
            )
        )
        self._logger_func = logging.info
        if not log:
            self._logger_func = lambda x: x
        self._logger = Log(logger_func=self._logger_func)

    def _log(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self = args[0]
            return self._logger.__call__(f)(*args, **kwargs)

        return decorator

    @_log
    def remove_parenthesis(self, s: str):
        return re.sub(self.start_end_par_pattern, r"\2", s)

    @_log
    def exp_par(self, items):
        yeah_mat = False
        s = ", ".join(items[1:-1])
        if s.startswith("\\left"):
            yeah_mat, row_par = UtilsMat.check_mat(s)
            if yeah_mat:
                s = UtilsMat.get_mat(s, row_par)
        lpar = left_parenthesis[concat(items[0])]
        rpar = right_parenthesis[concat(items[-1])]
        if lpar == "\\langle":
            left = "\\left" + lpar + " "
        elif lpar == "{:":
            left = "\\left."
        else:
            left = "\\left" + lpar
        if rpar == "\\rangle":
            right = " \\right" + rpar
        elif rpar == ":}":
            right = "\\right."
        else:
            right = "\\right" + rpar
        return (
            left
            + ("\\begin{matrix}" + s + "\\end{matrix}" if yeah_mat else s)
            + right
        )

    @_log
    def exp_frac(self, items):
        items[0] = self.remove_parenthesis(items[0])
        items[1] = self.remove_parenthesis(items[1])
        return "\\frac{" + items[0] + "}{" + items[1] + "}"

    @_log
    def exp_under(self, items):
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "_{" + items[1] + "}"

    @_log
    def exp_super(self, items):
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "^{" + items[1] + "}"

    @_log
    def exp_interm(self, items):
        return items[0]

    @_log
    def exp_under_super(self, items):
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        return items[0] + "_{" + items[1] + "}^{" + items[2] + "}"

    @_log
    def symbol(self, items):
        return smb[concat(items[0])]

    @_log
    def const(self, items):
        return items[0].value

    @_log
    def exp_unary(self, items):
        unary = unary_functions[concat(items[0])]
        items[1] = self.remove_parenthesis(items[1])
        if unary == "norm":
            return "\\left\\lVert " + items[1] + " \\right\\rVert"
        elif unary == "abs":
            return "\\left\\mid " + items[1] + " \\right\\mid"
        elif unary == "floor":
            return "\\left\\lfloor " + items[1] + " \\right\\rfloor"
        elif unary == "ceil":
            return "\\left\\lceil " + items[1] + " \\right\\rceil"
        else:
            return unary + "{" + items[1] + "}"

    @_log
    def exp_binary(self, items):
        binary = binary_functions[concat(items[0])]
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        if binary == "\\sqrt":
            return binary + "[" + items[1] + "]" + "{" + items[2] + "}"
        else:
            return binary + "{" + items[1] + "}" + "{" + items[2] + "}"

    @_log
    def q_str(self, items):
        return "\\text{" + items[0] + "}"

    @_log
    def exp(self, items):
        return " ".join(items)


class ASCIIMath2Tex(object):
    def __init__(
        self,
        grammar,
        *args,
        cache=True,
        inplace=False,
        parser="lalr",
        lexer="contextual",
        transformer=LatexTransformer(),
        **kwargs
    ):
        self.inplace = inplace
        self.grammar = grammar
        self.transformer = transformer
        if inplace:
            kwargs.update({"transformer": transformer})
        self.parser = Lark(
            grammar, *args, parser=parser, lexer=lexer, cache=cache, **kwargs
        )

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)
