from enum import Enum


class TokenClass(Enum):
  NUMBER = 1,
  IDENTIFIER = 2,
  SYMBOL = 3,
  FACTOR = 4,
  RESERVED_WORD = 5,
  STATEMENT = 6,
  KEYWORD = 7,
  RELATION = 8,
  SIGN = 9,
  COMMENT = 10,

class Token:

  def __init__(self, token_class: TokenClass, token_value):
    self.token_class = token_class
    self.token_value = token_value

  def __str__(self) -> str:
    return f'<Token class: {self.token_class}, value: {self.token_value}>'
