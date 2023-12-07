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
    
    def add_tab_to_newlines(self, s):
        return s.replace("\n", "\n\t")
    
    def parse_program(self):
        print(f'parse_program: {self.current_token()}')
        parse_block = self.parse_block()
        if parse_block:
            if self.current_token().token_value == '.':
                return f'{parse_block}'
        return False
    
    def parse_block(self):
        print(f'parse_block: {self.current_token()}')
        parse_block = ''
        count = 0
        initial_index = copy.deepcopy(self.buffer)
        if self.current_token().token_value == 'CONST':
            if not self.token_list[0].token_value == 'CONST':
                return False
            self.buffer+=1
            parse_constants = self.parse_constants()
            if not parse_constants:
                return False
            parse_block = f'{parse_constants}'
            count+=1

        if self.current_token().token_value == 'VAR':
            parse_variables = self.parse_variables()
            if not parse_variables:
                return False
            parse_block = f'{parse_block}\n{parse_variables}\n'
            count+=1

        if self.current_token().token_value == 'PROCEDURE':
            parse_procedures = self.parse_procedures()
            if not parse_procedures:
                return False
            parse_block = f'{parse_block}\n{parse_procedures}\n'
            count+=1
        
        if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
            parse_statement = self.parse_statement()
            if not parse_statement:
                return False
            parse_block = f'{parse_block}\n{parse_statement}\n'
            count+=1

        if (count == 0 and self.buffer == initial_index) or count >= 0:
            return f'{parse_block}'
        return False
    
    def parse_variables(self):
        print(f'1 parse_variables: {self.current_token()}')
        if (self.current_token().token_value == 'VAR'):
            self.buffer+=1
            print(f'2 parse_variables: {self.current_token()}')
            parse_vardecl = f'{self.parse_vardecl()}'
            if parse_vardecl:
                print(f'3 parse_variables: {self.current_token()}')
                if self.current_token().token_value == ';':
                    self.buffer+=1
                    print(f'4 parse_variables: {self.current_token()}')
                    return f'{parse_vardecl}'
        return False
    
    def parse_vardecl(self):
        print(f'1 parse_vardecl: {self.current_token()}')
        if self.current_token().token_class.name == 'IDENTIFIER':
            identifier = f'{self.current_token().token_value} = 0'
            self.buffer+=1
            print(f'2 parse_vardecl: {self.current_token()}')
            if self.current_token().token_value == ',':
                self.buffer+=1
                print(f'3 parse_vardecl: {self.current_token()}')
                parse_vardecl = self.parse_vardecl()
                if not parse_vardecl:
                    return False
                identifier = f'{identifier}; {parse_vardecl}'
                print(f'4 parse_vardecl: {self.current_token()}')
            return f'{identifier}'
        return False

    def parse_statement(self):
        if self.current_token().token_class.name == 'IDENTIFIER':
            identifier = self.current_token().token_value
            print(f'1 parse_statement IDENTIFIER: {self.current_token()}')
            self.buffer+=1
            print(f'2 parse_statement IDENTIFIER: {self.current_token()}')
            if self.current_token().token_value == '<-':
                self.buffer+=1
                print(f'3 parse_statement IDENTIFIER: {self.current_token()}')
                parse_expression = self.parse_expression()
                if parse_expression:
                    print(f'4 parse_statement IDENTIFIER: {self.current_token()}')
                    return f'{identifier} = {parse_expression}'
            return False

        if self.current_token().token_value == 'CALL':
            print(f'1 parse_statement CALL: {self.current_token()}')
            self.buffer+=1
            if self.current_token().token_class.name == 'IDENTIFIER':
                identifier = self.current_token().token_value
                print(f'2 parse_statement CALL: {self.current_token()}')
                self.buffer+=1
                print(f'3 parse_statement CALL: {self.current_token()}')
                return f'{identifier}()'
            return False
            
        if self.current_token().token_value == 'BEGIN':
            print(f'1 parse_statement BEGIN: {self.current_token()}')
            self.buffer+=1
            begin = ''
            if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
                print(f'2 parse_statement BEGIN: {self.current_token()}')
                begin = f'{self.parse_compound_statement()}'
                
            if self.current_token().token_value == 'END':
                print(f'3 parse_statement BEGIN: {self.current_token()}')
                self.buffer+=1
                print(f'4 parse_statement BEGIN: {self.current_token()}')
                return f'{begin}'
            return False

        if self.current_token().token_value == 'IF':
            if_statement = 'if'
            self.buffer+=1
            if self.current_token().token_value == 'NOT':
                if_statement = f'{if_statement} not'
                self.buffer+=1
            parse_condition = self.parse_condition()
            if parse_condition:
                if self.current_token().token_value == 'THEN':
                    self.buffer+=1
                    parse_statement = self.parse_statement()
                    if parse_statement:
                        result = self.add_tab_to_newlines(f'{if_statement} ({parse_condition}):\n{parse_statement}\n')
                        return result
            return False

        if self.current_token().token_value == 'WHILE':
            while_statement = 'while'
            self.buffer+=1
            if self.current_token().token_value == 'NOT':
                while_statement = f'{while_statement} not'
                self.buffer+=1
            parse_condition = self.parse_condition()
            if parse_condition:
                if self.current_token().token_value == 'DO':
                    self.buffer+=1
                    parse_statement = self.parse_statement()
                    if parse_statement:
                        result = self.add_tab_to_newlines(f'{while_statement} ({parse_condition}):\n{parse_statement}')
                        return result
            return False

        if self.current_token().token_value == 'PRINT':
            self.buffer+=1
            parse_expression = self.parse_expression()
            if parse_expression:
                result = self.add_tab_to_newlines(f'print({parse_expression})\n')
                return result
            return False
    
    def parse_procedures(self):
        print(f'1 parse_procedures: {self.current_token()}')
        parse_procdecl = self.parse_procdecl()
        if parse_procdecl:
            parse_procdecl = f'{parse_procdecl}\n'
            print(f'2 parse_procedures: {self.current_token()}')
            if self.current_token().token_value == 'PROCEDURE':
                parse_procedures_recall = self.parse_procedures()
                if not parse_procedures_recall:
                    print(f'3 parse_procedures: {self.current_token()}')
                    return False
                parse_procdecl = f'{parse_procdecl}{parse_procedures_recall}'
            result = self.add_tab_to_newlines(f'{parse_procdecl}')
            return result
            
        return False

    def parse_procdecl(self):
        print(f'1 parse_procdecl: {self.current_token()}')
        if self.current_token().token_value == 'PROCEDURE':
            self.buffer+=1
            print(f'2 parse_procdecl: {self.current_token()}')
            if self.current_token().token_class.name == 'IDENTIFIER':
                identifier = self.current_token().token_value
                self.buffer+=1
                print(f'3 parse_procdecl: {self.current_token()}')
                if self.current_token().token_value == ';':
                    self.buffer+=1
                    print(f'4 parse_procdecl: {self.current_token()}')
                    parse_block = self.parse_block()
                    if parse_block:
                        print(f'5 parse_procdecl: {self.current_token()}')
                        if self.current_token().token_value == ';':
                            self.buffer+=1
                            print(f'6 parse_procdecl: {self.current_token()}')
                            return f'def {identifier}():\n{parse_block}'
                        print(f'\033[91m\nERROR IN PARSE_PROCDECL: {self.current_token()}\033[0m')
                    print(f'\033[91m\nERROR IN PARSE_PROCDECL: {self.current_token()}\033[0m')
        return False
    
    def parse_compound_statement(self):
        print(f'1 parse_compound_statement: {self.current_token()}')
        parse_statement = self.parse_statement()
        if parse_statement:
            print(f'2 parse_compound_statement: {self.current_token()}')
            if self.current_token().token_value == ';':
                print(f'3 parse_compound_statement: {self.current_token()}')
                self.buffer+=1
                if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
                    print(f'4 parse_compound_statement: {self.current_token()}')
                    parse_compound_statement = self.parse_compound_statement()
                    if not parse_compound_statement:
                        return False
                    parse_statement = f'{parse_statement}\n{parse_compound_statement}'
                return f'{parse_statement}'
        return False
    
    def parse_expression(self):
        print(f'1 parse_expression: {self.current_token()}')
        parse_expression = ''
        if self.current_token().token_class.name == 'SIGN':
            parse_sign = self.parse_sign()
            if not parse_sign:
                return False
            parse_expression = f'{parse_sign}'
        print(f'2 parse_expression: {self.current_token()}')
        parse_term = self.parse_term()
        if parse_term:
            print(f'3 parse_expression: {self.current_token()}')
            parse_expression = f'{parse_expression}{parse_term}'
            if self.current_token().token_class.name == 'SIGN':
                print(f'4 parse_expression: {self.current_token()}')
                parse_terms = self.parse_terms()
                if not parse_terms:
                    return False
                parse_expression = f'{parse_expression} {parse_terms}'
                print(f'5 parse_expression: {self.current_token()}')
            return f'{parse_expression}'
        return False
        
    def parse_sign(self):
        print(f'1 parse_sign: {self.current_token()}')
        if self.current_token().token_class.name == 'SIGN':
            sign = self.current_token().token_value
            self.buffer+=1
            print(f'2 parse_sign: {self.current_token()}')
            return f'{sign}'
        return False
    
    def parse_term(self):
        print(f'1 parse_term: {self.current_token()}')
        parse_factor = self.parse_factor()
        if parse_factor:
            print(f'2 parse_term: {self.current_token()}')
            if self.current_token().token_value in ['*','/']:
                parse_factors = self.parse_factors()
                if not parse_factors:
                    return False
                parse_factor = f'{parse_factor} {parse_factors}'
                print(f'3 parse_term: {self.current_token()}')
            return f'{parse_factor}'
        return False
    
    def parse_terms(self):
        print(f'1 parse_terms: {self.current_token()}')
        if self.current_token().token_class.name == 'SIGN':
            sign = self.current_token().token_value
            self.buffer+=1
            print(f'2 parse_terms: {self.current_token()}')
            parse_term = self.parse_term()
            if parse_term:
                print(f'3 parse_terms: {self.current_token()}')
                return f'{sign} {parse_term}'
        return False
    
    def parse_factor(self):
        print(f'1 parse_factor: {self.current_token()}')
        if self.current_token().token_class.name in ['IDENTIFIER','NUMBER']:
            factor = self.current_token().token_value
            self.buffer+=1
            return f'{factor}'
        print(f'2 parse_factor: {self.current_token()}')
        if self.current_token().token_value == '(':
            self.buffer+=1
            print(f'3 parse_factor: {self.current_token()}')
            parse_expression = self.parse_expression()
            if parse_expression:
                print(f'4 parse_factor: {self.current_token()}')
                if self.current_token().token_value == ')':
                    self.buffer+=1
                    print(f'5 parse_factor: {self.current_token()}')
                    return f'({parse_expression})'
        return False
    
    def parse_factors(self):
        print(f'1 parse_factors: {self.current_token()}')
        if self.current_token().token_value in ['/','*']:
            sign = self.current_token().token_value
            self.buffer+=1
            print(f'2 parse_factors: {self.current_token()}')
            parse_factor = self.parse_factor()
            if parse_factor:
                print(f'3 parse_factors: {self.current_token()}')
                return f'{sign} {parse_factor}'
        return False
    
    def parse_condition(self):
        print(f'parse_condition: {self.current_token()}')
        if self.current_token().token_value in ['ODD','EVEN']:
            condition = self.current_token().token_value
            self.buffer+=1
            parse_expression = self.parse_expression()
            if parse_expression:
                if condition == 'ODD':
                    return f'({parse_expression}) % 2 != 0'
                if condition == 'EVEN':
                    return f'({parse_expression}) % 2 == 0'
            return False
        parse_expression = self.parse_expression()
        per = False
        if parse_expression:
            parse_relation, per = self.parse_relation()
            if parse_relation:
                parse_expression_inside = self.parse_expression()
                if parse_expression:
                    if per:
                        return f'{parse_expression} {parse_relation} {parse_expression_inside} == 0'
                    return f'{parse_expression} {parse_relation} {parse_expression_inside}'
        return False
    
    def parse_relation(self):
        print(f'1 parse_relation: {self.current_token()}')
        per = False
        if self.current_token().token_class.name == 'RELATION':
            relation = self.current_token().token_value
            if self.current_token().token_value == '/?':
                relation = '%'
                per = True
            if self.current_token().token_value == '=':
                relation = '=='
            self.buffer+=1
            print(f'2 parse_relation: {self.current_token()}')
            return relation, per
        return False

    def parse_constants(self):
        print(f'1 parse_constants: {self.current_token()}')
        parse_constdecl = self.parse_constdecl()
        if parse_constdecl:
            print(f'2 parse_constants: {self.current_token()}')
            if self.current_token().token_value == ';':
                self.buffer+=1
                print(f'3 parse_constants: {self.current_token()}')
                return f'{parse_constdecl}'
        return False

    def parse_constdecl(self):
        print(f'1 parse_constdecl: {self.current_token()}')
        parse_constdef = self.parse_constdef()
        if parse_constdef:
            print(f'2 parse_constdecl: {self.current_token()}')
            if self.current_token().token_value == ',':
                self.buffer+=1
                print(f'3 parse_constdecl: {self.current_token()}')
                parse_constdecl = self.parse_constdecl()
                if not parse_constdecl:
                    return False
                parse_constdef = f'{parse_constdef}; {parse_constdecl}'
                print(f'4 parse_constdecl: {self.current_token()}')
            return parse_constdef
        
    def parse_constdef(self):
        print(f'1 parse_constdef: {self.current_token()}')
        if (self.current_token().token_class.name == 'IDENTIFIER'):
            identifier = self.current_token().token_value
            self.buffer+=1
            print(f'2 parse_constdef: {self.current_token()}')
            if (self.current_token().token_value == '='):
                self.buffer+=1
                print(f'3 parse_constdef: {self.current_token()}')
                if (self.current_token().token_class.name == 'NUMBER'):
                    number = self.current_token().token_value
                    self.buffer+=1
                    print(f'4 parse_constdef: {self.current_token()}')
                    return f'{identifier} = {number}'
        return False
    


diretorio = './arquivos/'
with open('./testes/' + 'ex3.pl0mod.txt', 'r') as arquivo:
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
print(f"\n\n###############################################\n\n")
parser = Parser(lex, token_list)
prog = parser.parse_program()
if prog:
    print("\n:)")
    print("\n===============================\n")
    print(f'\033[93m{prog}\033[0m')
else:
    print(f"\033[91m\nSOMETHING WENT WHONG\033[0m")