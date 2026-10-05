from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class Node(Generic[T]):
  val: T
  prev: 'Node[T]' = None
  next: 'Node[T]' = None

@dataclass
class LinkedList(Generic[T]):
  head: Node[T] = None
  tail: Node[T] = None

  def append(self, node: Node[T]):
    if self.head == self.tail == None:
      self.head = self.tail = node
    else:
      self.tail.next = node
      node.prev = self.tail
      self.tail = self.tail.next

