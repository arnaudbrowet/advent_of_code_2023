# import re
# import numpy as np

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1] == '\n':
    data = data[:-1]

universe = data.split('\n')

# expand the univers
# expand rows


def expansion(u): return sum(
    [[row] if "#" in row else [row, row] for row in u],
    [],
)


universe_expanded_rows = expansion(universe)


def transpose_universe(u): return [
    ''.join([u[row][col] for row in range(len(u))]) for col in range(len(u[0]))
]


universe_transposed = transpose_universe(universe_expanded_rows)
universe_expanded_cols = expansion(universe_transposed)

universe_expanded = transpose_universe(universe_expanded_cols)


# detect galaxy
galaxies = []
for row_index, row in enumerate(universe_expanded):
    # break
    for col_index, col in enumerate(row):
        # break
        if col == '#':
            galaxies.append([row_index, col_index])

shortest_paths_length=[]
for g1_index, g1 in enumerate(galaxies):
    for g2 in galaxies[g1_index:]:
        dist = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
        shortest_paths_length.append(dist)

solution = sum(shortest_paths_length)
print('Solution: ', solution)
