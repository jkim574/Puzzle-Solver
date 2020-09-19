import heapq
import numpy as np

DEBUG = False
DEBUG_L2 = False

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state_ndarr = np.array(goal_state).reshape(3, 3)
tile_to_index = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1)
}
index_swap = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(0, 0), (0, 2), (1, 1)],
    (0, 2): [(0, 1), (1, 2)],
    (1, 0): [(0, 0), (1, 1), (2, 0)],
    (1, 1): [(0, 1), (1, 0), (1, 2), (2, 1)],
    (1, 2): [(0, 2), (1, 1), (2, 2)],
    (2, 0): [(1, 0), (2, 1)],
    (2, 1): [(1, 1), (2, 0), (2, 2)],
    (2, 2): [(2, 1), (1, 2)]
}
states_visited = []


class State(object):
    def __init__(self, state, heuristics=0):
        self._state = state
        self._successors = []
        self._heuristics = heuristics

    def add_successor(self, succ):
        self._successors.append(succ)

    @property
    def successors(self):
        return self._successors

    @property
    def state(self):
        return self._state

    def __str__(self):
        return f'{self._state} h={self._heuristics}'


def manhattan_distance(data_point1, data_point2):
    x1 = data_point1[0]
    x2 = data_point2[0]

    y1 = data_point1[1]
    y2 = data_point2[1]

    d = abs(x1 - x2) + abs(y1 - y2)
    return d


def find_heuristic(state):
    """Given a state, return the sum of Manhattan distance of eahc tile
    to its goal position."""
    #state = np.array([1, 2, 0, 4, 5, 3, 6, 7, 8]).reshape(3, 3)
    #state = np.array([2, 5, 8, 4, 3, 6, 7, 1, 0]).reshape(3, 3)
    #print(state)
    distances = []
    state = np.array(state).reshape(3, 3)
    it = np.nditer(state, flags=['multi_index'])
    for tile in it:
        tile = int(tile)
        if tile == 0:
            continue
        curr_index = it.multi_index
        goal_index = tile_to_index[tile]
        dist = manhattan_distance(curr_index, goal_index)
        distances.append(dist)
        #print(f'Tile {tile} {curr_index} -> {goal_index}: h = {dist}')
    return sum(distances)


def find_succ(state):
    state = np.array(state).reshape(3,3)
    curr_state = State(state)
    #print(state)
    zero_index = np.where(state == 0)
    zero_index = (zero_index[0][0], zero_index[1][0])
    #print(zero_index)

    # First get a list of successors (lists) sorted in order before creating State class
    succ_list = []
    for swap_index in index_swap[zero_index]:
        #print(f'Swap index: {swap_index}')
        succ = state.copy()
        swap_values(succ, zero_index, swap_index)
        #print(succ)
        succ_list.append(list(succ.reshape(9)))
    succ_list = sorted(succ_list)

    for succ in succ_list:
        #succ = np.array(succ).reshape(3,3)
        h = find_heuristic(succ)
        succ_state = State(succ, h)
        curr_state.add_successor(succ_state)

    return curr_state.successors


def swap_values(array, a, b):
    temp = array[a[0]][a[1]]
    array[a[0]][a[1]] = array[b[0]][b[1]]
    array[b[0]][b[1]] = temp


def print_succ(state):
    succs = find_succ(state)
    for succ in succs:
        print(succ)


def in_states_visited(state):
    for s in states_visited:
        if state[1] == s[1]:
            return True
    return False


def solve(state):
    g = 0  # for initial state
    h = find_heuristic(state)
    parent_index = -1  # for initial state

    pq = []
    heapq.heappush(pq, (g + h, state, (g, h, parent_index)))

    moves = 0
    iter = 0
    stat_count = 0
    max_queue_length = len(pq)
    while pq:
        curr_state = heapq.heappop(pq)
        if DEBUG:
            print(f'[Iter {iter}]')
            print('Current state:')
            print(curr_state)
        if in_states_visited(curr_state):
            if DEBUG:
                print('State already explored.')
                #print('States visited:')
                #print(f'{states_visited}')
                print(f'Total {len(states_visited)} states visited.\n')
                #exit()
            continue
        states_visited.append(curr_state)
        #print('States visited:')
        #print(states_visited)

        if curr_state[1] == goal_state:
            if DEBUG:
                print('Found Goal state\n')
            break

        if DEBUG:
            if DEBUG_L2:
                print('Successor states:')
        successors = find_succ(curr_state[1])
        parent_index += 1
        moves = curr_state[2][0] + 1

        if DEBUG:
            print(f'Index: {parent_index}')

        for succ in successors:
            g = moves
            h = find_heuristic(succ.state)
            heapq.heappush(pq, (g + h, succ.state, (g, h, parent_index)))
            if DEBUG:
                if DEBUG_L2:
                    print((g + h, succ.state, (g, h, parent_index)))

        if len(pq) > max_queue_length:
            max_queue_length = len(pq)

        if DEBUG:
            if DEBUG_L2:
                print('Priority Queue:')
                print(*pq, sep='\n')
            print(f'Max queue length: {max_queue_length}')
            print()

        iter += 1
        #input()
        # if iter == 23:
        #     exit()

    # Push states on solution path on the stack
    stack = []
    parent_index = curr_state[2][2]
    while True:
        stack.append(curr_state)
        if parent_index == -1:
            break
        curr_state = states_visited[parent_index]
        parent_index = curr_state[2][2]

    if DEBUG:
        print('*' * 45)
    # Pop states off of stack and print the solution
    while len(stack) > 0:
        item = stack.pop()
        state = item[1]
        h = item[2][1]
        moves = item[2][0]
        print(f'{state} h={h} moves: {moves}')
    print(f'Max queue length: {max_queue_length}')


def main():
    # This state completes in 1 move; max queue length: 3; 2 iterations
    #state = [1,2,3,4,5,6,7,0,8]

    # This state completes in 13 moves; max queue length: 59; 56 iterations
    #state = [1,2,3,4,5,0,6,7,8]

    # This state completes in 30 moves; max queue length: 7367; 7550 iterations
    #state = [8,7,6,5,4,3,2,1,0]

    # This state completes in 22 moves; max queue length: 581; 654 iterations
    state = [4,3,8,5,1,6,7,2,0]

    solve(state)



if __name__ == '__main__':
    main()
