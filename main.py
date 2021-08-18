from typing import Optional, Tuple, List, Dict, TypeVar, Generic, Callable, Set
from enum import Enum

State = str

class Action(Enum):
	Left = (-1,0)
	Right = (1,0)
	Up = (0,-1)
	Down = (0,1)

	def __str__(self):
		return str(self.name)
	def __repr__(self):
		return str(self.name)

def successors(s: State) -> List[Tuple[Action, State]]:
	hole = s.index('_')
	y1 = hole//3
	x1 = hole%3
	results = []
	for a in Action:
		(x2,y2) = a.value
		x = x1+x2
		y = y1+y2
		if x < 0 or x > 3 or y < 0 or y > 3:
			continue
		ss = swap(s, hole, 3*y+x)
		if ss is not None:
			results.append((a,ss))
	return results


def swap(s: str, s1: int, s2: int) -> Optional[str]:
	try:
		ss = list(s)
		a  = ss[s1]
		ss[s1] = ss[s2]
		ss[s2] = a
		return "".join(ss)
	except:
		return None

class Node:
	def __init__(self,
			state: State,
			parent: Optional["Node"]=None,
			action: Optional[Action]=None,
			path_cost: int=0,
			children: Dict[Action, "Node"]={}):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.children = children

	def path(self):
		current = self
		path = []
		while current is not None:
			if current.action is not None:
				path.append(current.action)
			current = current.parent
		return list(reversed(path))

def expand(node: Node) -> List[Node]:
	return [Node(s,node,a,node.path_cost+1) for (a,s) in successors(node.state)]

T = TypeVar('T')
class Collection(Generic[T]):
	def __init__(self):
		pass
	def insert(self, v:T):
		pass
	def next(self) -> Optional[T]:
		pass
	def __iter__(self):
		return [].__iter__()

def solve(start: State, target: State, frontier: Collection) -> Optional[List[Action]]:
	visited: Set[State] = set()
	frontier.insert(Node(start))
	while True:
		v = frontier.next()
		if v is None:
			return None
		if v.state == target:
			return v.path()
		if v.state not in visited:
			visited.add(v.state)
			for n in expand(v):
				frontier.insert(n)

class Stack(Collection):
	def __init__(self):
		super().__init__()
		self.data = []

	def insert(self, v):
		self.data.append(v)

	def next(self):
		if self.data == []:
			return None
		return self.data.pop()
	def __iter__(self):
		return reversed(self.data)

class Queue(Collection):
	def __init__(self):
		super().__init__()
		self.data = []

	def insert(self,v):
		self.data.append(v)

	def next(self):
		if self.data == []:
			return None
		return self.data.pop(0)
	def __iter__(self):
		return self.data.__iter__()

def dfs(start: State, target: State) -> Optional[List[Action]]:
	return solve(start, target, Stack())

def bfs(start: State, target: State) -> Optional[List[Action]]:
	return solve(start, target, Queue())

def hamming(s: State) -> int:
	return sum([ 1 for (n,e) in enumerate(s) if (e == '_' and n != 8) or (n+1 != int(e) if e != '_' else False) ])

def manhattan(s: State) -> int:
	count = 0
	for (i,c) in enumerate(s):
		(x,y) = pos(c)
		count += abs(i//3 - x) + abs(i%3 - y)
	return count

def pos(c: str):
	if c == '_':
		c = '9'
	n = int(c)-1
	return (n//3, n%3)

class Priority(Collection):
	def __init__(self, f: Callable[[State], int]):
		super().__init__()
		self.data: List[Tuple[int, Node]]= []
		self.scoring: Callable[[State], int] = f

	def insert(self, v: Node):
		score = self.scoring(v.state) + v.path_cost
		i = 0
		for (p, _) in self.data:
			if p > score:
				break
			i += 1
		self.data.insert(i, (score, v))


	def next(self):
		if self.data == []:
			return None
		else:
			return self.data.pop(0)[1]
	def __iter__(self):
		return [n[1] for n in self.data].__iter__()


def astar_hamming(start, target):
	return solve(start, target, Priority(hamming))

def astar_manhattan(start, target):
	return solve(start, target, Priority(manhattan))
