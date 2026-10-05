from dataclasses import dataclass
from language_types import VarType


# 5, 6, 8, 10000, 2478953271
@dataclass(frozen=True)
class Number:
  x: float

@dataclass(frozen=True)
class Variable:
  name: VarType

# 3 + 4, 534890 + 2
@dataclass(frozen=True)
class Addition:
  left_expr: 'Expression'
  right_expr: 'Expression'

# 5 * 8 
@dataclass(frozen=True)
class Multiplication:
  left_expr: 'Expression'
  right_expr: 'Expression'

# 7 / 8
@dataclass(frozen=True)
class Division:
  left_expr: 'Expression'
  right_expr: 'Expression'

# fdsasfa = &()
@dataclass(frozen=True)
class PointerOf:
  """
  when evaluated, should get the variable's address it's pointing towards.
  This is basically the pointer type! (very suspicious, not a good explaination)

  &() operator
  """
  var: Variable

# fjdsaklf; *fjdksal;
@dataclass(frozen=True)
class Dereference:
  """
  when evaluated, should get the value at the address 
  *() operator
  """
  expr: 'Expression'


@dataclass(frozen=True)
class LessThan:
  left_expr: 'Expression'
  right_expr: 'Expression'

@dataclass(frozen=True)
class GreaterThan:
  left_expr: 'Expression'
  right_expr: 'Expression'

@dataclass(frozen=True)
class Equals:
  left_expr: 'Expression'
  right_expr: 'Expression'

@dataclass(frozen=True)
class And:
  left_expr: 'Expression'
  right_expr: 'Expression'

@dataclass(frozen=True)
class Or:
  left_expr: 'Expression'
  right_expr: 'Expression'

@dataclass(frozen=True)
class Not:
  expr: 'Expression'


Expression = Number | Variable | Addition | Multiplication | Division | PointerOf | Dereference | LessThan | GreaterThan | And | Or | Not | Equals