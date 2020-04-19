from itertools import islice

from ..const import get_symbols_for
from ..utils.utils import alias_string

unary_functions = get_symbols_for("unary_functions", "asciimath", "latex")
unary_functions.update(
    get_symbols_for("function_symbols", "asciimath", "latex")
)
binary_functions = get_symbols_for("binary_functions", "asciimath", "latex")
left_parenthesis = get_symbols_for("left_parenthesis", "asciimath", "latex")
left_parenthesis.pop('"\\{"')
right_parenthesis = get_symbols_for("right_parenthesis", "asciimath", "latex")
right_parenthesis.pop('"\\}"')

smb = get_symbols_for("misc_symbols", "asciimath", "latex")
smb.update(get_symbols_for("colors", "asciimath", "latex"))
smb.update(get_symbols_for("relation_symbols", "asciimath", "latex"))
smb.update(get_symbols_for("logical_symbols", "asciimath", "latex"))
smb.update(get_symbols_for("operation_symbols", "asciimath", "latex"))
smb.update(get_symbols_for("greek_letters", "asciimath", "latex"))
smb.update(get_symbols_for("arrows", "asciimath", "latex"))
smb = dict(sorted(smb.items(), key=lambda x: (-len(x[0]), x[0])))

latex_grammar = r"""
    %import common.WS
    %import common.LETTER
    %import common.NUMBER
    %ignore WS
    start: i start* -> exp
    i: s -> exp_interm
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
    s: _l start? _r -> exp_par
        | "\\" _u "{{" start "}}" -> exp_unary
        | "\\" _b "{{" start "}}" "{{" start "}}" -> exp_binary
        | "\\" _latex1 -> symbol
        | "\\" _latex2 -> symbol
        | _c -> const
    !_c: /d[A-Za-z]/
        | NUMBER
        | LETTER
    !_l: {} // left parenthesis
    !_r: {} // right parenthesis
    !_b: {} // binary functions
    !_u: {} // unary functions
    !_latex1: {}
    !_latex2: {}
    QS: "\"" /(?<=").+(?=")/ "\"" // Quoted String
""".format(
    alias_string(left_parenthesis, alias=False),
    alias_string(right_parenthesis, alias=False),
    alias_string(binary_functions, alias=False),
    alias_string(unary_functions, alias=False),
    alias_string(dict(islice(smb.items(), len(smb) // 2)), alias=False),
    alias_string(
        dict(islice(smb.items(), len(smb) // 2, len(smb))), alias=False,
    ),
)
print(latex_grammar)