
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


def get_r_c_tuple(index):
	"""Given a list index, return a tuple of (row, column)
	"""
	row = index // size
	column = index % size
	return (row, column)

def swap(state, src, dst):
	"""Given a 1D list, swap the values in src and dst indices. 
	src and dst indices are in (r, c) form.
	"""
	# Convert src and dst (r, c) form to list index
	src_idx = src[0] * size + src[1] 
	dst_idx = dst[0] * size + dst[1]

	#print(f'Before swap: {state}')	

	#print(src_idx, dst_idx)
	tmp = state[src_idx]
	state[src_idx] = state[dst_idx]
	state[dst_idx] = tmp

	#print(f'After swap: {state}')



def manhattan(curr_coordinate, goal_coordinate):
	"""Calculate the manhattan distance from current coordinate (r,c) to goal coordinate (r,c)."""
	r1 = curr_coordinate[0] 
	c1 = curr_coordinate[1]

	r2 = goal_coordinate[0]
	c2 = goal_coordinate[1]

	distance = abs(r2 - r1) + abs(c2 - c1)
	return distance 


def get_manhattan_distance(state):
	"""Given a state (1D Python List), calculate its manhattan distance value by summing up the manhattan distance of each tile
	"""
	total_sum = 0
	#print(f'State: {state}')
	for idx, tile in enumerate(state):
		if tile == 0:
			continue
		curr_coordinate = get_r_c_tuple(idx)
		goal_coordinate = goal_coordinates[tile]
		h = manhattan(curr_coordinate, goal_coordinate)	
		#print(f'Tile {tile}: {curr_coordinate} -> {goal_coordinate} h = {h}')
		total_sum += h
	return total_sum


def print_succ(state):
	# Find the index of 0 from state (Python list)
	idx = state.index(0)
#	print(f'index: {idx}')

	# Convert the index to (r, c) tuple
	index_tuple = get_r_c_tuple(idx)
#	print(f'index tuple: {index_tuple}')

	# Look up successor indices from succ_lookup dictionary by using the (r, c) tuple
	succ_indices = succ_lookup[index_tuple]
#	print(f'sucessor index tuples: {succ_indices}')	
	
	succ_list = []
	# For each successor index, create a copy of state and swap the 0
	for swap_idx in succ_indices:
		state_cp = state[:]
		swap(state_cp, index_tuple, swap_idx)	
		succ_list.append(state_cp)
	
	sorted_succ_list = sorted(succ_list)

	#for item in sorted_succ_list:
	#	print(item)

	for succ in sorted_succ_list:
		h = get_manhattan_distance(succ)
		print(f'{succ} h={h}')



def solver(state):
	pass


def main():
	#state = [1, 2, 3, 4, 5, 6, 7, 0, 8]	
	state = [1,2,3,4,5,0,6,7,8]
	print_succ(state)
	'''
	for i in range(9):
		rc = get_r_c_tuple(i)
		print(rc)
	'''


if __name__ == '__main__':
	main()
