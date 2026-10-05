import language_types as lt
from collections import deque

class Memory:
  def __init__(self, initial_size: int):
    self.size = initial_size
    self._variable_to_address = {}
    self._memory = [None for _ in range(self.size)]
    self._types = [None for _ in range(self.size)]
    self._allocated_addresses = set()

  def _free_memory(self) -> bool:
    print("freeing")

    """
    returns if we were able to free up memory
    """
    reachable = set()
    for address in self._variable_to_address.values():
      reachable.add(address)

      frontier = deque() # all addresses ending up in frontier are reachable
      frontier.append(address)

      while len(frontier) > 0:
        curr_address = frontier.pop()

        if self._types[curr_address] == lt.Ptr and \
          (next_address := self._memory[curr_address]) not in reachable:
          frontier.append(next_address)
          reachable.add(next_address)

    reachable_unallocated_addresses = reachable - self._allocated_addresses
    assert len(reachable_unallocated_addresses) == 0, f"found addresses {reachable_unallocated_addresses} which are reachable but not allocated."
    before_length = len(self._allocated_addresses)
    self._allocated_addresses &= reachable
    after_length = len(self._allocated_addresses)

    return before_length > after_length

  def _allocate(self, var: lt.VarType, value, allocated_type: type):
    if len(self._allocated_addresses) == self.size:
      success = self._free_memory()

      if not success:
        raise Exception(f"Ran out of memory allocating variable {var} in memory instance {self}")

    for address in range(self.size):
      if address not in self._allocated_addresses:
        self._memory[address] = value
        self._variable_to_address[var] = address
        self._types[address] = allocated_type
        self._allocated_addresses.add(address)
        return

  def _assign(self, var: lt.VarType, value, allocated_type: type):
    if var in self._variable_to_address:
      address = self.get_memory_address_of_var(var)
      self._memory[address] = value
      self._types[address] = allocated_type

    else:
      self._allocate(var, value, allocated_type)

  def get_memory_address_of_var(self, var: lt.VarType) -> int:
    if var not in self._variable_to_address:
      raise Exception(f"Variable {var} could not be found.")
    
    return self._variable_to_address[var]

  def get_value_at_address(self, address: int) -> int:
    if address not in self._allocated_addresses:
      raise Exception(f"Address {address} not allocated in memory instance {self}")

    return self._memory[address]

  def get_variable_value_from_name(self, var: lt.VarType) -> int:
    return self.get_value_at_address(self.get_memory_address_of_var(var))
      
  def assign(self, var: lt.VarType, value):
    self._assign(var, value, type(value))

  def assign_pointer(self, var: lt.VarType, value: int):
    self._assign(var, value, lt.Ptr)

  def delete(self, var: lt.VarType):
    del self._variable_to_address[var]

