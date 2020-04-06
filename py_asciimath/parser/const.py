from itertools import islice

binary_functions = {
    '"frac"': "\\frac",
    '"root"': "\\sqrt",
    '"stackrel"': "\\stackrel",
    '"overset"': "\\overset",
    '"underset"': "\\underset",
    '"color"': "\\textcolor",
}

unary_functions = {
    '"sqrt"': "\\sqrt",
    '"text"': "\\textrm",
    '"abs"': "abs",
    '"floor"': "floor",
    '"ceil"': "ceil",
    '"norm"': "norm",
    '"ubrace"': "\\underbrace",
    '"underbrace"': "\\underbrace",
    '"obrace"': "\\overbrace",
    '"overbrace"': "\\overbrace",
    '"cancel"': "\\cancel",
    '"bb"': "\\boldsymbol",
    '"bbb"': "\\mathbb",
    '"cc"': "\\mathcal",
    '"tt"': "\\texttt",
    '"fr"': "\\mathfrak",
    '"sf"': "\\textsf",
    '"ul"': "\\underline",
    '"underline"': "\\underline",
    '"bar"': "\\overline",
    '"overline"': "\\overline",
    '"hat"': "\\hat",
    '"vec"': "\\vec",
    '"dot"': "\\dot",
    '"ddot"': "\\ddot",
}

operation_symbols = {
    '"+"': "+",
    '"*"': "\\cdot",
    '"-"': "-",
    '"cdot"': "\\cdot",
    '"**"': "\\ast",
    '"ast"': "\\ast",
    '"***"': "\\star",
    '"star"': "\\star",
    '"//"': "/",
    '"\\\\"': "\\setminus",
    '"setminus"': "\\setminus",
    '"xx"': "\\times",
    '"times"': "\\times",
    '"-:"': "\\div",
    '"div"': "\\div",
    '"|><"': "\\ltimes",
    '"ltimes"': "\\ltimes",
    '"><|"': "\\rtimes",
    '"rtimes"': "\\rtimes",
    '"|><|"': "\\bowtie",
    '"bowtie"': "\\bowtie",
    '"@"': "\\circ",
    '"circ"': "\\circ",
    '"o+"': "\\oplus",
    '"oplus"': "\\oplus",
    '"ox"': "\\otimes",
    '"otimes"': "\\otimes",
    '"o."': "\\odot",
    '"odot"': "\\odot",
    '"sum"': "\\sum",
    '"prod"': "\\prod",
    '"^^"': "\\wedge",
    '"wedge"': "\\wedge",
    '"^^^"': "\\bigwedge",
    '"bidwedge"': "\\bidwedge",
    '"vv"': "\\vee",
    '"vee"': "\\vee",
    '"vvv"': "\\bigvee",
    '"bigvee"': "\\bigvee",
    '"nn"': "\\cap",
    '"cap"': "\\cap",
    '"nnn"': "\\bigcap",
    '"bigcap"': "\\bigcap",
    '"uu"': "\\cup",
    '"cup"': "\\cup",
    '"uuu"': "\\bigcup",
    '"bigcup"': "\\bigcup",
}

logical_symbols = {
    '"and"': "\\text{and}",
    '"or"': "\\text{and}",
    '"not"': "\\neg",
    '"neg"': "\\neg",
    '"=>"': "\\implies",
    '"implies"': "\\implies",
    '"if"': "\\text{if}",
    '"<=>"': "\\iff",
    '"iff"': "\\iff",
    '"AA"': "\\forall",
    '"forall"': "\\forall",
    '"EE"': "\\exists",
    '"exists"': "\\exists",
    '"_|_"': "\\bot",
    '"bot"': "\\bot",
    '"TT"': "\\top",
    '"top"': "\\top",
    '"|--"': "\\vdash",
    '"vdash"': "\\vdash",
    '"|=="': "\\models",
    '"models"': "\\models",
}

relation_symbols = {
    '"="': "=",
    '"!="': "\\ne",
    '"ne"': "\\ne",
    '"<"': "<",
    '"lt"': "<",
    '">"': ">",
    '"gt"': ">",
    '"<="': "\\le",
    '"le"': "\\le",
    '">="': "\\ge",
    '"ge"': "\\ge",
    '"-<"': "\\prec",
    '"prec"': "\\prec",
    '"-<="': "\\preceq",
    '"preceq"': "\\preceq",
    '">-"': "\\succ",
    '"succ"': "\\succ",
    '">-="': "\\succeq",
    '"succeq"': "\\succeq",
    '"in"': "\\in",
    '"!in"': "\\notin",
    '"notin"': "\\notin",
    '"sub"': "\\subset",
    '"subset"': "\\subset",
    '"sup"': "\\supset",
    '"supset"': "\\supset",
    '"sube"': "\\subseteq",
    '"subseteq"': "\\subseteq",
    '"supe"': "\\supseteq",
    '"supseteq"': "\\supseteq",
    '"-="': "\\equiv",
    '"equiv"': "\\equiv",
    '"~="': "\\cong",
    '"cong"': "\\cong",
    '"~~"': "\\approx",
    '"approx"': "\\approx",
    '"prop"': "\\propto",
    '"propto"': "\\propto",
}

