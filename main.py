from lex import Lex
import rules

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

while True:
  token_atual = lex.next()
  if token_atual is None:
    break
  print(token_atual.token_value)
  print(f'\ntoken extraido: {token_atual}\n\n\n')
  input()
