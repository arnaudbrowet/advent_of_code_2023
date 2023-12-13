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

rows = data.split('\n')

def is_valid_pattern(base_pattern, sol):
    if len(base_pattern) != len(sol):
        return False
    
    for p,s in zip(base_pattern, sol):
        if p=='?':
            continue
        if p != s:
            return False

    return True


cik_map ={}

def cik(n,k):
    '''
    fit n elements in k set
    '''
    if n==1: return k
    if k==1: return 1

    if (n,k) in cik_map: return cik_map[(n,k)]

    cik_map[(n,k)] = sum([cik(n-i,k-1) for i in range(n+1)])
    return cik_map[(n,k)]


pattern = '???#'
required = ['###']
pattern = '????.???'
required = '##.#.##'.split('.')

# s = compute_solution(pattern, required)
# keep a temporary map of solved patterns
solved_patterns={}
def compute_solution(pattern, required):
    # avoid modifiying required patterns in solution
    required_groups = required.copy()
    
    # if we already solved the pattern, return the value
    base_sol = '.'.join(required_groups)
    
    vprint('solving')
    vprint(f'pattern ({len(pattern)}):', pattern)
    vprint("base_sol:", base_sol)
    vprint("required:", required)
    vprint()
    
    if (pattern, base_sol) in solved_patterns:
        return solved_patterns[(pattern, base_sol)]
    
    # if we have nothing to fit
    if len(required) == 0:
        return 0 if '#' in pattern else 1
    
    if len(pattern) == 0:
        return 0 if len(required) >0 else 1
    
    # if the base solution does not fit inside the pattern, no solution
    if len(base_sol) > len(pattern):
        return 0
    
    # if we can extend the solution, it must fit
    if len(base_sol) == len(pattern):
        return 1 if is_valid_pattern(pattern, base_sol) else 0
    
    # first strip the '.'
    if pattern[0] == '.':
        
        return compute_solution(pattern[1:], required_groups)

    if pattern[-1] == '.':
        return compute_solution(pattern[:-1], required_groups)
    
    # match the starting and ending #
    if pattern[0] == '#':
        group = required_groups.pop(0)
        sub = pattern[:len(group)+1]
        if sub[-1] == '#':
            return 0
        elif '.' in sub[:-1]:
            return 0
        else:
            return compute_solution(pattern[len(group)+1:], required_groups)
        
    if pattern[-1] == '#':
        group = required_groups.pop(-1)
        sub = pattern[-len(group)-1:]
        
        if sub[0]=='#':
            return 0
        elif '.' in sub[1:]:
            return 0
        else:
            return compute_solution(pattern[:-len(group)-1], required_groups)
    
    
    # if we have forced position (#) match the longest run in required
    if "#" in pattern:
        group_lengths = [len(g) for g in required_groups]
        longest_required = max(group_lengths)
        
        longest_index = group_lengths.index(longest_required)
        
        solutions = []
        
        # if the longest is the first
        if longest_index==0:
            max_matching_pos = min(pattern.index('#'), len(pattern)-len(base_sol))
            
            for i in range(max_matching_pos+1):
                
                sub_pattern = pattern[i:i+longest_required+1]    # +1 for the required dot
                
                if sub_pattern[-1]=='#':
                    continue
                
                if i+longest_required < len(pattern):
                    sub_pattern = sub_pattern[:-1]
                    
                # print(i, 'go with',sub_pattern)
                # print('valid:',is_valid_pattern(sub_pattern, required_groups[longest_index]))
                    
                # print('go with', sub_pattern)
                # print('isvalid ',is_valid_pattern(sub_pattern, required_groups[longest_index]))
                if is_valid_pattern(sub_pattern, required_groups[longest_index]):
                    right_pattern = pattern[i+longest_required+1:]
                    solutions.append(
                        compute_solution( right_pattern, required_groups[1:])
                    )
                
            return sum(solutions)
        
         # if the longest is the last
        elif longest_index==len(group_lengths)-1:
            # print('longest in last', )
            max_matching_pos = max(
                len(pattern) - pattern[::-1].index('#')-1,
                len(base_sol)-1
            )
            for i in range(len(pattern), max_matching_pos, -1):
                sub_pattern = pattern[i-longest_required-1:i]    # +1 for the required dot
                
                # print(i, sub_pattern)
                if sub_pattern[0]=='#':
                    continue
                
                sub_pattern = sub_pattern[1:]
                
                if is_valid_pattern(sub_pattern, required_groups[longest_index]):
                    left_pattern = pattern[:i-longest_required-1]
                    
                    # print(left_pattern, required_groups[:-1])
                    # print(left_pattern, required_groups[:-1])
                    
                    solutions.append(
                        compute_solution( left_pattern, required_groups[:-1])
                    )
            return sum(solutions)
        else:
            solutions = []
            # starting pos is the sum of the length + one dot per group
            starting_pos = sum(group_lengths[:longest_index]) + longest_index
            
            min_length = sum(group_lengths[longest_index:]) + len(group_lengths)-longest_index-1
            
            max_matching_pos = len(pattern)-starting_pos-min_length+1
            
            left_groups = required_groups[:longest_index]
            right_groups = required_groups[longest_index+1:]
            for i in range(max_matching_pos):
                sub_pattern = pattern[starting_pos+i-1:starting_pos+i+longest_required+1]    # +1 for the required dot
                
                if sub_pattern[0]=='#' or sub_pattern[-1] == '#':
                    continue
                
                sub_pattern = sub_pattern[1:-1]
                
                if is_valid_pattern(sub_pattern, required_groups[longest_index]):
                    
                    left_pattern = pattern[:starting_pos+i-1]   # -to account for a .
                    right_pattern = pattern[starting_pos+i+longest_required+1:]
                    
                    left_solutions = compute_solution( left_pattern, left_groups)
                    if left_solutions == 0: 
                        right_solutions = 0
                    else:
                        right_solutions = compute_solution( right_pattern, right_groups)
                    solutions.append(
                        left_solutions*right_solutions
                    )
            return sum(solutions)
                    
    elif '.' in pattern:
        
        sub_patterns = pattern.split('.')
        
        first_pattern = sub_patterns[0]
        remaining_patterns = '.'.join(sub_patterns[1:])
        first_group = required_groups[0]
        
        if len(required_groups)==1:
            sol =  compute_solution( first_pattern, required_groups)+compute_solution(remaining_patterns, required_groups)
            
            solved_patterns[(pattern, base_sol)] = sol
            return sol
        else:
            if len(first_pattern)< len(first_group):
                # first group does not fit in first pattern
                sol = compute_solution( remaining_patterns, required_groups)
                solved_patterns[(pattern, base_sol)] = sol
                return sol
            
            else:
                in_current = 0
                for i in range(len(first_pattern)-len(first_group)+1):
                    # fit the 1st group in the 1st pattern, fit the rest in the remaining
                    remaining_first_pattern=first_pattern[len(first_group)+i+1:]
                    
                    if len(remaining_first_pattern)>0:
                        in_current += compute_solution(
                            remaining_first_pattern + '.'+remaining_patterns, required_groups[1:]
                        )
                    else:
                        in_current += compute_solution(remaining_patterns, required_groups[1:])
                
            
                in_next = compute_solution(remaining_patterns, required_groups)
                sol = in_current + in_next
                solved_patterns[(pattern, base_sol)] = sol
                return sol
        
    else : 
        ## we only have ? in the pattern
        nb_holes = 1 + len(required_groups)
        nb_fill  = len(pattern)-len(base_sol)
        return cik(nb_fill, nb_holes)
    
