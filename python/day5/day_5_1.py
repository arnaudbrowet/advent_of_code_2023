import re

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

mappers = data.split('\n\n')

map_index = 0
seed_map = [int(d) for d in mappers[0].split(":")[1].split()]

cur_map = "seed"
map_index +=1
while map_index<len(mappers):
    # break
    sub_mapper = mappers[map_index].split('\n')
    # check the key are corrects
    map_name = sub_mapper[0]

    name_match = re.match(r'(\w+)-to-(\w+) map:', map_name)
    if name_match is None:
        raise Exception('invalid name mapping')

    (current, new) = name_match.groups()
    if current != cur_map:
        raise Exception('Incorrect current map')
    
    ## update the current mapping name
    cur_map = new

    # apply the mapping
    sub_map = [[int(d) for d in s.split()] for s in sub_mapper[1:]]
    
    for seed_index, seed_value in enumerate(seed_map):
        # break
        
        for map_range in sub_map:
            # break

            [destination,  source, ranges] = map_range
            if (seed_value >= source and seed_value < source+ranges):
                # found mapping
                delta = seed_value - source
                new_value = destination+delta

                seed_map[seed_index] = new_value
                break
    
    map_index+=1

print('Current type is:', cur_map)
solution = min(seed_map)
print('Solution: ', solution)