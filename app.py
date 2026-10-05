import command as cmd
import expression as expr
from memory import Memory
from interpreter import interpret
from lexer.lexer import Lexer

if __name__ == "__main__":
  with open("./main.code") as f:
    source_code = f.read()

  lexer = Lexer(source_code)
  tokens = lexer.lex()
  for token in tokens:
    print(token)