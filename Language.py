from ply.lex import lex
from ply.yacc import yacc
from colorama import Fore

# empty_character = ''
empty_character = ' '


class Language(object):
    tokens = ('NEG', 'AND', 'OR', 'IF', 'IFF', 'LPAREN', 'RPAREN', 'VARIABLE', 'CONSTANT')
    t_ignore = ' \t'
    t_NEG = r'~'
    t_AND = r'\^'
    t_OR = r'o'
    t_IF = r'=>'
    t_IFF = r'<=>'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_VARIABLE = r'[pqrstuvwxyz]'
    precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'IF', 'IFF'),
        ('nonassoc', 'NEG'),
        )


    def __init__(self, graph=False, memory=False):
        self.tokens = ('NEG', 'AND', 'OR', 'IF', 'IFF', 'LPAREN', 'RPAREN', 'VARIABLE', 'CONSTANT')

        self.nodes = [] if graph else None
        self.edges = [] if graph else None
        self.memory = memory or {'p': 0,
                                        'q': 1,
                                        'r': 1,
                                        's': 0,
                                        't': 1,
                                        'v': 0,
                                        'w': 0,
                                        'x': 0,
                                        'y': 0,
                                        'z': 0}
        self.lexer = lex(module=self)
        self.parser = yacc(module=self)


    def generate_node(self, node):
        if self.nodes is None:
            return None

        node = str(node)
        while node in self.nodes:
            node = empty_character + node
        self.nodes.append(node)
        return node


    def add_edges(self, *edges):
        if self.edges is None:
            return None
        self.edges += edges

    def t_CONSTANT(self, t):
        '[01]'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        # print(Fore.RED + 'Invalid Token:', t.value, Fore.RESET)
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def p_constant2expr(self, p):
        """expr : CONSTANT"""
        constant = p[1]
        p[0] = constant, self.generate_node(constant)

    def p_variable2expr(self, p):
        """expr : VARIABLE"""
        variable = p[1]
        p[0] = self.memory[variable] or 0, self.generate_node(variable)

    def p_neg(self, p):
        """expr : NEG expr"""
        value, node = p[2]
        self_node = self.generate_node('~')
        self.add_edges((self_node, node))
        p[0] = int(not value), self_node

    def p_and(self, p):
        """expr : expr AND expr"""
        first_value, first_node = p[1]
        second_value, second_node = p[3]
        self_node = self.generate_node('^')
        self.add_edges((self_node, first_node), (self_node, second_node))
        p[0] = int(first_value and second_value), self_node

    def p_or(self, p):
        """expr : expr OR expr"""
        first_value, first_node = p[1]
        second_value, second_node = p[3]
        self_node = self.generate_node('o')
        self.add_edges((self_node, first_node), (self_node, second_node))
        p[0] = int(first_value or second_value), self_node

    def p_if(self, p):
        """expr : expr IF expr"""
        first_value, first_node = p[1]
        second_value, second_node = p[3]
        self_node = self.generate_node('=>')
        self.add_edges((self_node, first_node), (self_node, second_node))
        p[0] = int(not first_value or second_value), self_node

    def p_iff(self, p):
        """expr : expr IFF expr"""
        first_value, first_node = p[1]
        second_value, second_node = p[3]
        self_node = self.generate_node('<=>')
        self.add_edges((self_node, first_node), (self_node, second_node))
        p[0] = int(first_value == second_value), self_node

    def p_parens(self, p):
        """expr : LPAREN expr RPAREN"""
        value, node = p[2]
        self_node = self.generate_node('()')
        self.add_edges((self_node, node))
        p[0] = value, self_node

    def p_error(self, p):
        if p is not None:
            print(Fore.RED + 'Syntax Error', p, Fore.RESET)

    def parse(self, args):
        answer = self.parser.parse(args)
        if self.edges is not None:
            graph = self.nodes, self.edges
            self.nodes = []
            self.edges = []
            if len(answer) > 1:
                return answer[0], graph
            else:
                return answer, graph
        else:
            if len(answer) > 1:
                return answer[0]
            else:
                return answer

    def get_graph(self):
        return self.nodes, self.edges