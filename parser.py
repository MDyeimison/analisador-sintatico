class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def expect(self, expected_token_value):
        token = self.lexer.next()
        return token and token.token_value == expected_token_value

    def parse_program(self):
        if self.parse_block():
            return self.expect('.')
        return False

    def parse_block(self):
        # Implementing partial functionality for <block>
        # In a full implementation, you would check for <constants>, <variables>, <procedures>, and <statement>
        # Here, we'll just call parse_statement as a placeholder
        return self.parse_statement()

    def parse_statement(self):
        # Placeholder for statement parsing
        # Implement the actual statement parsing logic here
        # Returning True for the sake of example
        return True

    # Additional parser methods for other grammar rules can be added here
    # ...