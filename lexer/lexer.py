import lexer.lexer_tokens as tok
from typing import Optional, Iterator

class Lexer:
  def __init__(self, source_code: str):
    self._source = source_code
    self._source_cursor = 0
    self._length = len(source_code)
    self._tokens = self._lex()
    self._token_pointer = 0


  def _add_last_token(self, tokens: list[str], last_token: list[str]):
    token_as_string = "".join(last_token)
    if len(token_as_string) == 0:
      return

    tokens.append(token_as_string)

  def _match_singlechar_token(self, char: str=None) -> Optional[tok.Token]:    
    first_char = char if char is not None else self._source[self._cursor]
    token_start = self._source_cursor

    match first_char:
      case c if c in tok.SemiColon.keywords:
        return tok.SemiColon(token_start)
      case c if c in tok.LeftCurly.keywords:
        return tok.LeftCurly(token_start)
      case c if c in tok.RightCurly.keywords:
        return tok.RightCurly(token_start)
      case c if c in tok.LeftParen.keywords:
        return tok.LeftParen(token_start)
      case c if c in tok.RightParen.keywords:
        return tok.RightParen(token_start)
      case c if c in tok.Equals.keywords:
        return tok.Equals(token_start)
      case c if c in tok.Operator.keywords:
        return tok.Operator(token_start, c)
      
    return None

  def _match_multichar_token(self) -> Optional[tok.Token]:
    token_start = self._source_cursor
    token_end = self._source_cursor + 1
    while token_end < self._length and \
          self._source[token_end] not in tok.WHITESPACE and \
          self._match_singlechar_token(self._source[token_end]) is None:
      token_end += 1

    self._source_cursor = token_end
    token_string = self._source[token_start:token_end]

    match token_string:
      case string if string in tok.Assign.keywords:
        return tok.Assign(token_start)
      case string if string in tok.Delete.keywords:
        return tok.Delete(token_start)
      case string if string in tok.While.keywords:
        return tok.While(token_start)
      case string if string in tok.If.keywords:
        return tok.If(token_start)
      case string if string in tok.Else.keywords:
        return tok.Else(token_start)
      case string if string in tok.Output.keywords:
        return tok.Output(token_start)
      case string if string in tok.And.keywords:
        return tok.And(token_start)
      case string if string in tok.Or.keywords:
        return tok.Or(token_start)
      case string if string in tok.Not.keywords:
        return tok.Not(token_start)

    if token_string.isascii() and token_string.isdecimal():
      return tok.Number(token_start, int(float(token_string)))
    
    if token_string.isalnum():
      return tok.Identifier(token_start, token_string)

    return None

  def _next_token(self) -> tok.Token:
    while self._source_cursor < self._length and self._source[self._source_cursor] in tok.WHITESPACE:
      self._source_cursor += 1

    token_start = self._source_cursor

    if token := self._match_singlechar_token():
      self._source_cursor += 1
      return token

    if token := self._match_multichar_token():
      return token

    raise Exception(f"Unrecognized Token at position {token_start}")

  def _has_next_token(self) -> tok.Token:
    return self._source_cursor < self._length

  def _lex(self) -> list[tok.Token]:
    tokens = []
    while self._has_next_token():
      tokens.append(self._next_token())

    self._source_cursor = 0
    return tokens

  def next(self) -> tok.Token:
    next_token = self.peek()
    self._token_pointer += 1
    return next_token

  def peek(self) -> tok.Token:
    if not self.has_next():
      raise Exception("no more tokens available")

    return self._tokens[self._token_pointer]

  def has_next(self) -> bool:
    return self._token_pointer < self._tokens

  