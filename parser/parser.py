from parser.command_parser import parse_command_sequence
from lexer.lexer import Lexer

def parse(lexer: Lexer):
  commands = parse_command_sequence(lexer)

  if lexer.has_next():
    raise Exception(f"Unexpected token {lexer.peek()}. Expected EOF")

  return commands
