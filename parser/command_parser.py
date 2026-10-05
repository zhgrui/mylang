from typing import Optional
import lexer.lexer_tokens as tok
from lexer.lexer import Lexer
from parser.heap_expression_parser import parse_expression
import command as cmd
import expression as expr

def _parse_for(lexer: Lexer):
  pass

def _parse_if_then_else(lexer: Lexer):
  if not isinstance(token := lexer.next(), tok.LeftParen):
    raise Exception(f"Got token {token}, expected an left parentheses")

  expression_ast = parse_expression(lexer)

  if not isinstance(token := lexer.next(), tok.RightParen):
    raise Exception(f"Got token {token}, expected an right parentheses")
  
  if not isinstance(token := lexer.next(), tok.LeftCurly):
    raise Exception(f"Got token {token}, expected an left curly braces")

  then_command_sequence = parse_command_sequence(lexer)
  
  if not isinstance(token := lexer.next(), tok.RightCurly):
    raise Exception(f"Got token {token}, expected an right curly braces")

  next_token = lexer.peek()
  if not isinstance(next_token, tok.Else):
    return cmd.IfThenElse(expression_ast, then_command_sequence, cmd.Skip())

  lexer.next()

  if not isinstance(token := lexer.next(), tok.LeftCurly):
    raise Exception(f"Got token {token}, expected an left curly braces")

  else_command_sequence = parse_command_sequence(lexer)
  
  if not isinstance(token := lexer.next(), tok.RightCurly):
    raise Exception(f"Got token {token}, expected an right curly braces")
  
  return cmd.IfThenElse(expression_ast, then_command_sequence, else_command_sequence)
  


def _parse_while(lexer: Lexer):
  if not isinstance(token := lexer.next(), tok.LeftParen):
    raise Exception(f"Got token {token}, expected an left parentheses")

  expression_ast = parse_expression(lexer)
  
  if not isinstance(token := lexer.next(), tok.RightParen):
    raise Exception(f"Got token {token}, expected an right parentheses")

  if not isinstance(token := lexer.next(), tok.LeftCurly):
    raise Exception(f"Got token {token}, expected an left curly braces")

  command_sequence = parse_command_sequence(lexer)
  
  if not isinstance(token := lexer.next(), tok.RightCurly):
    raise Exception(f"Got token {token}, expected an right curly braces")

  return cmd.While(expression_ast, command_sequence)


def _parse_delete(lexer: Lexer):
  if not isinstance(token := lexer.next(), tok.Identifier):
    raise Exception(f"Got token {token}, expected an Identifier")

  return cmd.Delete(expr.Variable(token.name))

def _parse_output(lexer: Lexer):
  expression_ast = parse_expression(lexer)

  return cmd.Output(expression_ast)


def _parse_assign(lexer: Lexer) -> cmd.Assignment:
  if not isinstance(token := lexer.next(), tok.Identifier):
    raise Exception(f"Got token {token}, expected an Identifier")

  identifier = token
  
  if not isinstance(token := lexer.next(), tok.Equals):
    raise Exception(f"Got token {token}, expected =")

  expression_ast = parse_expression(lexer)

  return cmd.Assignment(expr.Variable(identifier.name), expression_ast)


def _parse_command(lexer: Lexer) -> Optional[cmd.Command]:
  if not lexer.has_next():
    return None

  next_token = lexer.peek()

  match next_token:
    case tok.Assign:
      lexer.next()
      return _parse_assign(lexer) 
    case tok.Output:
      lexer.next()
      return _parse_output(lexer) 
    case tok.Delete:
      lexer.next()
      return _parse_delete(lexer)
    case tok.While:
      lexer.next()
      return _parse_while(lexer)
    case tok.If:
      lexer.next()
      return _parse_if_then_else(lexer)
    case _:
      return None

def parse_command_sequence(lexer: Lexer) -> cmd.Command:
  current_command = cmd.Skip

  while lexer.has_next():
    command = _parse_command(lexer)

    if command is None:
      return current_command

    next_token = lexer.peek()

    if not isinstance(next_token, tok.SemiColon):
      raise Exception(f"Got token {next_token}, expected a semicolon.")

    lexer.next()

    current_command = cmd.Sequence(current_command, command)

  return current_command


