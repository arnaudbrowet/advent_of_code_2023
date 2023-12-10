# import re
import numpy as np

input_file = "small_input2.txt"
# input_file = "input.txt"
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

# create the map of the loop segments
loop_map = np.zeros(tubes.shape)
loop_map[starting_tube[0], starting_tube[1]] = 1

loop_map_indexed = np.zeros(tubes.shape)
loop_map_indexed[starting_tube[0], starting_tube[1]] = -1

loop_segments = []

steps = 1
for l in loop:
    pos = l['pos']
    loop_map[pos[0], pos[1]] = 1
    loop_map_indexed[pos[0], pos[1]] = steps

cur = starting_tube
cur_str = [c+0.5 for c in cur]
for l in loop:
    pos = l['pos']
    pos_str = [c+0.5 for c in pos]

    a=cur_str
    b=pos_str
    if (a[0] > b[0] or a[1]>b[1]):
        a=pos_str
        b=cur_str

    loop_segments.append(f'{a[0]},{a[1]};{b[0]},{b[1]}')


# print('loop', loop)

while (loop[0]['pos'][0] != loop[1]['pos'][0] or loop[0]['pos'][1] != loop[1]['pos'][1]):
    new_loop = []
    # if (steps==48):
    #     break

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

    # add loop segments
    for i in range(2):
        # break
        cur = loop[i]['pos']
        cur_str = [c+0.5 for c in cur]

        pos = new_loop[i]['pos']
        pos_str =[c+0.5 for c in pos]

        a=cur_str
        b=pos_str
        if (a[0] > b[0] or a[1]>b[1]):
            a=pos_str
            b=cur_str

        loop_segments.append(f'{a[0]},{a[1]};{b[0]},{b[1]}')

    loop = new_loop
    steps += 1

    # update loop map
    for p in loop:
        pos = p['pos']
        loop_map[pos[0], pos[1]] = 1
        loop_map_indexed[pos[0], pos[1]] = steps


# compute the number of crossing on each non loop point
# should be the same %2 in all directions, we choose top

# first floodfill to reduce number of tested points
nb_zeros = np.prod(loop_map.shape) - np.count_nonzero(loop_map)

nb_inside_points = 0
i, j = 2,19
for i in range(loop_map.shape[0]):
    for j in range(loop_map.shape[1]):
        p = loop_map[i, j]
        # print(i,j)
        if (p == 1):
            continue

        possible_crossings = [
            f'{k+0.5},{j-0.5};{k+.5},{j+.5}' for k in range(i)]

        valid_crossings = [c for c in possible_crossings if c in loop_segments]

        nb_crossings = len(valid_crossings)

        if nb_crossings % 2 == 1:
            # odd number of crossing is inside the loop
            # print("point inside:", i, j)
            nb_inside_points += 1


solution = nb_inside_points
print('Solution: ', solution)
