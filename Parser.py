from Lexer import tokens
import ply.yacc as yacc
import ply.lex as lex

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

    scope = 'global'


def p_program(p):
    '''program : PROGRAM ID SEMICOLON declarations subDeclarations comStatement DOT'''
    p[0] = Node('Program', [p[4], p[5], p[6]])


def p_declarations(p):
    '''declarations :
                    | declarations VAR identifierList COLON type'''
    if len(p) == 1:
        p[0] = Node('Var', [], )
    else:
        p[0] = p[1].add_parts([p[3], p[5]])


def p_identifierList(p):
    '''identifierList : ID
                        | identifierList COMA ID'''
    if len(p) == 2:
        p[0] = Node('ID', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_type(p):
    '''type : INT
            | REAL
            | STRI'''
    if len(p) == 2:
        p[0] = Node('Type', [p[1]])


def p_subDeclarations(p):
    '''subDeclarations :
                        | subDeclarations subDeclaration SEMICOLON'''
    if len(p) == 1:
        p[0] = Node('SubDeclare', [])
    else:
        p[0] = p[1].add_parts([p[2]])


def p_subDeclaration(p):
    '''subDeclaration : subHead declarations comStatement'''
    p[0] = Node('SubDeclaration', [p[1], p[2], p[3]])
    p[2].scope = p[1].scope


def p_subHead(p):
    '''subHead : FUNCTION ID args COLON type SEMICOLON
                | PROCEDURE ID args SEMICOLON '''
    if len(p) == 7:
        p[0] = Node(p[1] + ' ' + p[2], [p[3], p[5]])
    else:
        p[0] = Node(p[1] + ' ' + p[2], [p[3]])
    scope = p[2]
    p[3].scope = p[2]
    p[0].scope = p[2]


def p_args(p):
    '''args :
            | OPEN paramList CLOSE'''
    if len(p) == 1:
        p[0] = Node('Ar', [])
    else:
        p[0] = p[2]
        p[2].scope = p[0].scope


def p_paramList(p):
    '''paramList : identifierList COLON type
                | paramList SEMICOLON identifierList COLON type'''
    if len(p) == 4:
        p[0] = Node('Arguments', [p[1], p[3]])
        p[1].scope = p[0].scope
    else:
        p[0] = p[1].add_parts([p[3], p[5]])
        p[3].scope = p[0].scope


def p_comStatement(p):
    '''comStatement : BEGIN optionalStatements END'''
    p[0] = Node('Compound statement', [p[2]])


def p_comStatementWBC(p):
    '''comStatementWBC : BEGIN optionalStatementsWBC END'''
    p[0] = Node('Compound statement', [p[2]])


def p_optionalStatements(p):
    '''optionalStatements :
                            | statementList'''
    if len(p) == 1:
        p[0] = Node('Optional statements', [])
    else:
        p[0] = Node('Optional statements', [p[1]])


def p_optionalStatementsWBC(p):
    '''optionalStatementsWBC :
                            | statementListWBC'''
    if len(p) == 1:
        p[0] = Node('Optional statements', [])
    else:
        p[0] = Node('Optional statements', [p[1]])


def p_statementList(p):
    '''statementList : statement
                    |  statementList SEMICOLON statement'''
    if len(p) == 2:
        p[0] = Node('Statement List', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_statementListWBC(p):
    '''statementListWBC : statementWBC
                    |  statementListWBC SEMICOLON statementWBC'''
    if len(p) == 2:
        p[0] = Node('Statement List', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_statement(p):
    '''statement : variable ASSIGN expression
                | WRITE OPEN string CLOSE
                | WRITE OPEN ID CLOSE
                | READ OPEN string CLOSE
                | ID OPEN expressionListProc CLOSE
                | comStatement
                | IF expression THEN comStatementWBC
                | WHILE expression DO statement'''
    if len(p) == 2:
        p[0] = Node('Statement', [p[1]])
    elif len(p) == 2:
        p[0] = Node('Call procedure', [p[1]])
    elif len(p) == 4:
        p[0] = Node('Assign', [p[1], p[3]])

    elif p[1] == 'if':
        p[0] = Node('If clause', [p[2], p[4]])
    elif p[1] == 'while':
        p[0] = Node('While clause', [p[2], p[4]])
    elif len(p) == 5 and p[1] != 'write':
        p[0] = Node('Call proc', [p[1], p[3]])
    elif len(p) == 5:
        p[0] = Node(p[1], [p[3]])


def p_statementWBC(p):
    '''statementWBC : statement
                    | brCon'''
    p[0] = Node('Statement', [p[1]])


def p_brCon(p):
    '''brCon : BREAK
            | CONTINUE'''
    p[0] = Node('BR', [p[1]])


def p_string(p):
    '''string : STRING STR STRING'''
    p[0] = Node('Strings', [p[2]])


def p_variable(p):
    '''variable : ID'''
    p[0] = Node('Variable', [p[1]])


def p_procedureStatement(p):
    '''expressionListProc :
                            | expressionList '''
    if len(p) == 1:
        p[0] = Node('Empty', [])
    else:
        p[0] = Node('Expressions', [p[1]])


def p_expressionList(p):
    '''expressionList : expression
                        | expressionList COMA expression'''
    if len(p) == 2:
        p[0] = Node('ExpressionList', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_expression(p):
    '''expression : simpleExpression
                    | simpleExpression COMPARE simpleExpression
                    | simpleExpression EQUAL simpleExpression
                    | simpleExpression AND simpleExpression
                    | simpleExpression OR simpleExpression'''
    if len(p) == 2:
        p[0] = Node('Expression', [p[1]])
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_simpleExpression(p):
    '''simpleExpression : term
                        | sign term
                        | simpleExpression PLUSMINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node('Sign', [p[1], p[2]])
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_term(p):
    '''term : factor
            | term MULTIPLE factor
            | term DIV factor
            | term MOD factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_factor(p):
    '''factor : ID
                | ID OPEN expressionList CLOSE
                | NUM
                | REALNUM
                | OPEN expression CLOSE
                | NOT factor'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node('Not', [p[2]])
    elif len(p) == 4:
        p[0] = Node('Expression in parentheses', [p[2]])
    else:
        p[0] = Node('Function', [p[1], p[3]])


def p_sign(p):
    '''sign : PLUSMINUS'''
    p[0] = p[1]


def p_error(p):
    print('Error at line', p.lineno-1)


parser = yacc.yacc()


def build_tree(code):
    return parser.parse(code)


def find(tree, tableOfValues):
    if (type(tree) != str):
        for part in tree.parts:

            if (type(part) != str):
                variable = []
                if (part.type.startswith('function')):
                    variable.append(part.parts[1].parts[0])
                    tableOfValues[part.type[9:]] = {}
                    tableOfValues[part.type[9:]][part.type[9:]] = variable

                if (part.type.startswith('procedure')):
                    tableOfValues[part.type[10:]] = {}

                if (part.type == 'Arguments'):
                    if (len(part.parts)) != 0:
                        for idvars in range(0, len(part.parts), 2):
                            if len(part.parts[idvars].parts) > 1:
                                id = part.parts[idvars]
                                for i in range(len(id.parts)):
                                    variable.append(part.parts[idvars + 1].parts[0])
                                    tableOfValues[part.scope][id.parts[i]] = variable
                                    variable = []

                            elif len(part.parts[idvars].parts) == 1:
                                variable.append(part.parts[idvars + 1].parts[0])
                                tableOfValues[part.scope][part.parts[idvars].parts[0]] = variable
                                variable = []
                if (part.type == 'Var'):
                    if (len(part.parts)) != 0:
                        for idvars in range(0, len(part.parts), 2):

                            if len(part.parts[idvars].parts) >= 1:
                                id = part.parts[idvars]
                                for i in range(len(id.parts)):
                                    variable.append(part.parts[idvars + 1].parts[0])
                                    tableOfValues[part.scope][id.parts[i]] = variable
                                    variable = []

                            elif len(part.parts[idvars].parts) == 1:
                                variable.append(part.parts[idvars].parts[0])
                                variable.append(part.parts[idvars + 1].parts[0])
                                variable.append(part.scope)
                                variable = []
            find(part, tableOfValues)


def getTable(code):
    tableOfValues = {}
    tableOfValues['global'] = {}
    find(code, tableOfValues)
    return tableOfValues


def main():
    data = '''
    program Program;
    var a,b : integer

    begin
        a := 5;
        write(b)
    end.
        '''

    print(build_tree(data))


if __name__ == '__main__':
    main()
