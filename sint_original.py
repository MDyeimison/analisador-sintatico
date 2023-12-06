from lex import Lex
import rules
import copy

class Parser:
    def __init__(self, lexer, token_list, buffer=0):
        self.lexer = lexer
        self.buffer = buffer
        self.token_list = token_list
    
    def current_token(self):
        return self.token_list[self.buffer]
    
    def parse_program(self):
        print(f'parse_program: {self.current_token()}')
        if self.parse_block():
            return self.current_token().token_value == '.'
        return False
    
    def parse_block(self):
        print(f'parse_block: {self.current_token()}')
        count = 0
        initial_index = copy.deepcopy(self.buffer)
        if self.current_token().token_value == 'CONST':
            if not self.token_list[0].token_value == 'CONST':
                return False
            self.buffer+=1
            if not self.parse_constants():
                return False
            count+=1

        if self.current_token().token_value == 'VAR':
            if not self.parse_variables():
                return False
            count+=1

        if self.current_token().token_value == 'PROCEDURE':
            if not self.parse_procedures():
                return False
            count+=1
        
        if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
            if not self.parse_statement():
                return False
            count+=1

        if (count == 0 and self.buffer == initial_index) or count >= 0:
            return True
        return False
    
    def parse_variables(self):
        print(f'1 parse_variables: {self.current_token()}')
        if (self.current_token().token_value == 'VAR'):
            self.buffer+=1
            print(f'2 parse_variables: {self.current_token()}')
            if self.parse_vardecl():
                print(f'3 parse_variables: {self.current_token()}')
                if self.current_token().token_value == ';':
                    self.buffer+=1
                    print(f'4 parse_variables: {self.current_token()}')
                    return True
        return False
    
    def parse_vardecl(self):
        print(f'1 parse_vardecl: {self.current_token()}')
        if self.current_token().token_class.name == 'IDENTIFIER':
            self.buffer+=1
            print(f'2 parse_vardecl: {self.current_token()}')
            if self.current_token().token_value == ',':
                self.buffer+=1
                print(f'3 parse_vardecl: {self.current_token()}')
                if not self.parse_vardecl():
                    return False
                print(f'4 parse_vardecl: {self.current_token()}')
            return True
        return False

    def parse_statement(self):
        if self.current_token().token_class.name == 'IDENTIFIER':
            print(f'1 parse_statement IDENTIFIER: {self.current_token()}')
            self.buffer+=1
            print(f'2 parse_statement IDENTIFIER: {self.current_token()}')
            if self.current_token().token_value == '<-':
                self.buffer+=1
                print(f'3 parse_statement IDENTIFIER: {self.current_token()}')
                if self.parse_expression():
                    print(f'4 parse_statement IDENTIFIER: {self.current_token()}')
                    return True
            return False

        if self.current_token().token_value == 'CALL':
            self.buffer+=1
            if self.current_token().token_class.name == 'IDENTIFIER':
                self.buffer+=1
                return True
            return False
            
        if self.current_token().token_value == 'BEGIN':
            print(f'1 parse_statement BEGIN: {self.current_token()}')
            self.buffer+=1
            if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
                print(f'2 parse_statement BEGIN: {self.current_token()}')
                if not self.parse_compound_statement():
                    return False
            if self.current_token().token_value == 'END':
                print(f'3 parse_statement BEGIN: {self.current_token()}')
                self.buffer+=1
                print(f'4 parse_statement BEGIN: {self.current_token()}')
                return True
            return False

        if self.current_token().token_value == 'IF':
            self.buffer+=1
            if self.current_token().token_value == 'NOT':
                self.buffer+=1
            if self.parse_condition():
                if self.current_token().token_value == 'THEN':
                    self.buffer+=1
                    if self.parse_statement():
                        return True
            return False

        if self.current_token().token_value == 'WHILE':
            self.buffer+=1
            if self.current_token().token_value == 'NOT':
                self.buffer+=1
            if self.parse_condition():
                if self.current_token().token_value == 'DO':
                    self.buffer+=1
                    if self.parse_statement():
                        return True
            return False

        if self.current_token().token_value == 'PRINT':
            self.buffer+=1
            if self.parse_expression():
                return True
            return False
    
    def parse_procedures(self):
        print(f'1 parse_procedures: {self.current_token()}')
        if self.parse_procdecl():
            print(f'2 cai prodecl: {self.current_token()}')
            if self.current_token().token_value == 'PROCEDURE':
                if self.parse_procedures():
                    print(f'3 cai procedures: {self.current_token()}')
                    return True
            return True
        return False

    def parse_procdecl(self):
        print(f'1 parse_procdecl: {self.current_token()}')
        if self.current_token().token_value == 'PROCEDURE':
            self.buffer+=1
            print(f'2 parse_procdecl: {self.current_token()}')
            if self.current_token().token_class.name == 'IDENTIFIER':
                self.buffer+=1
                print(f'3 parse_procdecl: {self.current_token()}')
                if self.current_token().token_value == ';':
                    self.buffer+=1
                    print(f'4 parse_procdecl: {self.current_token()}')
                    if self.parse_block():
                        print(f'5 parse_procdecl: {self.current_token()}')
                        if self.current_token().token_value == ';':
                            self.buffer+=1
                            print(f'6 parse_procdecl: {self.current_token()}')
                            return True
                        print(f'\033[91m\nERROR IN PARSE_PROCDECL: {self.current_token()}\033[0m')
                    print(f'\033[91m\nERROR IN PARSE_PROCDECL: {self.current_token()}\033[0m')
        return False
    
    def parse_compound_statement(self):
        print(f'1 parse_compound_statement: {self.current_token()}')
        if self.parse_statement():
            print(f'2 parse_compound_statement: {self.current_token()}')
            if self.current_token().token_value == ';':
                print(f'3 parse_compound_statement: {self.current_token()}')
                self.buffer+=1
                if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
                    print(f'4 parse_compound_statement: {self.current_token()}')
                    if not self.parse_compound_statement():
                        return False
                return True
        return False
    
    def parse_expression(self):
        print(f'1 parse_expression: {self.current_token()}')
        if self.current_token().token_class.name == 'SIGN':
            if not self.parse_sign(self):
                return False
        print(f'2 parse_expression: {self.current_token()}')
        if self.parse_term():
            print(f'3 parse_expression: {self.current_token()}')
            if self.current_token().token_class.name == 'SIGN':
                print(f'4 parse_expression: {self.current_token()}')
                if not self.parse_terms():
                    return False
                print(f'5 parse_expression: {self.current_token()}')
            return True
        return False
        
    def parse_sign(self):
        print(f'1 parse_sign: {self.current_token()}')
        if self.current_token().token_class.name == 'SIGN':
            self.buffer+=1
            print(f'2 parse_sign: {self.current_token()}')
            return True
        return False
    
    def parse_term(self):
        print(f'1 parse_term: {self.token_list[self.buffer]}')
        if self.parse_factor():
            print(f'2 parse_term: {self.token_list[self.buffer]}')
            if self.current_token().token_value in ['*','/']:
                if not self.parse_factors():
                    return False
                print(f'3 parse_term: {self.token_list[self.buffer]}')
            return True
        return False
    
    def parse_terms(self):
        print(f'1 parse_terms: {self.current_token()}')
        if self.current_token().token_class.name == 'SIGN':
            self.buffer+=1
            print(f'2 parse_terms: {self.current_token()}')
            if self.parse_term():
                print(f'3 parse_terms: {self.current_token()}')
                return True
        return False
    
    def parse_factor(self):
        print(f'1 parse_factor: {self.current_token()}')
        if self.current_token().token_class.name in ['IDENTIFIER','NUMBER']:
            self.buffer+=1
            return True
        print(f'2 parse_factor: {self.current_token()}')
        if self.current_token().token_value == '(':
            self.buffer+=1
            print(f'3 parse_factor: {self.current_token()}')
            if self.parse_expression():
                print(f'4 parse_factor: {self.current_token()}')
                if self.current_token().token_value == ')':
                    self.buffer+=1
                    print(f'5 parse_factor: {self.current_token()}')
                    return True
        return False
    
    def parse_factors(self):
        print(f'1 parse_factors: {self.current_token()}')
        if self.current_token().token_value in ['/','*']:
            self.buffer+=1
            print(f'2 parse_factors: {self.current_token()}')
            if self.parse_factor():
                print(f'3 parse_factors: {self.current_token()}')
                return True
        return False
    
    def parse_condition(self):
        print(f'parse_condition: {self.current_token()}')
        if self.current_token().token_value in ['ODD','EVEN']:
            self.buffer+=1
            if self.parse_expression():
                return True
            return False
        if self.parse_expression():
            if self.parse_relation():
                if self.parse_expression():
                    return True
        return False
    
    def parse_relation(self):
        print(f'1 parse_relation: {self.current_token()}')
        if self.current_token().token_class.name == 'RELATION':
            self.buffer+=1
            print(f'2 parse_relation: {self.current_token()}')
            return True
        return False

    def parse_constants(self):
        print(f'1 parse_constants: {self.current_token()}')
        if self.parse_constdecl():
            print(f'2 parse_constants: {self.current_token()}')
            if self.current_token().token_value == ';':
                self.buffer+=1
                print(f'3 parse_constants: {self.current_token()}')
                return True
        return False

    def parse_constdecl(self):
        print(f'1 parse_constdecl: {self.current_token()}')
        if self.parse_constdef():
            print(f'2 parse_constdecl: {self.current_token()}')
            if self.current_token().token_value == ',':
                self.buffer+=1
                print(f'3 parse_constdecl: {self.current_token()}')
                if not self.parse_constdecl():
                    return False
                print(f'4 parse_constdecl: {self.current_token()}')
            return True
        
    def parse_constdef(self):
        print(f'1 parse_constdef: {self.current_token()}')
        if (self.current_token().token_class.name == 'IDENTIFIER'):
            self.buffer+=1
            print(f'2 parse_constdef: {self.current_token()}')
            if (self.current_token().token_value == '='):
                self.buffer+=1
                print(f'3 parse_constdef: {self.current_token()}')
                if (self.current_token().token_class.name == 'NUMBER'):
                    self.buffer+=1
                    print(f'4 parse_constdef: {self.current_token()}')
                    return True
        return False
    


diretorio = './arquivos/'
with open('./testes/' + 'ex2.pl0mod.txt', 'r') as arquivo:
    content = arquivo.read()

lex = Lex(content, [ \
    rules.CommentRule(), \
    rules.SignRule(), \
    rules.KeywordRule(), \
    rules.NumberRule(), \
    rules.StatementRule(), \
    rules.SymbolRule(), \
    rules.RelationRule(), \
    rules.FactorsRule(), \
    rules.ReservedWordsRule(), \
    rules.IdentifierRule(), \
    ])

token_list = []
while True:
  token_atual = lex.next()
  if token_atual is None:
    break
  if not token_atual.token_class.name == 'COMMENT':
    token_list.append(token_atual)
  else:
      print(f'\033[91m', token_atual ,'\033[0m')
[print(e) for e in token_list if e != None]
print(f"\n\n###############################################\n\n")
parser = Parser(lex, token_list)
if parser.parse_program():
    print("\n:)")
else:
    print(f"\033[91m\nSOMETHING WENT WHONG\033[0m")