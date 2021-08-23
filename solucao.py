import heapq

Action = ["esquerda", "direita", "acima", "abaixo"]

def match(a):
	if a == "esquerda":
		return (-1,0)
	if a == "direita":
		return (1,0)
	if a == "acima":
		return (0,-1)
	if a == "abaixo":
		return (0,1)
	raise ValueError(a)

class Nodo:
	"""
	Implemente a classe Nodo com os atributos descritos na funcao init
	"""
	def __init__(self, estado, pai=None, acao=None, custo=0):
		"""
		Inicializa o nodo com os atributos recebidos
		:param estado:str, representacao do estado do 8-puzzle
		:param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
		:param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
		:param custo:int, custo do caminho da raiz até este nó
		"""
		self.estado = estado
		self.pai = pai
		self.acao = acao
		self.custo = custo
		self.chilren = {}

	def path(self):
		current = self
		path = []
		while current is not None:
			if current.acao is not None:
				path.append(current.acao)
			current = current.pai
		return list(reversed(path))

	def __lt__(self, other):
		return self.custo < other.custo


def swap(s, s1, s2):
	try:
		ss = list(s)
		a  = ss[s1]
		ss[s1] = ss[s2]
		ss[s2] = a
		return "".join(ss)
	except:
		return None

def sucessor(estado):
	"""
	Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
	para cada ação possível no estado recebido.
	Tanto a ação quanto o estado atingido são strings também.
	:param estado:
	:return:
	"""
	hole = estado.index('_')
	y1 = hole//3
	x1 = hole%3
	results = []
	for a in Action:
		(x2,y2) = match(a)
		x = x1+x2
		y = y1+y2
		if x < 0 or x > 2 or y < 0 or y > 2:
			continue
		ss = swap(estado, hole, 3*y+x)
		if ss is not None:
			results.append((a,ss))
	return results


def expande(nodo):
	"""
	Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
	Cada nodo do iterable é contém um estado sucessor do nó recebido.
	:param nodo: objeto da classe Nodo
	:return:
	"""
	return [Nodo(s, nodo, a, nodo.custo+1) for (a,s) in sucessor(nodo.estado)]

def solve(start, target, frontier):
	visited = set()
	frontier.insert(Nodo(start))
	while True:
		v = frontier.next()
		if v is None:
			return None
		if v.estado == target:
			return v.path()
		if v.estado not in visited:
			visited.add(v.estado)
			for n in expande(v):
				frontier.insert(n)

class Stack:
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

def bfs(estado):
	"""
	Recebe um estado (string), executa a busca em LARGURA e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	return solve(estado, "12345678_", Queue())

class Queue:
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

def dfs(estado):
	"""
	Recebe um estado (string), executa a busca em PROFUNDIDADE e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	return solve(estado, "12345678_", Stack())

def hamming(s) -> int:
	return sum([ 1 for (n,e) in enumerate(s) if (e == '_' and n != 8) or (n+1 != int(e) if e != '_' else False) ])

def manhattan(s) -> int:
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

class Priority:
	def __init__(self, f):
		super().__init__()
		self.data = []
		self.scoring = f

	def insert(self, v):
		score = self.scoring(v.estado) + v.custo
		heapq.heappush(self.data, (score, v))


	def next(self):
		if self.data == []:
			return None
		else:
			return heapq.heappop(self.data)[1]
	def __iter__(self):
		return [n[1] for n in self.data].__iter__()

def astar_hamming(estado):
	"""
	Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	return solve(estado, "12345678_", Priority(hamming))


def astar_manhattan(estado):
	"""
	Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
	retorna uma lista de ações que leva do
	estado recebido até o objetivo ("12345678_").
	Caso não haja solução a partir do estado recebido, retorna None
	:param estado: str
	:return:
	"""
	return solve(estado, "12345678_", Priority(manhattan))
