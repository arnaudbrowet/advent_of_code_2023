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
map = {}
rows = data.split('\n')
nbRows = len(rows)
nbCols = len(rows[0])
for i, row in enumerate(rows):
    for j, p in enumerate(row):
        if p != '#':
            map[(i, j)] = p
            if i == 0:
                start = (i, j)
            if i == len(rows)-1:
                end = (i, j)

shifts = {
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
}

# detect intersection
neighbours = {}
for node, symbol in map.items():
    nodeNeighbours = set()
    for shift in shifts:
        # break
        dest = (node[0]+shift[0], node[1]+shift[1])
        if dest in map:
            nodeNeighbours.add(shift)

    neighbours[node] = nodeNeighbours

intersections = {
    start: neighbours[start],
    end: neighbours[end],
}
for node, nodeNeighbours in neighbours.items():
    if len(nodeNeighbours) > 2:
        intersections[node] = nodeNeighbours

# compute long edges
longEdges = {
    k: {} for k in intersections.keys()
}
visited = {}
for node, nodeDirections in intersections.items():
    # break
    allowedShifs = nodeDirections
    if node in visited:
        allowedShifs = allowedShifs - visited[node]

    # follow the path
    for shift in allowedShifs:
        # break
        dest = (node[0]+shift[0], node[1]+shift[1])
        l = 1
        s = shift
        while dest not in intersections.keys():
            newShift = neighbours[dest] - {(-s[0], -s[1])}
            if len(newShift) > 1:
                raise Exception('invalid, should be an intersection')
            s = list(newShift)[0]
            dest = (dest[0]+s[0], dest[1]+s[1])
            l += 1

        if dest in visited:
            visited[dest].add((-s[0], -s[1]))
        else:
            visited[dest] = {(-s[0], -s[1])}

        longEdges[node][dest] = l
        longEdges[dest][node] = l

def pathExists(s, e, G):
    if s == e:
        return True
    
    visited = set([s])
    queue = [s]
    found = False
    while queue and not found:
        node = queue.pop(0)

        for target in G[node].keys():
            if target == e:
                found = True
                break
            if target in visited:
                continue
            visited.add(target)
            queue.append(target)

    return found


def trimGraph(n, G):
    # edges = G[n]

    newG = {
        N: {
            T:l for T, l in E.items() if T!=n
        } for N, E in G.items() if N!=n
    }
    return newG


def getMaxPath(s, e, G):
    if s == e:
        return 0

    edges = G[s]
    newG = trimGraph(s,G)

    s = []
    for target, length in edges.items():
        # print(target, length)
        # printGraphViz(newG)
        if pathExists(target, e, newG):
            s.append(
                length + getMaxPath(target, e, newG)
            )
    return max(s)

maxLength = getMaxPath(start,end, longEdges)

# Graph viz
def printGraphViz(G):
    nodeMap={
        node: i for i, node in enumerate(G.keys())
    }
    for node, edges in G.items():
        
        nodeName = nodeMap[node]
        
        print(f"A{nodeName} [")
        print(f'label = "({node[0]},{node[1]})"')
        print(f'pos = "{node[0]},{node[1]}!"')
        print(']')

        for edge, edgeLength in edges.items():
            print(f'A{nodeName} ->A{nodeMap[edge]} [label="{edgeLength}"];')

# printGraphViz(longEdges)


print('Solution:', maxLength)
