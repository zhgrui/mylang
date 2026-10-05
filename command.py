from dataclasses import dataclass
import expression as expr
import language_types as lt

# TODO: del / deallocate statement


@dataclass(frozen=True)
class Assignment: #assign
  variable: expr.Variable
  value: expr.Expression

@dataclass(frozen=True)
class Delete: #delete
  variable: expr.Variable

@dataclass(frozen=True)
class Sequence: 
  left_command: 'Command'
  right_command: 'Command'

@dataclass(frozen=True)
class While: #while
  guard: expr.Expression
  loop_command: 'Command'

@dataclass(frozen=True)
class IfThenElse: #if then else
  guard: expr.Expression
  then_command: 'Command'
  else_command: 'Command'

@dataclass(frozen=True)
class Output: # output
  value: expr.Expression

@dataclass(frozen=True)
class Skip:
  pass

Command = Skip | Output | IfThenElse | While | Sequence | Delete | Assignment