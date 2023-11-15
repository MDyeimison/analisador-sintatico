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

class RelationRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [
      r'=',r'#',r'<=',r'<',r'>=',r'>',r'\/\?'
    ]

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.RELATION, match)
  
class ReservedWordsRule(RuleInterface):

  def regex_rules(self) -> list[str]:
    return [
      r'\bNOT\b',r'\bTHEN\b',r'\bDO\b',r'\bODD\b',r'\bEVEN\b',r'\bPROCEDURE\b',r'\bEND\b'
    ]

  def extract_token(self, match: str) -> Token:
    return Token(TokenClass.RESERVED_WORD, match)

class KeywordRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'CONST', r'VAR']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.KEYWORD, match)


class SymbolRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'\,',r'\;',r'<-']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.SYMBOL, match)

class SignRule(RuleInterface):

  def regex_rules(self) -> list[str]:
        return [r'\+', r'\-']

  def extract_token(self, match: str) -> Token:
      return Token(TokenClass.SIGN, match)
class FactorsRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'[^*]\*[^*]',r'\*',r'\/',r'\(',r'\)',r'\.']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.FACTOR, match)


class NumberRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'\d+']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.NUMBER, int(match))

class IdentifierRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'[a-zA-Z_][a-zA-Z0-9_]*']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.IDENTIFIER, match)
    
class StatementRule(RuleInterface):

    def regex_rules(self) -> list[str]:
        return [r'\bCALL\b',r'\bBEGIN\b',r'\bIF\b',r'\bWHILE\b',r'\bPRINT\b']

    def extract_token(self, match: str) -> Token:
        return Token(TokenClass.STATEMENT, match)
    
class CommentRule(RuleInterface):
   
   def regex_rules(self) -> list[str]:
      return [r"\{e\}(.*?)\{e\}"]
   
   def extract_token(self, match: str) -> Token:
      return Token(TokenClass.COMMENT, match)