import ply.lex as lex
from ply.lex import TOKEN
import re

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'while': 'WHILE',
    'begin': 'BEGIN',
    'end': 'END',
    'var': 'VAR',
    'do': 'DO',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'integer': 'INT',
    'real': 'REAL',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'div': 'DIV',
    'mod': 'MOD',
    'write': 'WRITE',
    'read': 'READ',
    'string': 'STRI',
    'program': 'PROGRAM',
    'function': 'FUNCTION',
    'procedure': 'PROCEDURE'
}
states = (
    ('string', 'exclusive'),
)

tokens = [
             'ASSIGN', 'EQUAL',
             'STRING', 'COLON', 'COMA',
             'OPEN', 'CLOSE', 'NUM', 'PLUSMINUS',
             'MULTIPLE', 'STR', 'SEMICOLON', 'ID', 'COMPARE', 'DOT', 'REALNUM', 'DIVIDE'
         ] + list(reserved.values())


ident = r'[a-z]\w*'

t_DIVIDE = r'\/'
t_DOT = r'\.'
t_COMPARE = r'\>\=|\<\=|\>|\<|\<\>'
t_EQUAL = r'\='
t_COLON = r'\:'
t_ASSIGN = r'\:='
t_SEMICOLON = r';'
t_COMA = r','
t_OPEN = r'\('
t_CLOSE = r'\)'
t_NUM = r'\d+'
t_PLUSMINUS = r'\+|\-'
t_MULTIPLE = r'\*'
t_REALNUM = r'\d+\.\d+'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_comment(t):
    r'(\{(.|\n)*?\})|(//.*)'
    pass

def t_ANY_STRING(t):
    r'"'
    if t.lexer.current_state() == 'string':
        t.lexer.begin('INITIAL')
    else:
        t.lexer.begin('string')
    return t

t_string_STR = r'(\\.|[^$"])+'

t_string_ignore = ''

def t_string_error(t):
    print("Syntax error. Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \r\t\f'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Syntax error. Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE | re.DOTALL | re.IGNORECASE)

if __name__ == "__main__":
    data = '''
    program Hello;
    var a,b,c : integer
    var d : real

    begin
        while (a < 5) do begin
        a := a + 1;
        write(a)
        end
    end.
    '''

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok: break
        print(tok)