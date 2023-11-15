from lex import Lex
import rules
from token import TokenClass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.buffer = []

    def next_token(self):
        if self.buffer:
            return self.buffer.pop(0)
        return self.lexer.next()

    def peek(self):
        if not self.buffer:
            self.buffer.append(self.lexer.next())
        return self.buffer[0]

    def expect(self, expected_token_value):
        token = self.lexer.next()
        return token and token.token_value == expected_token_value

    def parse_program(self):
        if self.parse_block():
            return self.expect('.')
        return False

    def parse_block(self):
        if not self.parse_variables():
            return False
        if not self.parse_constants():
            return False
        if not self.parse_procedures():
            return False
        return self.parse_statement()

    def parse_statement(self):
        # Placeholder for statement parsing
        # Implement the actual statement parsing logic here
        # Returning True for the sake of example
        return True

################################################################S

    def parse_constants(self):
        token = self.lexer.next()
        if token and token.token_value == "CONST":
            if not self.parse_constdecl():
                return False
            return self.expect(';')
        # No 'CONST' token, so this part is optional
        return True

    def parse_constdecl(self):
        # Implement this method based on the grammar rule for <constdecl>
        pass

    def parse_variables(self):
        token = self.lexer.next()
        if token and token.token_value == "VAR":
            if not self.parse_vardecl():
                return False
            return self.expect(';')
        # No 'VAR' token, so this part is optional
        return True

    def parse_procedures(self):
        while True:
            token = self.lexer.peek()  # 'peek' does not consume the token
            if not token or token.token_value != "PROCEDURE":
                break
            if not self.parse_procdecl():
                return False
        return True

    def parse_procdecl(self):
        # Implement based on the grammar rule for <procdecl>
        pass

    def parse_statement(self):
        # This will be more complex as <statement> might have multiple forms
        token = self.lexer.peek()
        if not token:
            return False
        if token.token_value == "IF":
            return self.parse_if_statement()
        elif token.token_value == "WHILE":
            return self.parse_while_statement()
        # ... handle other types of statements
        else:
            return False

    def parse_while_statement(self):
        # Implement based on the grammar rule for 'while' statements
        pass

    def parse_expression(self):
        if not self.parse_term():
            return False
        while True:
            token = self.lexer.peek()
            if token and token.token_value in ["+", "-"]:
                self.lexer.next()  # Consume the '+' or '-' token
                if not self.parse_term():
                    return False
            else:
                break
        return True

    def parse_term(self):
        # Implement based on the grammar rule for <term>
        pass

    def parse_compound_statement(self):
        if not self.expect('BEGIN'):
            return False

        while True:
            if not self.parse_statement():
                return False

            # Assuming ';' is used to separate statements
            next_token = self.lexer.peek()
            if not next_token or next_token.token_value != ';':
                break
            self.lexer.next()  # Consume the ';' token

        return self.expect('END')

    def parse_factor(self):
        token = self.lexer.next()
        if token.token_class == TokenClass.NUMBER or token.token_class == TokenClass.IDENTIFIER:
            return True
        elif token.token_value == '(':
            if not self.parse_expression():
                return False
            return self.expect(')')
        return False

    def parse_terms(self):
        if not self.parse_term():
            return False
        while True:
            token = self.lexer.peek()
            if token and token.token_value in ['*', '/']:
                self.lexer.next()  # Consume the operator
                if not self.parse_term():
                    return False
            else:
                break
        return True


    def parse_condition(self):
        # Implement based on the grammar rule for <condition>
        pass

    def parse_sign(self):
        token = self.lexer.peek()
        if token and token.token_value in ['+', '-']:
            self.lexer.next()  # Consume the sign
        return self.parse_expression()

    def parse_constdef(self):
        token = self.lexer.next()
        if token.token_class != TokenClass.IDENTIFIER:
            return False

        if not self.expect('='):
            return False

        return self.expect_number()
    
    def parse_vardecl(self):
        token = self.lexer.next()
        if token.token_class == TokenClass.IDENTIFIER:
            print('aloha')
            token = self.lexer.next()
            if token.token_class == TokenClass.SYMBOL:
                self.parse_vardecl()
        # if not self.expect_identifier():
            return False

        while True:
            token = self.lexer.peek()
            if token and token.token_value == ',':
                self.lexer.next()  # Consume the comma
                if not self.expect(','):
                    return False
            else:
                break
        return True

    def parse_vardecl(self):
        if not self.expect(','):
            return False

        while True:
            token = self.lexer.peek()
            if token and token.token_value == ',':
                self.lexer.next()  # Consume the comma
                if not self.expect(','):
                    return False
            else:
                break
        return True

    def parse_if_statement(self):
        if not self.expect('IF'):
            return False

        if not self.parse_condition():
            return False

        if not self.expect('THEN'):
            return False

        if not self.parse_statement():
            return False

        if self.lexer.peek().token_value == 'ELSE':
            self.lexer.next()  # Consume 'ELSE'
            return self.parse_statement()

        return True


diretorio = './arquivos/'
with open('./testes/' + 'ex2.pl0mod.txt', 'r') as arquivo:
    content = arquivo.read()

print('parsing content')
print(content)
print('\n\n')

lex = Lex(content, [ \
    rules.KeywordRule(), \
    rules.NumberRule(), \
    rules.StatementRule(), \
    rules.RelationRule(), \
    rules.FactorsRule(), \
    rules.SymbolRule(), \
    rules.ReservedWordsRule(), \
    rules.IdentifierRule(), \
    ])


# Example usage
example_tokens = []  # Placeholder for actual tokens from the lexical analyzer
parser = Parser(lex)

# Parse the program
result = parser.parse_program()
print(result)  # True or False depending on whether the parsing was successful
input()


while True:
  token_atual = lex.next()
  if token_atual is None:
    break
  print(f'\ntoken extraido: {token_atual}\n\n\n')