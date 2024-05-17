# Solver for KenKen puzzles (version 3)
#
# We represent the set of possible values in a solution's cells as a string
# of integers; this approach only works for problems with N <= 9
import	string


# Return first non-false value, or False
def first(iterable):
	for i in iterable:
		if (i): return i
	return False

# Can we select exactly one member from each set s.t. the sum of all selected members is t?
d_sum_queries = {}
def can_make_sum_p(t, sets):
	if (len(sets) == 1): return (t in sets[0])
	r = d_sum_queries.get((t, sets))
	if (r == None):
		head = sets[0]; tail = sets[1:]
		r = any(can_make_sum_p(t-e, tail) for e in head if e <= t)
		d_sum_queries[(t, sets)] = r
	return r

# Can we select exactly one member from each set s.t. the product of all selected members is t?
d_prod_queries = {}
def can_make_product_p(t, sets):
	if (len(sets) == 1): return (t in sets[0])
	r = d_prod_queries.get((t, sets))
	if (r == None):
		head = sets[0]; tail = sets[1:]
		r = any(can_make_product_p(t/e, tail) for e in head if not t%e)
		d_prod_queries[(t, sets)] = r
	return r


def print_solution(s):
	if (not s):
		print(s)
		return
	rows	= list(set(k[0] for k in s.keys())); rows.sort()
	cols	= list(set(k[1] for k in s.keys())); cols.sort()
	max_len = max(map(len, s.values()))
	row_div = '\n' + '-+-'.join('-'*max_len for c in cols) + '\n'
	print(row_div.join(' | '.join(str.center(s[r+c], max_len) for c in cols) for r in rows))


class Constraint(object):
	def __init__(self, value, *cells):
		self.cells	= set(cells)
		self.value	= int(value)
	def _test_component(self, component, context):
		return True
	def apply(self, solution):
		l_sets = [(c, tuple(map(int, solution[c]))) for c in self.cells]
		l_good = []
		for k, values in l_sets:
			others = tuple(ov for ok, ov in l_sets if ok != k)
			l_good.append((k, ''.join(str(e) for e in values if self._test_component(e, others))))
		return l_good

class Assert(Constraint):
	def apply(self, solution):
		v = str(self.value)
		return ((c, v) for c in self.cells)
	
class Sum(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) < 2): raise Exception('Sum constraints must be applied to 2 or more cells')
	def _test_component(self, component, context):
		return (self.value>=component) and can_make_sum_p(self.value-component, context)

class Diff(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) != 2): raise Exception('Diff constraints must be applied to pairs of cells')
	def _test_component(self, component, context):
		return (self.value+component in context[0]) or (component-self.value in context[0])

class Prod(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) < 2): raise Exception('Prod constraints must be applied to 2 or more cells')
	def _test_component(self, component, context):
		return (not self.value%component) and can_make_product_p(self.value/component, context)

class Div(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) != 2): raise Exception('Div constraints must be applied to pairs of cells')
	def _test_component(self, component, context):
		return (self.value*component in context[0]) or (float(component)/self.value in context[0])

class Set(Constraint):
	def _remove(self, l_good, cell, value):
		for p in l_good:
			if (p[0] == cell): continue
			if (value in p[1]):
				p[1] = p[1].replace(value, '')
				if (len(p[1]) == 1):
					self._remove(l_good, *p)
	def apply(self, solution):
		# For each cell:
		l_good = [[c, solution[c]] for c in self.cells]
		for c,v in l_good:
			# If a cell has only one possible value, remove that value from all other cells
			if (len(v) == 1): self._remove(l_good, c, v)
		return l_good


class Puzzle:
	lut = {'.':Assert, '+':Sum, '-':Diff, '*':Prod, '/':Div}
	def __init__(self, size, lines):
		self.size	= size
		self.cages	= [self.lut[l[1]](l[2], *l[0]) for l in lines]


def solve(puzzle: Puzzle, exhaustive: bool = False, assignements: list = []):
	# Derived from the problem size
	size = puzzle.size
	square_sets = []
	for i in range(1, 4):
		for j in range(1, 4):
			square_sets.append(
				Set(
					0, *((i + k, j + l) for k in range(3) for l in range(3))))
	sets = [Set(0, *((r, c) for r in range(1, size + 1))) for c in range(1, size + 1)] + \
		   [Set(0, *((r, c) for c in range(1, size + 1))) for r in range(1, size + 1)] + \
		   square_sets
	# Cell -> constraint mapping
	d_constraints = dict(((r, c), set()) for r in range(1, size + 1) for c in range(1, size + 1))
	for constraint in sets + puzzle.cages:
		for cell in constraint.cells:
			d_constraints[cell].add(constraint)
	# Helper: Given a partial solution, apply (potentially) unsatisfied constraints
	def constrain(solution: list, *constraints):
		queue = set(constraints)
		while (queue):
			constraint = queue.pop()
			for cell, values in constraint.apply(solution):
				if (not values):
					print(cell)
					print(values)
					print(constraint)
					return False
				if (solution[cell] == values):
					continue
				solution[cell] = values
				queue.update(d_constraints[cell])
			queue.discard(constraint)
		return solution
	# Helper: Given a partial solution, force one of its cells to a given value
	def assign(solution: list, cell: "tuple[int, int]", value: int):
		solution[cell] = value
		return constrain(solution, *d_constraints[cell])
	# Helper: Recursively refine a solution with search and propogation
	def search(solution):
		# Check for trivial cases
		if ((not solution) or all(len(v)==1 for v in solution.values())):
			return solution
		# Find a most-constrained unsolved cell
		cell = min((len(v),k) for k,v in solution.items() if len(v)>1)[1]
		# Try solutions based upon exhaustive guesses of the cell's value
		return first(search(assign(solution.copy(), cell, h)) for h in solution[cell])
	# Helper: Recursively refine a solution with search and propogation
	def search_ex(solution):
		# Check for trivial cases
		if (not solution):
			return []
		if all(len(v)==1 for v in solution.values()):
			return [solution]
		# Find a most-constrained unsolved cell
		cell = min((len(v),k) for k,v in solution.items() if len(v)>1)[1]
		# Try solutions based upon exhaustive guesses of the cell's value
		rv = []
		for h in solution[cell]: rv.extend(search_ex(assign(solution.copy(), cell, h)))
		return rv
	# Solve
	d_sum_queries = {}
	d_prod_queries = {}
	symbols = string.digits[1:1+puzzle.size]
	if (exhaustive):
		fxn = search_ex
	else:
		fxn = search

	solution = constrain(dict((c,symbols) for c in d_constraints.keys()), *puzzle.cages)
	print(solution)
	for assignement in assignements:
		assign(solution, assignement[0], assignement[1])

	return fxn(solution)