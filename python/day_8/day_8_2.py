# import re
# import numpy as np
import math

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]


steps = 0

[sequence, points] = data.split('\n\n')

sequence = [0 if s =='L' else 1 for s in sequence]

base = [p.split(' = ') for p in points.split('\n')]

points_map = {b[0]: {'moves':b[1][1:-1].split(', ')} for b in base }

starts = [k for k in points_map.keys() if k.endswith('A') ]


# while loop does not work, let's be smarter

# compute the valid ending from each start
for start in points_map.keys():
    # break
    valid_steps = []
    pos = start
    step = 0
    for seq in sequence:
        step +=1
        pos = points_map[pos]['moves'][seq]
        # print( seq, pos)
        if pos.endswith('Z'):
            valid_steps.append(step)

    points_map[start]['valid_steps'] = valid_steps
    points_map[start]['ending'] = pos


valid_starting_sequence = [key for key, point in points_map.items() if len(point['valid_steps'])>0]

# we need to reach valid sequences
points_sequence = {}
for start in starts:
    # break
    visit = [points_map[start]['ending']]
    reached = [points_map[start]['valid_steps']]

    ind=1
    while True:
        p = visit[-1]
        new_visit = points_map[p]['ending']
        if new_visit in visit:
            break
        visit += [new_visit]
        reached += [[s+ind*len(sequence) for s in points_map[p]['valid_steps']]]
        ind += 1

    sequence_start = visit.index(new_visit)
    out_of_sequence = [item for row in reached[:sequence_start] for item in row]
    in_sequence = [item for row in reached[sequence_start:] for item in row]
    sequence_shift = len(sequence)*sequence_start


    points_sequence[start] = dict(
        sequence_start= sequence_start,
        # reached=reached,
        in_sequence=in_sequence,
        out_of_sequence=out_of_sequence,
        sequence_shift=sequence_shift,
    )


# need to find a way to be general but here, all sequence starts at 0, all sequence length = 1 so..

all_paths_length = [val['in_sequence'][0] for val in points_sequence.values()]
steps = math.lcm(*all_paths_length)
print('Solution: ', steps)