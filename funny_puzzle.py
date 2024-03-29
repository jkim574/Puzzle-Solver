import heapq


class Solution:

	DEBUG = False

	succ_lookup = {
		(0, 0): [(0, 1), (1, 0)],
		(0, 1): [(0, 0), (0, 2), (1, 1)],
		(0, 2): [(0, 1), (1, 2)],
		(1, 0): [(0, 0), (1, 1), (2, 0)],
		(1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)],
		(1, 2): [(0, 2), (1, 1), (2, 2)],
		(2, 0): [(1, 0), (2, 1)],
		(2, 1): [(1, 1), (2, 0), (2, 2)],
		(2, 2): [(1, 2), (2, 1)]
	}
	# size means n in n x n board
	size = 3

	goal_coordinates = {
		1: (0, 0),
		2: (0, 1),
		3: (0, 2),
		4: (1, 0),
		5: (1, 1),
		6: (1, 2),
		7: (2, 0),
		8: (2, 1),
		0: (2, 2)
	}

	goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


	@staticmethod
	def get_r_c_tuple(index):
		"""Given a list index, return a tuple of (row, column)
		"""
		row = index // Solution.size
		column = index % Solution.size
		return (row, column)

	@staticmethod
	def swap(state, src, dst):
		"""Given a 1D list, swap the values in src and dst indices.
		src and dst indices are in (r, c) form.
		"""
		# Convert src and dst (r, c) form to list index
		src_idx = src[0] * Solution.size + src[1]
		dst_idx = dst[0] * Solution.size + dst[1]

		#print(f'Before swap: {state}')

		#print(src_idx, dst_idx)
		tmp = state[src_idx]
		state[src_idx] = state[dst_idx]
		state[dst_idx] = tmp

		#print(f'After swap: {state}')


	@staticmethod
	def manhattan(curr_coordinate, goal_coordinate):
		"""Calculate the manhattan distance from current coordinate (r,c) to goal coordinate (r,c)."""
		r1 = curr_coordinate[0]
		c1 = curr_coordinate[1]

		r2 = goal_coordinate[0]
		c2 = goal_coordinate[1]

		distance = abs(r2 - r1) + abs(c2 - c1)
		return distance


	@staticmethod
	def get_manhattan_distance(state):
		"""Given a state (1D Python List), calculate its manhattan distance value by summing up the manhattan distance of each tile
		"""
		total_sum = 0
		#print(f'State: {state}')
		for idx, tile in enumerate(state):
			if tile == 0:
				continue
			curr_coordinate = Solution.get_r_c_tuple(idx)
			goal_coordinate = Solution.goal_coordinates[tile]
			h = Solution.manhattan(curr_coordinate, goal_coordinate)
			#print(f'Tile {tile}: {curr_coordinate} -> {goal_coordinate} h = {h}')
			total_sum += h
		return total_sum


	@staticmethod
	def print_succ(state):
		sorted_succ_list = Solution.get_succ(state)
		for succ in sorted_succ_list:
			h = Solution.get_manhattan_distance(succ)
			print(f'{succ} h={h}')


	@staticmethod
	def get_succ(state):
		# Find the index of 0 from state (Python list)
		idx = state.index(0)
	#	print(f'index: {idx}')

		# Convert the index to (r, c) tuple
		index_tuple = Solution.get_r_c_tuple(idx)
	#	print(f'index tuple: {index_tuple}')

		# Look up successor indices from succ_lookup dictionary by using the (r, c) tuple
		succ_indices = Solution.succ_lookup[index_tuple]
	#	print(f'sucessor index tuples: {succ_indices}')

		succ_list = []
		# For each successor index, create a copy of state and swap the 0
		for swap_idx in succ_indices:
			state_cp = state[:]
			Solution.swap(state_cp, index_tuple, swap_idx)
			succ_list.append(state_cp)

		sorted_succ_list = sorted(succ_list)

		return sorted_succ_list


	@staticmethod
	def solver(state):
		moves = 0
		idx = 0
		idx_table = {}
		pq = []
		initial_g = 0
		initial_h = Solution.get_manhattan_distance(state)
		initial_parent_index = -1
		initial_priority = initial_g + initial_h
		heapq.heappush(pq, (initial_priority, state, (initial_g, initial_h, initial_parent_index)))
		visited = []

		while len(pq) > 0:
			state = heapq.heappop(pq)
			visited.append(state[1])
			if Solution.DEBUG:
				print(f'{idx} {state[1]}')
				#print(f'visited list: {visited}')
			if state[1] == Solution.goal_state:
	#			print("reached goal_state")
				break
			idx_table[idx] = state
			succ_states = Solution.get_succ(state[1])

			for succ in succ_states:
				if succ in visited:
					if Solution.DEBUG:
						print(f"{succ} already visited")
					continue
				h = Solution.get_manhattan_distance(succ)
				g = state[2][0] + 1
				parent_index = idx
				priority = g + h				heapq.heappush(pq, (priority, succ, (g, h, parent_index)))
				if Solution.DEBUG:
					print(f'\t{succ} h = {h}, g = {g}')
			moves += 1
			idx += 1

		if Solution.DEBUG:
			print(f'idx table: {idx_table}')

		stack = []
		curr_state = state
		parent_index = curr_state[2][2]
		if Solution.DEBUG:
			print(f'Parent index of goal state: {parent_index}')
			print(f'current state: {curr_state}')
		while parent_index != -1:
			stack.append(curr_state)
			curr_state = idx_table[parent_index]
			parent_index = curr_state[2][2]
			if Solution.DEBUG:
				print(f'Parent index: {parent_index}')
				print(f'state: {curr_state}')
		stack.append(curr_state)

		if Solution.DEBUG:
			print(stack)

		while len(stack) > 0:
			item = stack.pop()
			state = item[1]
			g = item[2][0]
			h = item[2][1]
			print(f'{state} h = {h} moves: {g}')




def print_succ(state):
	Solution.print_succ(state)

def solver(state):
	Solution.solver(state)




def main():
#	state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
#	state = [8,7,6,5,4,3,2,1,0]
#	state = [1,2,3,4,5,0,6,7,8]
	state = [4,3,8,5,1,6,7,2,0]
#	state = [1,2,3,4,5,6,7,0,8]
	#print_succ(state)

	solver(state)



if __name__ == '__main__':
	main()
