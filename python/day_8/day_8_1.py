# import re
import numpy as np
import functools

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]


steps = 0

[sequence, points] = data.split('\n\n')

base = [p.split(' = ') for p in points.split('\n')]

points_map = {b[0]: b[1][1:-1].split(', ') for b in base }

pos = 'AAA'

cur_step = 0
while pos !='ZZZ':
    next = sequence[cur_step]
    
    pos = points_map[pos][1 if next == 'R' else 0]
    cur_step = (cur_step+1)%len(sequence)
    steps+=1
    
    

print('Solution: ', steps)