# -------------------------------
# Name: deque
# Author: Jasper Keijzer
# A custom implementation of pythons collections.deque
# Created: 24/04/2020
# Inspiration & source for large amount of code:
# TigerhawkT3
# https://github.com/TigerhawkT3/deque
# https://www.youtube.com/playlist?list=PLQ7bGgvf9FtFQ_E4g6Th2F45oY8qUzp65
# -------------------------------

class DQ:
	def __init__(self, *items, maxlen=None):
		self.maxlen = maxlen
		self.quantity = 0 # number of objects in this deque
		self.first = self.last = None
		for item in items:
			self.append(item)
	
	def append(self, item):
		temp = self.last # save current last node
		if temp:
			# current last.next = new last node (assignment left to right)
			self.last.next = self.last = Node(item)
			# new last prior = previous last node
			self.last.prior = temp
		else: # if the list is empty
			self.first = self.last = Node(item)
		self.quantity += 1
		if self.maxlen and self.quantity > self.maxlen:
			self.popleft()
		return self, item
	
	def pop(self):
		temp = self.last # save current last node
		if not temp: # if the deque is empty
			return self, None
		self.last = self.last.prior # new last node is current last.prior
		if self.last: # set new last.next to None
			self.last.next = None
		self.quantity -= 1
		if not self: # if we end up with an empty deque
			self.first = None
		return self, temp.element
	
	def appendleft(self, item):
		temp = self.first # save current first node
		if temp:
			# current first.prior = new first node (assignment left to right)
			self.first.prior = self.first = Node(item)
			# new first next = previous first node
			self.first.next = temp
		else: # if the list is empty
			self.first = self.last = Node(item)
		self.quantity += 1
		if self.maxlen and self.quantity > self.maxlen:
			self.pop()
		return self, item
	
	def popleft(self):
		temp = self.first # save current first node
		if not temp: # if the deque is empty
			return self, None
		self.first = self.first.next # new first node is current first.next
		if self.first: # set new first.prior to None
			self.first.prior = None
		self.quantity -= 1
		if not self: # if we end up with an empty deque
			self.last = None
		return self, temp.element
	
	def clear(self):
		self.last = self.first = None
		self.quantity = 0

	def copy(self):
		return DQ(*self)

	def count(self, item):
		return sum(item == element for element in self)
	
	def extend(self, other):
		for item in other:
			self.append(item)

	def extendleft(self, other):
		for item in other:
			# extendleft reverses item order due to multiple appendleft calls
			# extendleft([1,2,3]) to DQ(0) results in DQ(3,2,1,0)
			self.appendleft(item)
	
	def index(self, item, start=0, stop=0):
		# why no stop=self.quantity in function arguments?
		# default parameters are calculated when functions are defined
		# that would mean stop = self.quantity = 0 instead of updating
		# stop = self.quantity every time the function is called
		stop = stop or self.quantity
		for idx, val in enumerate(self):
			if val == item and start<=idx<stop:
				return idx
		raise ValueError(f'{repr(item)} is not in deque between index {start} and {stop}')

	def __str__(self):
		# join with commas the repro of each item
		return 'DQ({})'.format(', '.join(map(repr, self)))
	
	def __repr__(self):
		return repr(str(self))

	def __iter__(self):
		if not self.first: 
			return iter('')
		current = self.first
		while current:
			yield current.element
			current = current.next
	
	def __len__(self):
		return self.quantity
	
	def __bool__(self):
		# by default an instance of a user-defined class is truthy, however
		# we only want this deque to be truthy if it actually contains something
		return bool(self.quantity)

	def __add__(self, other):
		return DQ(*self, *other)

class Node:
	def __init__(self, element=None, *args):
		self.next = self.prior = None
		self.element = element
	
	def __str__(self):
		return str(self.element)
	
	def __repr__(self):
		# if self.prior has a node (self.prior and ..) will be truthy and return ...
		# if self.prior is None (self.prior and ..) will be falsy and return None
		# ... is the Ellipsis object
		return f'Node({repr(self.element)}, {self.prior and "..."}, {self.next and "..."})'

if __name__ == '__main__':
	d = DQ()
	print(d.append(1))
	print(d.append(2))
	print(d.append(3))
	print(d+d)
	print(d.appendleft(4))
	print(d.appendleft(5))
	print(d.appendleft(6))
	print(d.popleft())
	print(d.pop())
	print(d.append(7))
	print(d.appendleft(8))
	print(d.popleft())
	print(d.popleft())
	print(d.popleft())
	print(d.popleft())
	print(d.pop())
	print(d.pop())
	print(d.append(9))
	print(d.appendleft(10))
	print(d.popleft())
	print(d.pop())
	print(d.popleft())
	print(d.append(11))
	print(repr(d.last))
	print(d.append(12))
	print(repr(d.last))
	d.clear()
	d.extend([1,2,3])
	d.extendleft([3,4,5,6])
	print(d)
	e = d.copy()
	print(e)
	print(d.count(3), d.count(1), d.count(0))
	print(d.index(3))
	print(d.index(3, 4))
	print(d.index(0))
