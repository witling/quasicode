from program import Program

class Lexer:
    KEYWORDS = [
            'action please', # main method
            'uzbl', 'nuzbl', # True / False
            'quasi',    # output value
            'passt so', # rounding nums: <value> passt so 
            'und',      # logical and; concatenate strings (?)
            'oder',     # logical or
            'so',       # speed up program
            'also',     # right hand assignment <val> = <ident>
            'stark',    # declare a constant
            'ist',      # left hand assignment <ident> = <val>
            'das ist',  # comparison
            'im quadrat', # square something
            'und zwar',  # function declaration: und zwar <ident> mit <ident1>
            'und fertig',  # return from a function: <value> und fertig
            'das holen wir nach', # repeat last statement
            'jens',     # exit program
            'kris?',    # if
            'kris??',   # else if
            'patrick!', # break
            'softwareproblem', 'fähler', # raise error
            'oettinger' # keine ahnung
        ]
    LEX_KEYWORD = 0
    LEX_NUMBER = 1
    LEX_STRING = 2
    LEX_IDENT = 3

    def lex(self, line: str):
        lexed = []
        for lexem in line.split(' '):
            lexem = lexem.lower()

            if lexem == '':
                continue

            if lexem in self.KEYWORDS:
                lexed.append((self.LEX_KEYWORD, lexem))
            elif lexem.isnumeric():
                lexed.append((self.LEX_NUMBER, lexem))
            else:
                lexed.append((self.LEX_IDENT, lexem))
        return lexed

class Parser:
    def __init__(self):
        self._lexer = Lexer()
        self._program = Program()

    def parse_line(self, line):
        for token in line:
            if token[0] == Lexer.LEX_IDENT:
                after = next(line)
                if after[0] == Lexer.LEX_KEYWORD and after[1] == 'ist':
                    self._program.ident(token[1], list(line))
                    return

    def parse(self, content: str) -> Program:
        lexed = (self._lexer.lex(line) for line in content.split('\n'))

        for line in lexed:
            self.parse_line(iter(line))

        return self._program
