from dataclasses import dataclass
from typing import Literal, ClassVar, get_args
from expression import Expression

@dataclass(frozen=True)
class Token:
  start: int

@dataclass(frozen=True)
class LeftParen(Token):
  keywords: ClassVar[set[str]] = {"("}

@dataclass(frozen=True)
class RightParen(Token):
  keywords: ClassVar[set[str]] = {")"}

@dataclass(frozen=True)
class LeftCurly(Token):
  keywords: ClassVar[set[str]] = {"{"}

@dataclass(frozen=True)
class RightCurly(Token):
  keywords: ClassVar[set[str]] = {"}"}

@dataclass(frozen=True)
class Equals(Token):
  keywords: ClassVar[set[str]] = {"="}

@dataclass(frozen=True)
class SemiColon(Token):
  keywords: ClassVar[set[str]] = {";"}

Operators = Literal["+", "-", "*", "/", "<", ">", "#", "&", "^"]

@dataclass(frozen=True)
class Operator(Token):
  keywords: ClassVar[set[str]] = set(get_args(Operators))
  symbol: str

SINGLECHAR_TOKENS: set[type[Token]] = {LeftParen, RightParen, LeftCurly, RightCurly, Equals, SemiColon, Operator}


@dataclass(frozen=True)
class Assign(Token):
  keywords: ClassVar[set[str]] = {"assign"}

@dataclass(frozezn=True)
class Delete(Token):
  keywords: ClassVar[set[str]] = {"delete"}

@dataclass(frozen=True)
class While(Token):
  keywords: ClassVar[set[str]] = {"while"}

@dataclass(frozen=True)
class If(Token):
  keywords: ClassVar[set[str]] = {"if"}

@dataclass(frozen=True)
class Else(Token):
  keywords: ClassVar[set[str]] = {"else"}

@dataclass(frozen=True)
class Output(Token):
  keywords: ClassVar[set[str]] = {"output"}

@dataclass(frozen=True)
class And(Token):
  keywords: ClassVar[set[str]] = {"and"}

@dataclass(frozen=True)
class Or(Token):
  keywords: ClassVar[set[str]] = {"or"}

@dataclass(frozen=True)
class Not(Token): 
  keywords: ClassVar[set[str]] = {"not"}

MULTICHAR_TOKENS: set[type[Token]] = {Assign, While, If, Else, Output, And, Or, Not}


@dataclass(frozen=True)
class Number(Token):
  x: int

@dataclass(frozen=True)
class Identifier(Token):
  name: str


LOWER_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
UPPER_ALPHABET = LOWER_ALPHABET.upper()
IDENTIFIER_ALPHABET = LOWER_ALPHABET + UPPER_ALPHABET + "_" + "0123456789"


@dataclass(frozen=True)
class ExpressionTreeToken(Token):
  expr: Expression



WHITESPACE = set((" ", "\t", "\n", "\r"))

KEYWORD_TO_SINGLECHAR_TOKENS = {
  keyword : token_class
  for token_class in SINGLECHAR_TOKENS
  for keyword in token_class.keywords 
}

KEYWORD_TO_MULTICHAR_TOKENS = {
  keyword : token_class
  for token_class in MULTICHAR_TOKENS
  for keyword in token_class.keywords 
}
