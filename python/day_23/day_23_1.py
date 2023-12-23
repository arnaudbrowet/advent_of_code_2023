# from heapq import heappush, heappop

verbose = False


def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts
start = None
end = None
map={}
rows = data.split('\n')
for i, row in enumerate(rows):
    for j, p in enumerate(row):
        if p != '#':
            map[(i,j)]=p
            if i==0:
                start = (i,j)
            if i == len(rows)-1:
                end = (i,j)

shifts = [
    (1, 0),
    (-1, 0),
    (0,1),
    (0,-1),
]
symbolShift = {
    '^':(-1,0), 
    '>':(0,1), 
    'v':(1,0),
    '<': (0,-1)
}
edges={}
for node, symbol in map.items():
    if symbol != '.':
        continue

    edges[node] = {}
    for shift in shifts:
        # break
        edgeLength = 1
        dest = (node[0]+shift[0], node[1]+shift[1])
        if dest not in map:
            continue
        symb = map[dest]
        
        while symb != '.':
            slip = symbolShift[symb]
            dest = (dest[0]+slip[0], dest[1]+slip[1])
            edgeLength += 1
            symb = map[dest]

        edges[node][dest] = edgeLength

    
paths = [
    # pos, visited, length
    (start, {start}, 0)
]
sol = []
while paths:
    pos, visited, length = paths.pop(0)

    for target, edgeLength in edges[pos].items():
        if target == end:
            sol.append(
                # (length + edgeLength, {*visited, target} )
                length + edgeLength
            )
            continue
        if target not in visited:
            paths.append(
                (target, {*visited, target}, length+edgeLength)
            )

print('Solution:', max(sol))