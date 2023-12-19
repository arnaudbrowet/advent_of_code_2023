import re
import math 

verbose = True


def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


input_file = "small_input.txt"
# input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts
workflowsDesc, partsDesc = data.split('\n\n')

workflowsList = [re.match(r'(\w+)\{(.+)\}', w).groups()
                 for w in workflowsDesc.split('\n')]
workflows = {w[0]: [{
    'key': t[0],
    'symbol': t[1],
    'value': int(t.split(':')[0][2:]),
    'next': t.split(':')[1]
} if ':' in t else {'next': t} for t in w[1].split(',')] for w in workflowsList}

keys = ['x', 'm', 's', 'a']
workflowIterator = [
    ('in', {k: [1, 4000] for k in keys})
]
solvedWorkflow = []

while workflowIterator:

    (workflowId, works) = workflowIterator.pop()
    print('** workflow', workflowId)

    workflow = workflows[workflowId]

    for step in workflow:
        # break
        nextStep = step['next']
        if 'key' in step:
            key = step['key']
            symbol = step['symbol']
            value = step['value']

            if nextStep == 'R':
                # rejected anyway
                continue

            w = {k: s.copy() for k, s in works.items()}
            if symbol == '<':
                w[key][1] = min(value-1, w[key][1])
                works[key][0] = max(value, works[key][0])
            else:
                w[key][0] = max(value+1, w[key][0])
                works[key][1] = min(value, works[key][1])

            if nextStep == 'A':
                solvedWorkflow.append(w)
            else:
                workflowIterator.append((nextStep, w))
        else:
            if nextStep == 'R':
                continue
            if nextStep == 'A':
                solvedWorkflow.append(works)
            else:
                workflowIterator.append((nextStep, works))

    print('solved')
    print(solvedWorkflow)

    print('iterator')
    for w in workflowIterator:
        print(w)
    print()

nbSolutions = 0
for workflow in solvedWorkflow:
    score = []
    for key in keys:
        score.append(
            workflow[key][1]-workflow[key][0]+1
        )
    print(score, math.prod(score))
    nbSolutions += math.prod(score)

for s in solvedWorkflow:
    print(s)
print('Solution (found):', nbSolutions)
print('Solution (small):', 167409079868000)