import lxml.etree

lxml_parser = lxml.etree.XMLParser(
    dtd_validation=True,
    no_network=True,
    load_dtd=True,
    ns_clean=False,
    remove_blank_text=True,
    resolve_entities=True,
)

transform = lxml.etree.parse(
    open("./py_asciimath/translation/mathml2tex/mmltex.xsl")
)
transform = lxml.etree.XSLT(transform)
doc = lxml.etree.fromstring(
    '<!DOCTYPE math SYSTEM "/home/belerico/Desktop/projects/py_asciimath/py_asciimath/dtd/mathml3/mathml3.dtd"><math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mo>[</mo><mtable><mtr><mtd><mo>&Integral;</mo><mi>x</mi><mi>dx</mi><mrow><mo>&langle;</mo><mrow><mo>&rarr;</mo></mrow><mo>&rangle;</mo></mrow></mtd></mtr><mtr><mtd><mo>log</mo><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mstyle></math>',
    lxml_parser,
)
print(transform(doc))