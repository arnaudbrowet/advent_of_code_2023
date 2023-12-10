# import re
import numpy as np

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1] == '\n':
    data = data[:-1]


move_map = {

    '|': dict(
        has_down=True,
        has_up=True,
        has_left=False,
        has_right=False,
        from_top=dict(
            move=[1, 0],
            next='from_top'
        ),
        from_bottom=dict(
            move=[-1, 0],
            next='from_bottom'
        ),
    ),
    '-': dict(
        has_down=False,
        has_up=False,
        has_left=True,
        has_right=True,
        from_left=dict(
            move=[0, 1],
            next="from_left"
        ),
        from_right=dict(
            move=[0, -1],
            next="from_right"
        ),
    ),
    'L': dict(
        has_down=False,
        has_up=True,
        has_left=False,
        has_right=True,
        from_top=dict(
            move=[0, 1],
            next="from_left"
        ),
        from_right=dict(
            move=[-1, 0],
            next="from_bottom"
        ),
    ),
    'J': dict(
        has_down=False,
        has_up=True,
        has_left=True,
        has_right=False,
        from_top=dict(
            move=[0, -1],
            next="from_right",
        ),
        from_left=dict(
            move=[-1, 0],
            next="from_bottom",
        ),
    ),
    '7': dict(
        has_down=True,
        has_up=False,
        has_left=True,
        has_right=False,
        from_bottom=dict(
            move=[0, -1],
            next='from_right'
        ),
        from_left=dict(
            move=[1, 0],
            next="from_top"
        ),
    ),
    'F': dict(
        has_down=True,
        has_up=False,
        has_left=False,
        has_right=True,
        from_bottom=dict(
            move=[0, 1],
            next="from_left"
        ),
        from_right=dict(
            move=[1, 0],
            next="from_top"
        ),
    ),
}
tubes = np.array([[c for c in s] for s in data.split('\n')])

(nb_rows, nb_cols) = tubes.shape


(x, y) = np.where(tubes == 'S')

starting_tube = [x[0], y[0]]

# check
v0 = tubes[starting_tube[0], starting_tube[1]]
if (v0 != 'S'):
    raise Exception('invalid starting point')


# find the direction of the main loop
loop = []

if starting_tube[0] > 0:
    top_pos = starting_tube[0]-1, starting_tube[1]
    top = tubes[top_pos[0], top_pos[1]]
    if move_map[top]['has_down']:
        loop.append(dict(
            pos=top_pos,
            dir='from_bottom'
        ))

if (starting_tube[0] < nb_rows-1):
    bottom_pos = starting_tube[0]+1, starting_tube[1]
    bottom = tubes[bottom_pos[0], bottom_pos[1]]
    if move_map[bottom]['has_up']:
        loop.append(dict(
            pos=bottom_pos,
            dir='from_top'
        ))

if (starting_tube[1] > 0):
    left_pos = starting_tube[0], starting_tube[1]-1
    left = tubes[left_pos[0], left_pos[1]]
    if move_map[left]['has_right']:
        loop.append(dict(
            pos=left_pos,
            dir='from_right'
        ))

if (starting_tube[1] < nb_cols-1):
    right_pos = starting_tube[0], starting_tube[1]+1
    right = tubes[right_pos[0], right_pos[1]]
    if move_map[right]['has_left']:
        loop.append(dict(
            pos=right_pos,
            dir='from_left'
        ))

if len(loop) != 2:
    raise Exception('invalid loop length')

# print('loop', loop)
steps = 1
while (loop[0]['pos'][0] != loop[1]['pos'][0] or loop[0]['pos'][1] != loop[1]['pos'][1]):
    new_loop = []

    for l in loop:
        # break
        n = l['pos']
        char = tubes[n[0], n[1]]
        move = move_map[char][l['dir']]

        new_n = n[0]+move['move'][0], n[1]+move['move'][1]
        # print(n, char,l['dir'], move, new_n)
        new_loop.append(dict(
            pos=new_n,
            dir=move['next']
        ))
    # print('loop', new_loop)
    loop = new_loop
    steps += 1



solution=steps
print('Solution: ', solution)
