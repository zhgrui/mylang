from lexer.lexer import Lexer
from expression import Expression
from utils.linkedlist import Node, LinkedList
import lexer.lexer_tokens as tok
import heapq


def _valid_token_type(token: tok.Token):
  return \
    isinstance(token, tok.Identifier) or \
    isinstance(token, tok.Operator) or \
    isinstance(token, tok.Number) or \
    isinstance(token, tok.Not) or \
    isinstance(token, tok.And) or \
    isinstance(token, tok.Or) or \
    isinstance(token, tok.Equals) or \
    isinstance(token, tok.LeftParen)

def _is_operator(token: tok.Token):
  return \
    isinstance(token, tok.Operator) or \
    isinstance(token, tok.Not) or \
    isinstance(token, tok.And) or \
    isinstance(token, tok.Or) or \
    isinstance(token, tok.Equals)
  
def _get_operator_precedence(token: tok.Token) -> int:
  pass

def _get_operator_associativity(token: tok.Token) -> int:
  pass


class HeapNode:
  token_node: Node[tok.Token]

  def __lt__(self, other: 'HeapNode'):
    self_tuple = (
      _get_operator_precedence(self.token_node.val),
      _get_operator_associativity(self.token_node.val)
    )
    other_tuple = (
      _get_operator_precedence(other.token_node.val),
      _get_operator_associativity(other.token_node.val)
    )
    return self_tuple < other_tuple


def parse_expression(lexer: Lexer) -> Expression:
  token_list = LinkedList()
  operator_heap = []

  while _valid_token_type(lexer.peek()):
    next_token = lexer.next()

    if isinstance(next_token, tok.LeftParen):
      sub_expression = parse_expression(lexer)
      next_token = tok.ExpressionTreeToken(next_token.start, sub_expression)

      if not isinstance(lexer.peek(), tok.RightParen):
        raise Exception(f"Expected right parentheses. Got {lexer.peek()} instead")

    new_token_node = Node(next_token)
    token_list.append(new_token_node)

    if _is_operator(next_token):
      heapq.heappush(operator_heap, )
  


  