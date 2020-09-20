class Puzzle(object):
	def __init__(self, data, previous, moves):
		self.init = [] 
		self.goal = []
		self.data = data
		self.previous = previous
		self.moves = moves

	def add_stat(self, node):
		self.init.append(node)
		self.goal.append(node)

	def print_puzzle(self):
		for node in self.init:
			print('\t' + str(node)

	def __str__(self):
		return str(self.data)


if __name__ == '__main__':
	a = Puzzle('1')
	b = Puzzle('2')
	c = Puzzle('3')
	d = Puzzle('4')
	
	a.print_puzzle()
