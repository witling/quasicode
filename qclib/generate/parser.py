from lark import Lark
from lark.indenter import Indenter

class QuasiIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR']
    CLOSE_PAREN_types = ['RPAR']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

class Parser:
    def __init__(self):
        kwargs = dict(postlex=QuasiIndenter(), start='start')

        self._lark = Lark(self._get_grammar(), parser='lalr', **kwargs)

    def _get_grammar(self):
        import os
        fname = os.path.join(os.path.dirname(__file__), 'grammar.lark')
        
        lark_grammar = None
        with open(fname, 'r') as fin:
            lark_grammar = fin.read()

        return lark_grammar

    def parse(self, content: str) -> list:
        # append one newline as I'm not able to fix that parser :-)
        content += '\n'
        result = self._lark.parse(content)
        return result
