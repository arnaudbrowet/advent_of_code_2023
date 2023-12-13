import re
# import numpy as np

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1] == '\n':
    data = data[:-1]

verbose = False
def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


nb_arrangments = []
rows = data.split('\n')

def is_valid_sub_pattern(base_pattern, sol):
        is_valid = True
        for i in range(len(base_pattern)):
            if base_pattern[i] == "#" and sol[i]!='#':
                is_valid=False
                break
        return is_valid

# iterate on each row of springs
row_iterator = rows
# row_iterator = rows[19:20]
# row_iterator = [rows[27]]
row_iterator = ["?#?????#?##.??#???? 2,5,4,1"]
# s='?###?????.???.# 3,2,1,2,1'.split(' ')# 
# k=1
# row_iterator=['?'.join([s[0]]*k) + ' '+','.join([s[1]]*k)]
for row in row_iterator:
    # break
    (springs, runs) = row.split(' ')
    
    # find groups of springs & run length
    groups = re.findall('([\?#]+)', springs)
    runs_length = [int(r) for r in runs.split(',')]

    # start possible pattern
    patterns = [
        (groups, runs_length, [])
    ]
    groups_length = [len(group) for group in groups]
    total_len = sum(groups_length)

    row_solutions = []

    while len(patterns) > 0:

        vprint()
        vprint(patterns)

        group, run_length, history = patterns.pop(0)
        group = group.copy()
        run_length = run_length.copy()
        history = history.copy()

        vprint('group:', group)
        vprint("run_length:", run_length)
        vprint('history:', history)

        # check that we did not loose a character in the pattern
        full_pattern = (history + group).copy()
        if len(''.join(full_pattern)) != total_len:
            raise Exception('invalid history')

        # if there is nothing in the run, we fit everything
        # check if the fit is valid
        if len(run_length) == 0:
            # break
            remaining = ''.join(group)

            # if there is # remaining the matching can not be valid
            if ('#' not in remaining):
                
                hist = ''.join(history)
                hist += '.'*(len(remaining))

                row_solution = []
                for nb in groups_length:
                    row_solution += [hist[:nb]]
                    hist = hist[nb:]

                vprint(history)
                vprint(row_solution)
                vprint()

                row_solutions.append(tuple(row_solution))

            continue

        # so we still have some match to do

        # if we don't have any more groups, skip the run
        if len(group) == 0:
            continue

        current_group = group.pop(0)
        current_run = run_length.pop(0)

        # if the group is shorter than the run, we can not fit here
        if len(current_group) < current_run:
            # the run does not fit in the group
            
            # if it did not contain # then it can be skipped
            vprint('run too small')
            if ("#" not in current_group):
                history.append('.'*len(current_group))
                adder = (group, [current_run]+run_length, history)
                patterns.append(
                    adder
                )
            continue

        # we can match in this group

        # try a match at the beginning
        remaining_just_after_group = current_group[current_run:]
        is_fit = len(remaining_just_after_group) == 0
        if not is_fit:
            if remaining_just_after_group[0] == '?':
                is_fit = True

        if is_fit:

            new_history = history.copy()
            new_history.append('#'*current_run + '.' *
                               (1 if len(remaining_just_after_group) > 0 else 0))

            remaining = group
            if len(remaining_just_after_group) > 1:
                remaining = [remaining_just_after_group[1:]] + group

            adder = (remaining, run_length, new_history)
            vprint("adder following in current", adder)
            patterns.append(
                adder
            )

        # otherwise, allow a potential match later
        if len(current_group) >= current_run and current_group[0] != '#':

            new_history = history.copy()
            new_history.append('.')

            adder = ([current_group[1:]] + group,
                     [current_run]+run_length, new_history)
            vprint('adder current in next', adder)
            patterns.append(
                adder
            )
        # break

    

    vprint()
    vprint(row)
    vruns = [int(v) for v in runs.split(',')]
    for r in row_solutions:
        # break
        vprint(r)
        
        for i in range(len(groups)):
            is_valid = is_valid_sub_pattern(groups[i], r[i])
            if not is_valid:
                raise Exception('Found an invalid pattern')
        sol_part = '.'.join(r)

        v=[]
        for m in re.finditer(r'(\#+)', sol_part):
            span = m.span()
            v.append(span[1]-span[0])

        if len(v) != len(vruns):
            raise Exception('Found an invalid length pattern')
        
        for i in range(len(vruns)):
            if vruns[i] != v[i]:
                raise Exception('Found an invalid length pattern')


        

    vprint()

    nb_row_arrangments = len(row_solutions)
    nb_arrangments.append(nb_row_arrangments)

print(nb_arrangments)
solution = sum(nb_arrangments)
print('Solution: ', solution)
