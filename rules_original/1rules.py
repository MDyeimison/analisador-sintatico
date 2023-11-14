import re
from token import Token, TokenClass


class RuleInterface:

  def regex_rules(self) -> list[str]:
    pass

  def extract_token(self, match: str) -> Token:
    pass

  def check_match(self, content: str) -> re.Match:
    for rule in self.regex_rules():
      match = re.match('^' + rule, content)
      if match:
        return match
    return None


class NumberConstantRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [r'\d+']

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.NUMERICAL_CONSTANT, int(match))

class NumberFloatRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [r'\d*\.\d+']

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.NUMERICAL_FLOAT, match)

class IdRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return ['[a-zA-Z_][a-zA-Z0-9_]*']

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.ID, match)
  
class TextConstRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [r'"([^"\\]*(\\.[^"\\]*)*)"']

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.TEXT_CONST, match)


class SymbolRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [r'\{', r'\}', r'\(', r'\)', r'\[', r'\]', r'\;', r'\,']

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.SYMBOL, match)


class OperatorRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [
      r'==', r'[^*]\*[^*]', r'/',
      r'\+\+', r'--', r'!', r'&&', r'%', r'-\>', r'=', r'!\=',
      r'\|\|', r'&', r'\+=', r'\-\=', r'\*\=', r'\/\=', r'\<\=', r'\<',
      r'\>\=', r'\>', r'\+', r'-', r'\*'
    ]

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.OPERATOR, match)
  
class ReservedWordsRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [
      r'\bint\b',r'\bchar\b',r'\bfloat\b',r'\bdouble\b',r'\bvoid\b',r'\bif\b',r'\belse\b',r'\bfor\b',r'\bwhile\b',r'\bdo\b',r'\bbreak\b',r'\bcontinue\b',r'\bstruct\b',r'\bswitch\b',r'\bcase\b',r'\bdefault\b',r'\breturn\b'
    ]

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.RESERVED_WORD, match)
  
class CommentsRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [
      r'(\/\*([^*]|[\r\n]|(\*+([^*\/]|[\r\n])))*\*+\/)|(\/\/.*)'
    ]

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.COMMENT, match)