import re

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

mappers = data.split('\n\n')

map_index = 0
seed_base = [int(d) for d in mappers[0].split(":")[1].split()]
seed_map = [ [seed_base[2*i], seed_base[2*i+1]] for i in range(int(len(seed_base)/2))]

sort_seed = lambda seed : sorted(seed, key=lambda x:x[0])
seed_map = sort_seed(seed_map)

cur_map = "seed"
map_index +=1
sort_map = lambda map : sorted(map, key=lambda x:x[1])
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
    sub_map = sort_map([[int(d) for d in s.split()] for s in sub_mapper[1:]])

    # we will overwrite the seed map with the new mapping
    new_seed_map = []
    for seed_value_base in seed_map:
        # break

        # make a copy to avoid overwriting values early
        seed_value_range = seed_value_base.copy()

        for map_range in sub_map:
            # break
            if (seed_value_range[1]==0):
                break

            [destination,  source, ranges] = map_range

            min_value = source
            max_value = source+ranges-1

            min_seed = seed_value_range[0]
            max_seed = seed_value_range[0]+seed_value_range[1]-1

            # detect if range has overlap
            has_overlap = (min_value <=min_seed and max_value>=min_seed) or (min_value <= max_seed and max_value >= max_seed) 
            
            if has_overlap:
                start_overlap = max([min_value, min_seed])
                end_overlap = min([max_value, max_seed])

                # if overlap starts after the minimum mapping, add non-mapped values to seed_map
                if start_overlap > min_seed:
                    delta = start_overlap-min_seed
                    new_seed_map.append( [min_seed, delta])

                # add the mapping overlap
                new_seed_map.append([
                    destination + (start_overlap-min_value), end_overlap-start_overlap+1
                ])

                # if end_overlap < max_seed:
                # overwrite the seed range to check
                seed_value_range = [end_overlap, max_seed-end_overlap]
                    
        # if part of the range is not mapped, add it as is
        if seed_value_range[1] >0:
            new_seed_map.append([
                    seed_value_range[0], seed_value_range[1]
                ])

    # sort the seed map 
    seed_map = sort_seed(new_seed_map)
    
    map_index+=1


print('Current type is:', cur_map)
solution = seed_map[0][0]
print('Solution: ', solution)