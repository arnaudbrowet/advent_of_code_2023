using StatsBase

f = open("input.txt", "r")
data = Dict()
while !eof(f)  
    global hands, bids
    s = readline(f)
    hand, bid = split(s, " ")
    data[hand] = parse(Int64, bid)
end
close(f)

VALS = Dict(zip(['1', '2', '3', '4', '5', '6', '7', '8', '9'], collect(1:9)))
VALS['T'] = 10
VALS['Q'] = 12
VALS['K'] = 13
VALS['A'] = 14
VALS['J'] = 0

function type(h)
    counter = countmap([c for c ∈ h if c != 'J'])
    n_jokers = count(==('J'), [c for c ∈ h])
    if 5 ∈ values(counter) || n_jokers == 5
        return 1
    end
    for i = 1:4
        if 5 - i ∈ values(counter) && n_jokers == i
            return 1
        end
    end

    if 4 ∈ values(counter) || n_jokers == 4
        return 2
    end
    for i = 1:3
        if 4 - i ∈ values(counter) && n_jokers == i
            return 2
        end
    end

    if (3 ∈ values(counter) && 2 ∈ values(counter)) || (3 ∈ values(counter) && n_jokers == 2) || (2 ∈ values(counter) && n_jokers == 3)
        return 3
    end
    check_pairs = countmap(values(counter))
    if haskey(check_pairs, 2)
        if check_pairs[2] == 2 && n_jokers == 1
            return 3
        end
    end

    if 3 ∈ values(counter) || n_jokers == 3
        return 4
    end
    for i ∈ 1:2
        if 3 - i ∈ values(counter) && n_jokers == i 
            return 4
        end
    end

    if haskey(check_pairs, 2)
        return check_pairs[2] == 2 ? 5 : 6
    end

    if n_jokers > 0
        return 6
    end

    return 7
end

function isless(h1, h2)
    t1 = type(h1)
    t2 = type(h2)
    if t1 == t2
        h1_map = [VALS[c] for c ∈ h1]
        h2_map = [VALS[c] for c ∈ h2]
        return h1_map > h2_map
    end
    return t1 < t2
end

ranks = reverse(sort(collect(keys(data)), lt = isless))
sum = 0
for (i, h) ∈ enumerate(ranks)
    global sum
    sum += i * data[h]
end
println(sum)