# iterate on each row of springs
row_iterator = rows

# row_iterator = ["????.######..#####. 1,6,5"]
# row_iterator = ["??##?##?????##...##? 12,2"]


for nb_dup in [1]:
    # break
    nb_arrangments = []
    for i, row in enumerate(row_iterator):
        # print("row", i)
        # break
        (base_springs, base_runs) = row.split(' ')

        springs = '?'.join([base_springs for i in range(nb_dup)])
        run_lengths = ','.join([base_runs for i in range(nb_dup)])

        # remove leading and trailing .
        springs = re.sub(r'^(\.+)', '', springs)
        springs = re.sub(r'(\.+)$', '', springs)

        # replace multiple .
        springs = re.sub(r'(\.+)', '.', springs)

        # run lengths as integer
        runs = [int(r) for r in run_lengths.split(',')]

        required_patterns = ['#'*r for r in runs]
        base_sol = '.'.join(required_patterns)
        
        # reset the solved patterns
        # solved_patterns={}
        pattern = springs
        required = required_patterns
        nbSolution = compute_solution(springs, required_patterns)
        
        nb_arrangments.append(nbSolution)

        # print()
    # print(springs)
    # print(base_sol)
    # min_required_length = sum(runs) + len(runs)-1

    # pattern_length = len(springs)

    # print(pattern_length, min_required_length, pattern_length-min_required_length)
    # print(nb_arrangments)
    
    
solution = sum(nb_arrangments)
print('Solution: ', solution)

if False:

    row = ['?????????#?# 1,1,7']
    # row_iterator = rows[0:10]
    nb_arrangments_dup = []
    # for nb_dup in [2]: # [1,2,3,4]:
    if True:
        nb_arrangments = []
        for i, row in enumerate(row_iterator):
            # break
            (springs, runs) = row.split(' ')

            springs = '?'.join([springs for i in range(nb_dup)])
            runs = ','.join([runs for i in range(nb_dup)])

            # springs = springs + '.' + springs + '.' +springs
            # springs = springs + '.' + springs + '#' +springs
            # springs = springs + '#' + springs + '.' +springs
            # springs = springs + '#' + springs + '#' +springs

            # runs = runs + ',' + runs + ',' +runs
            
            # springs = springs + '#'
            # springs = springs + '.'
            # springs = '#'+springs
            # springs = '.'+springs

            # springs = springs + '#'+springs
            # springs = springs + '.'+springs
            # runs = runs + ','+runs

            
            

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

            

            # print()
            # print(springs)
            vruns = [int(v) for v in runs.split(',')]
            for r in row_solutions:
                # break
                # print(r)
                
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

            # print()

            nb_row_arrangments = len(row_solutions)
            # print(nb_row_arrangments)
            nb_arrangments.append(nb_row_arrangments)

        nb_arrangments_dup.append(nb_arrangments)

    print(nb_arrangments_dup)
    # true_prod = []

    # for r1, r2 in zip(nb_arrangments_dup[0],nb_arrangments_dup[1]):
    #     # break
    #     ratio = r2/r1
    #     true = r1*(ratio**4)
    #     true_prod.append(int(true))

    # solution = sum(true_prod)
    # solution = nb_arrangments_dup[0].sum()
    solution = 0
    print('Solution: ', solution)