function_symbols = {
    '"sin"': "\\sin",
    '"cos"': "\\cos",
    '"tan"': "\\tan",
    '"sec"': "\\sec",
    '"csc"': "\\csc",
    '"cot"': "\\cot",
    '"arcsin"': "\\arcsin",
    '"arccos"': "\\arccos",
    '"arctan"': "\\arctan",
    '"sinh"': "\\sinh",
    '"cosh"': "\\cosh",
    '"tanh"': "\\tanh",
    '"sech"': "\\sech",
    '"csch"': "\\csch",
    '"coth"': "\\coth",
    '"exp"': "\\exp",
    '"log"': "\\log",
    '"ln"': "\\ln",
    '"det"': "\\det",
    '"dim"': "\\dim",
    '"mod"': "\\mod",
    '"gcd"': "\\gcd",
    '"lcm"': "\\lcm",
    '"lub"': "\\lub",
    '"glb"': "\\glb",
    '"min"': "\\min",
    '"max"': "\\max",
    '"lim"': "\\lim",
    '"dstyle"': "\\displaystyle",
    '"f"': "f",
    '"g"': "g",
}

greek_letters = {
    '"alpha"': "\\alpha",
    '"beta"': "\\beta",
    '"gamma"': "\\gamma",
    '"Gamma"': "\\Gamma",
    '"delta"': "\\delta",
    '"Delta"': "\\Delta",
    '"epsilon"': "\\epsilon",
    '"varepsilon"': "\\varepsilon",
    '"zeta"': "\\zeta",
    '"eta"': "\\eta",
    '"theta"': "\\theta",
    '"Theta"': "\\Theta",
    '"vartheta"': "\\vartheta",
    '"iota"': "\\iota",
    '"kappa"': "\\kappa",
    '"lambda"': "\\lambda",
    '"Lambda"': "\\Lambda",
    '"mu"': "\\mu",
    '"nu"': "\\nu",
    '"xi"': "\\xi",
    '"Xi"': "\\Xi",
    '"pi"': "\\pi",
    '"Pi"': "\\Pi",
    '"rho"': "\\rho",
    '"sigma"': "\\sigma",
    '"Sigma"': "\\Sigma",
    '"tau"': "\\tau",
    '"upsilon"': "\\upsilon",
    '"phi"': "\\phi",
    '"Phi"': "\\Phi",
    '"varphi"': "\\varphi",
    '"chi"': "\\chi",
    '"psi"': "\\psi",
    '"Psi"': "\\Psi",
    '"omega"': "\\omega",
    '"Omega"': "\\Omega",
}

left_parenthesis = {
    '"(:"': "\\langle",
    '"("': "(",
    '"["': "[",
    '"{:"': "{:",
    '"{"': "\\{",
    '"|:"': "\\vert",
    '"||:"': "\\lVert",
    '"langle"': "\\langle",
    '"<<"': "\\langle",
}

right_parenthesis = {
    '":)"': "\\rangle",
    '")"': ")",
    '"]"': "]",
    '":}"': ":}",
    '"}"': "\\}",
    '":|"': "\\vert",
    '":||"': "\\rVert",
    '"rangle"': "\\rangle",
    '">>"': "\\rangle",
}

arrows = {
    '"uarr"': "\\uparrow",
    '"uparrow"': "\\uparrow",
    '"darr"': "\\downarrow",
    '"downarrow"': "\\downarrow",
    '"rarr"': "\\rightarrow",
    '"rArr"': "\\Rightarrow",
    '"rightarrow"': "\\rightarrow",
    '"->"': "\\to",
    '"to"': "\\to",
    '">->"': "\\rightarrowtail",
    '"rightarrowtail"': "\\rightarrowtail",
    '"->>"': "\\twoheadrightarrow",
    '"twoheadrightarrow"': "\\twoheadrightarrow",
    '">->>"': "\\twoheadrightarrowtail",
    '"twoheadrightarrowtail"': "\\twoheadrightarrowtail",
    '"|->"': "\\mapsto",
    '"mapsto"': "\\mapsto",
    '"larr"': "\\leftarrow",
    '"leftarrow"': "\\leftarrow",
    '"harr"': "\\leftrightarrow",
    '"leftrightarrow"': "\\leftrightarrow",
    '"lArr"': "\\Leftarrow",
    '"Leftarrow"': "\\Leftarrow",
    '"hArr"': "\\Leftrightarrow",
    '"Leftrightarrow"': "\\Leftrightarrow",
}

