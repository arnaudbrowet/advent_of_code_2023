import re

verbose = True


def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


# input_file = "small_input2.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts


def printDig(digMap, xlimits, ylimits):
    nbItems = len(digMap[next(iter(digMap))])
    # print(nbItems)
    for i in range(ylimits[0], ylimits[1]+1):
        row = ''
        # row = []
        for j in range(xlimits[0], xlimits[1]+1):
            # row += "#" if (i, j) in digMap else '.'
            row += digMap[(i, j)] if (i, j) in digMap else '.'*nbItems
            # row += [digMap[(i,j)]] if (i, j) in digMap else [['.', '.']]
        vprint(row)


steps = data.split('\n')
directionMap = {
    'R': ((0, 1), '>'),
    'L': ((0, -1), '<'),
    'D': ((1, 0), 'v'),
    'U': ((-1, 0), '^'),
}
digs = {
    (0, 0): ''
}

xlimits = (0, 0)
ylimits = (0, 0)
point = (0, 0)
for step in steps:
    # break
    direction, nbDig, color = re.match(r'(\w) (\d+) \(#(\w+)\)', step).groups()

    dir, symbol = directionMap[direction]

    # if direction in ('U', 'D'):
    # digs[point] += symbol

    for _ in range(int(nbDig)):

        newPoint = (point[0]+dir[0], point[1]+dir[1])

        # if (point in digs):
        #     raise Exception('point already digged')
        # digs[point] = symbol
        if newPoint in digs:
            digs[newPoint] = symbol + digs[newPoint]
        else:
            digs[newPoint] = symbol

        digs[point] += symbol
        point = newPoint

        xlimits = (
            min(xlimits[0], point[1]),
            max(xlimits[1], point[1])
        )
        ylimits = (
            min(ylimits[0], point[0]),
            max(ylimits[1], point[0])
        )
    # break

digBoundary = { k:'#' for k in digs.keys()}
# printDig(digs, xlimits, ylimits)
# printDig(digBoundary, xlimits, ylimits)

# compute inside points
filledDigs = {
    k:'#' for k in digs.keys()
}
downMap = [
    'vv',
    '^<','^>', '^^',
    '>v',
    '<v',
]
for i in range(ylimits[0], ylimits[1]+1):
    inside = False
    # break
    for j in range(xlimits[0], xlimits[1]+1):
        # print(i,j, inside)
        # break
        if (i, j) in digs:
            # filledDigs[(i, j)] = '#'
            dig = digs[(i, j)]
            # print(dig)

            hasDown = dig in downMap

            if hasDown:
                inside = not inside

        else:
            if inside:
                filledDigs[(i, j)] = '#'

printDig(filledDigs, xlimits, ylimits)

print('Solution:', len(filledDigs))
