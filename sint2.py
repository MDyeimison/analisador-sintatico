from lex import Lex
import rules

class Parser:
    def __init__(self, lexer, token_list, buffer=0):
        self.lexer = lexer
        self.buffer = buffer
        self.token_list = token_list

    # def next_token(self):
    #     if self.buffer:
    #         self.buffer+=1
    #         return self.token_list[self.buffer]
    #     return self.token_list[0]

    def next_token(self):
        # if self.buffer == 0:
        #     return self.token_list[self.buffer]
        self.buffer+=1
        return self.token_list[self.buffer]
    
    def current_token(self):
        return self.token_list[self.buffer]
    
    def peek(self):
        if not self.buffer:
            self.token_list[0]
        return self.token_list[self.buffer+1]

    def expect(self, expected_token_value):
        token = self.next_token()
        return token and token.token_value == expected_token_value
    
    def expect_class(self, expected_token_value):
        token = self.next_token()
        return token and token.token_class.name == expected_token_value
    
    def parse_program(self):
        # while self.buffer < len(self.token_list)-1:
        #     print('aiiiii')
        #     if self.buffer > 0:
        #         print(f'\033[91m', self.token_list[self.buffer-1] ,'\033[0m')
        #     print(f'\033[91m', self.token_list[self.buffer] ,'\033[0m')
        #     if not self.parse_block():
        #         print(f'\033[94m', self.current_token() ,'\033[0m')
        #         print(f'\033[91mparse_block ERROR\033[0m')
        #         return False
        if self.parse_block():
            print(f'teste: {self.peek()}')
            return self.expect('.')
        return False
        # print('aiiiii')
        # return self.expect('.')
    
    def parse_block(self):
        print(f'\033[96mENTREIIIIIIIIIIII\033[0m')
        print(f'\033[92m', self.current_token() ,'\033[0m')
        input()
        if self.current_token():
            if self.current_token().token_value == 'VAR':
                if not self.parse_variables():
                    return False
            if self.current_token().token_class.name in ['STATEMENT','IDENTIFIER']:
                print(f'\033[92mSTATEMENT: {self.current_token()}\033[0m')
                if not self.parse_statement():
                    return False
                print(f'\033[94mDEU CERTO STATEMENT: ', self.current_token() ,'\033[0m')
                input()
                return True
            
            if self.current_token().token_value == 'CONST':
                print(f'\033[92mCONST\033[0m')
                return False
            print(f'passei: {self.current_token()}')
            if self.current_token().token_value == 'PROCEDURE':
                print(f'\033[92mENTREI PROCEDURE {self.current_token()}\033[0m')
                if not self.parse_procedures():
                    print(f'\033[92mFODEU PROCEDURE\033[0m')
                    return False
                print(f'\033[94matomalaka\033[0m')
                return True
            # if not self.parse_constants():
            #     return False
            # if not self.parse_procedures():
            #     return False
            # return self.parse_statement()
        return True

    def parse_variables(self):
        print(f'{self.token_list[self.buffer]}')
        if self.token_list[self.buffer].token_value == 'VAR':
            if self.parse_vardecl():
                if self.expect(';'):
                    self.buffer+=1
                    return True
            return False
        else:
            return False
        
    def parse_vardecl(self):
        if self.peek().token_class.name == 'IDENTIFIER':
            self.buffer+=1
            if not (self.peek().token_value == ','):
                return True
            else:
                self.buffer+=1
                if self.parse_vardecl():
                    return True
        return False

    def parse_procedures(self):
        print(f'\033[96mentrei parseprocedures1: ', self.current_token() ,'\033[0m')
        if not self.parse_prodecl():
            print(f'cai prodecl: {self.current_token()}')
            return False
        else:
            print(f'sucesso1: {self.current_token()}')
            input()
        if not self.parse_procedures():
            print(f'cai procedures: {self.current_token()}')
            return False
        else:
            print(f'sucesso2: {self.current_token()}')
            input()
        print('passei direto')
        return True

    def parse_prodecl(self):
        if not self.current_token().token_value == 'PROCEDURE':
            return False
        if not self.expect_class('IDENTIFIER'):
            return False
        if not self.expect(';'):
            return False
        self.buffer+=1
        if not self.parse_block():
            print(f'\033[91mcai no parse_block do parse_prodecl: {self.current_token()}\033[0m')
            return False
        if not self.current_token().token_value == ';':
            print(f'\033[91mcai no final parse_prodecl: {self.current_token}\033[0m')
            return False
        return True
    
    def parse_statement(self):
        if self.current_token().token_class.name == 'IDENTIFIER':
            if not self.expect('<-'):
                return False
            self.buffer+=1
            if not self.parse_expression():
                print(f'\033[94mcai no statement: {self.current_token()}\033[0m')
                input()
                return False
        if self.current_token().token_value == 'CALL':
            if not self.expect_class('IDENTIFIER'):
                return False
            print(f'\033[93mcai no statement CALL: ', self.current_token() ,'\033[0m')
            input()
        print(f'CHEGUI AQUI STATEMENT: {self.current_token()}')
        input()
        if self.current_token().token_value == 'BEGIN':
            self.buffer+=1
            print(f'ENTREI BEGIN: {self.current_token()}')
            if not self.parse_compound_statement():
                return False
            if not self.expect('END'):
                return False
            print('FINAL BEGIN')
            input()
        return True

    def parse_compound_statement(self):
        print(f'\033[94mENTREI COMPOUND STATEMENT: ', self.current_token() ,'\033[0m')
        if not self.parse_statement():
            return False
        if not self.expect(';'):
            return False
        return True
    
    def parse_expression(self):
        if self.current_token().token_class.name == 'SIGN':
            if not self.parse_sign(self):
                return False
        if not self.parse_term():
            pass
        return True

    def parse_sign(self):
        if not self.expect('+') or not self.expect('-'):
            return False
        self.buffer+=1
        return True
    
    def parse_term(self):
        if not self.parse_factor():
            return False
        if self.current_token().token_class.name == 'SIGN':
            if not self.parse_terms():
                return False
        return True
    
    def parse_factor(self):
        print('SDFSDFSDF')
        input()
        token_class_name = self.current_token().token_class.name
        if token_class_name == 'IDENTIFIER' or token_class_name == 'NUMBER':
            self.buffer+=1
            # return True
        if self.current_token().token_value == '(':
            self.buffer+=1
            if not self.parse_expression():
                return False
            elif not self.current_token().token_value == ')':
                return False
            self.buffer+=1
            # return True
        #######################################
        #######################################
        #######################################
        ##############CONTINUE AQUI############
        ###########IMPLEMENTAR FACTORS#########
        #######################################
        #######################################
        return True
        
    
    def parse_terms(self):
        if not self.current_token().token_class.name == 'SIGN':
            return False
        self.buffer+=1
        if not self.parse_term():
            return False
        self.buffer+=1
        return True

        

diretorio = './arquivos/'
with open('./testes/' + 'ex2.pl0mod.txt', 'r') as arquivo:
    content = arquivo.read()

print('parsing content')
print(content)
print('\n\n')

lex = Lex(content, [ \
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


# Example usage
# example_tokens = []  # Placeholder for actual tokens from the lexical analyzer

# Parse the program
# result = parser.parse_program()
# print(result)  # True or False depending on whether the parsing was successful
# input()

teste = []
while True:
  token_atual = lex.next()
  print(f'\033[94m', token_atual ,'\033[0m')
  teste.append(token_atual)
  if token_atual is None:
    break
  print(f'\ntoken extraido: {token_atual}\n\n\n')
parser = Parser(lex, teste)
print(teste[0].token_class.name)
print(teste[0].token_value)
print(parser.parse_program())