f = open("input.txt", "r")

c = 0
seeds = []
maps = [[], [], [], [], [], [], []]

while !eof(f)  
    global seeds, maps, c

    s = readline(f)
    if s == ""
        c += 1 
        continue
    end
    if !isdigit(s[1]) && c > 0
        continue
    end

    if c == 0
        _, s = split(s, ":")
        s = s[2:end]
        seeds = [parse(Int, a) for a ∈ split(s, " ")]
    else
        mapping = split(s, " ")
        mapping = map(x -> parse(Int, x), mapping)
        push!(maps[c], (mapping[1], mapping[2], mapping[3]))
    end
end

m = Inf32
for seed ∈ seeds
    global m
    val = seed
    for mappings ∈ maps
        for (d_s, s_s, l) ∈ mappings
            if val >= s_s && val <= s_s + l - 1
                val = d_s + (val - s_s)
                break
            end
        end
    end
    m = min(m, val)
end

println(m)
