# import re
# import numpy as np

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1] == '\n':
    data = data[:-1]

universe = data.split('\n')

expansion = 1000000

# detect the expanded columns
expanded_cols=set()
for col_index in range(len(universe[0])):
    # break
    col = {row[col_index] for row in universe}
    if '#' not in col:
        expanded_cols.add(col_index)

# detect the galaxy position in the expanded universe
galaxies = []
actual_row = 0
for row in universe:
    
    actual_col = 0
    row_galaxies=[]
    for col, dot in enumerate(row):
        if dot =='#':
            row_galaxies.append(actual_col)
        
        actual_col += expansion if col in expanded_cols else 1

    galaxies += [(actual_row, r) for r in row_galaxies]
    actual_row += expansion if len(row_galaxies)==0 else 1


shortest_paths_length=[]
for g1_index, g1 in enumerate(galaxies):
    for g2 in galaxies[g1_index:]:
        dist = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
        shortest_paths_length.append(dist)

solution = sum(shortest_paths_length)
print('Solution: ', solution)
