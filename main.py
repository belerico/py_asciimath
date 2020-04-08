from py_asciimath.parser.parser import ASCIIMath2MathML
# from py_asciimath.transformer.transformer import MathmlTransformer
from py_asciimath.grammar.asciimath_grammar import asciimath_grammar

if __name__ == "__main__":
    parser = ASCIIMath2MathML(
        asciimath_grammar, inplace=False
    )
    text = ""
    # text = (
    #     text
    #     + """
    #     frac{root(5)(a iff c)}
    #     {
    #         dstyle int(
    #             sqrt(x_2^3.14)
    #             X
    #             root(langle x,t rangle) (max(dot z,4)) +
    #             min(x,y,"time",bbb C)
    #         ) dg
    #     }
    # """
    # )
    # text = (
    #     text
    #     + """
    #     uuu_{2(x+1)=1)^{n}
    #     min{
    #             2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i
    #             rarr Omega < b, 5=x
    #     }
    # """
    # )
    # text = (
    #     text
    #     + """
    #     [[:[1,2]:]]
    # """
    # )
    # text = text + """lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx"""
    # text = text + """||:[2 x + 17 y = 23],[y = int_{0}^{x} t dt]:||"""
    # text = (
    #     text
    #     + """
    #         floor frac "Time" (A nn (bbb(N) | f'(x) = dx/dy | |><|><|
    #         (D setminus (B uu C))))
    #     """
    # )
    # text = text + """(1,2,3)"""
    # # System of equation
    # text = (
    #     text
    #     + """
    #         e^{:
    #             [2 x + 17 (y) = 23],
    #             [1],
    #             [y = dstyle int_{0}^{x} t dt],
    #             [y = dstyle integral_{0}^{x} t dt]
    #         :}"""
    # )
    text = text + """(a_2^3+b^2) * 2"""
    # text = text + "[(1,2), (2^|: 3 :|, (dstyle int x^{2(x-n)})), (2,4)]"
    # text = text + "[[], []]"
    print(parser.translate(text, pprint=True))
