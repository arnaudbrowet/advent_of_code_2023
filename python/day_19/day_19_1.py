import re

verbose = True


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
workflowsDesc, partsDesc = data.split('\n\n')

workflowsList = [re.match(r'(\w+)\{(.+)\}', w).groups() for w in workflowsDesc.split('\n')]
workflows = {w[0] : [ {
    'key':t[0],
    'symbol':t[1],
    'value': int(t.split(':')[0][2:]),
    'next': t.split(':')[1]
} if ':' in t else {'next':t} for t in w[1].split(',') ] for w in workflowsList}

parts = [{v[0]:int(v[2:]) for v in p[1:-1].split(',')} for p in partsDesc.split('\n')]

# part 2 - test
# parts = [dict(x=2000,m=1000,s=1000,a=2000)]
accepted = []
for part in parts:
    # break
    pos = 'in'

    while pos != 'A' and pos != 'R':
        workflow = workflows[pos]

        for step in workflow:
            if 'key' not in step:
                pos = step['next']
            else:
                key = step['key']
                symbol = step['symbol']
                value = step['value']

                isValid = part[key] > value if symbol == '>' else part[key]<value
                
                if isValid:
                    pos = step['next']
                    break
        
    if pos == 'A':
        accepted.append(
            sum(part.values())
        )
    
print('Solution:', sum(accepted))