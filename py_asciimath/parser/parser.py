from lark import Lark

from ..transformer.transformer import LatexTransformer


class ASCIIMath2Tex(object):
    def __init__(
        self,
        grammar,
        *args,
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
            grammar, *args, parser=parser, lexer=lexer, **kwargs
        )

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)
