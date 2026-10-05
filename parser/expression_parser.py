from typing import Iterator
import lexer.lexer_tokens as tok



def _parse_dereference(tokens: Iterator[tok.Token]):
  pass

def _parse_pointer_of():
  pass

def _parse_not():
  pass

def _parse_negative():
  pass

def _parse_power():
  pass

def _parse_multiplication():
  pass

def _parse_division():
  pass

def _parse_addition():
  pass

def _parse_minus():
  pass

def _parse_greater_than():
  pass

def _parse_less_than():
  pass

def _parse_and():
  pass

def _parse_or():
  pass

def _parse_equals():
  pass

def parse_expression(tokens: Iterator[tok.Token]):
  return _parse_equals(tokens)