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
VALS['J'] = 11
VALS['Q'] = 12
VALS['K'] = 13
VALS['A'] = 14

function type(h)
    count = countmap([c for c ∈ h])
    if 5 ∈ values(count)
        return 1
    end
    if 4 ∈ values(count) 
        return 2
    end
    if 3 ∈ values(count) && 2 ∈ values(count)
        return 3
    end
    if 3 ∈ values(count)
        return 4
    end
    check_pairs = countmap(values(count))
    if haskey(check_pairs, 2)
        return check_pairs[2] == 2 ? 5 : 6
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