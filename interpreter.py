import expression as expr
import command as cmd
import memory as memo

# TODO: make this into a class, because memory is shared state which needs to be modified
# TODO: rewrite with enum semantics


def _evaluate_expression(expression: expr.Expression, memory: memo.Memory) -> int:
  match expression:
    case expr.Number(x):
      return x
    
    case expr.Variable(name):
      return memory.get_variable_value_from_name(name)
    
    case expr.Dereference(e):
      return memory.get_value_at_address(
        _evaluate_expression(e, memory)
      )
    
    case expr.Addition(left_expr, right_expr):
      return _evaluate_expression(left_expr, memory) + \
            _evaluate_expression(right_expr, memory)
    
    case expr.Multiplication(left_expr, right_expr):
      return _evaluate_expression(left_expr, memory) * \
            _evaluate_expression(right_expr, memory)

    case expr.Division(left_expr, right_expr):
      return _evaluate_expression(left_expr, memory) // \
        _evaluate_expression(right_expr, memory)

    case expr.PointerOf(var):
      return memory.get_memory_address_of_var(var.name)

    case expr.LessThan(left_expr, right_expr):
      left_result = _evaluate_expression(left_expr, memory)
      right_result = _evaluate_expression(right_expr, memory)
      return 1 if left_result < right_result else 0

    case expr.GreaterThan(left_expr, right_expr):
      left_result = _evaluate_expression(left_expr, memory)
      right_result = _evaluate_expression(right_expr, memory)
      return 1 if left_result > right_result else 0

    case expr.And(left_expr, right_expr):
      left_result = _evaluate_expression(left_expr, memory)
      right_result = _evaluate_expression(right_expr, memory)
      return 1 if left_result != 0 and right_result != 0 else 0

    case expr.Or(left_expr, right_expr):
      left_result = _evaluate_expression(left_expr, memory)
      right_result = _evaluate_expression(right_expr, memory)
      return 1 if left_result != 0 or right_result != 0 else 0

    case expr.Not(inner_expr):
      return 1 if _evaluate_expression(inner_expr, memory) == 0 else 0

    case expr.Equals(left_expr, right_expr):
      return 1 if _evaluate_expression(left_expr, memory) == _evaluate_expression(left_expr, memory) else 0
    
    case _:
      raise Exception(f"Invalid expression type {type(expression)} when evaluating expression {expression} with memory {memory}")


def interpret(command: cmd.Command, memory: memo.Memory):
  match command:
    case cmd.Assignment(var, value):
      val = _evaluate_expression(value, memory)
      if isinstance(value, expr.PointerOf):
          memory.assign_pointer(var.name, val)
          return

      memory.assign(var.name, val)
      return

    case cmd.Delete(var):
      memory.delete(var.name)
      return

    case cmd.Sequence(left_command, right_command):
      interpret(left_command, memory)
      interpret(right_command, memory)
      return

    case cmd.IfThenElse(guard, then_cmd, else_cmd):
      if _evaluate_expression(guard, memory) != 0:
        interpret(then_cmd, memory)
      else:
        interpret(else_cmd, memory)
      return

    case cmd.While(guard, loop_cmd):
      interpret(
        cmd.IfThenElse(
          guard,
          cmd.Sequence(loop_cmd, command), 
          cmd.Skip()
        ),
        memory
      )
      return

    case cmd.Skip():
      return

    case cmd.Output(val):
      print(_evaluate_expression(val, memory))
      return

    case _:
      raise Exception(f"Invalid command type {type(command)} when interpreting command {command} with memory {memory}")