misc_symbols = {
    '"^"': "^",
    '","': ",",
    '"_"': "_",
    '"\'"': "'",
    '"/"': "/",
    '"|"': "|",
    '":"': ":",
    '"int"': "\\int",
    '"integral"': "\\int",
    '"oint"': "\\oint",
    '"del"': "\\partial",
    '"partial"': "\\partial",
    '"grad"': "\\nable",
    '"nabla"': "\\nabla",
    '"+-"': "\\pm",
    '"pm"': "\\pm",
    '"O/"': "\\emptyset",
    '"emptyset"': "\\emptyset",
    '"oo"': "\\infty",
    '"infty"': "\\infty",
    '"aleph"': "\\aleph",
    '":."': "\\therefore",
    '"therefore"': "\\therefore",
    '":\'"': "\\because",
    '"because"': "\\because",
    '"..."': "\\ldots",
    '"ldots"': "\\ldots",
    '"cdots"': "\\cdots",
    '"vdots"': "\\vdots",
    '"ddots"': "\\ddots",
    '"quad"': "\\quad",
    '"/_"': "\\angle",
    '"angle"': "\\angle",
    '"frown"': "\\frown",
    '"/_\\\\"': "\\triangle",
    '"triangle"': "\\triangle",
    '"diamond"': "\\diamond",
    '"square"': "\\square",
    '"|__"': "\\lfloor",
    '"lfloor"': "\\lfloor",
    '"__|"': "\\rfloor",
    '"rfloor"': "\\rfloor",
    '"|~"': "\\lceiling",
    '"lceiling"': "\\lceiling",
    '"~|"': "\\rceiling",
    '"rceiling"': "\\rceiling",
    '"CC"': "\\mathbb{C}",
    '"NN"': "\\mathbb{N}",
    '"QQ"': "\\mathbb{Q}",
    '"RR"': "\\mathbb{R}",
    '"ZZ"': "\\mathbb{Z}",
}

matrix2par = {
    "pmatrix": ["(", ")"],
    "bmatrix": ["[", "]"],
    "Bmatrix": ["\{", "\}"],
    "vmatrix": ["|", "|"],
    "Vmatrix": ["||", "||"],
}


def alias_string(mapping: dict, init=False, alias=True, prefix=""):
    mapping = list(mapping.items())
    s = (
        "|"
        if init
        else ""
        + mapping[0][0]
        + (
            " -> " + (prefix + "_" if prefix != "" else "") + mapping[0][1]
            if alias
            else ""
        )
    )
    for k, v in mapping[1:]:
        s = (
            s
            + "\n\t| "
            + k
            + (
                " -> " + (prefix + "_" if prefix != "" else "") + v
                if alias
                else ""
            )
        )
    return s


smb = misc_symbols
smb.update(function_symbols)
smb.update(relation_symbols)
smb.update(logical_symbols)
smb.update(operation_symbols)
smb.update(greek_letters)
smb.update(arrows)
smb = dict(sorted(smb.items(), key=lambda x: (-len(x[0]), x[0])))

asciimath_grammar = r"""
    %import common.WS
    %import common.LETTER
    %import common.NUMBER
    %ignore WS
    start: i start* -> exp
    i: s -> exp_interm
        | s "/" s -> exp_frac
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
    s: _l start? _r -> exp_par
        | _u s -> exp_unary
        | _b s s -> exp_binary
        | _latex -> symbol
        | _c -> const
        | QS -> q_str
    !_c: /d[A-Za-z]/
        | NUMBER
        | LETTER
    !_l: {} // left parenthesis
    !_r: {} // right parenthesis
    !_b: {} // binary functions
    !_u: {} // unary functions
    !_latex: {}
    QS: "\"" /(?<=").+(?=")/ "\"" // Quoted String
""".format(
    alias_string(left_parenthesis, alias=False),
    alias_string(right_parenthesis, alias=False),
    alias_string(binary_functions, alias=False),
    alias_string(unary_functions, alias=False),
    alias_string(smb, alias=False),
)
