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
    rules.SymbolRule(), \
    rules.StatementRule(), \
    rules.RelationRule(), \
    rules.FactorsRule(), \
    rules.SignRule(), \
    rules.ReservedWordsRule(), \
    rules.IdentifierRule(), \
    ])

teste = []
while True:
  token_atual = lex.next()
  teste.append(token_atual)
  if token_atual is None:
    break
  print(token_atual.token_value)
  print(f'\ntoken extraido: {token_atual}\n\n\n')
  #input()
print(teste[0].token_class.name)
print(teste[0].token_value)
