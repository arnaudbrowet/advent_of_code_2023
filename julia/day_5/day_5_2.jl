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
        vals = [parse(Int, a) for a ∈ split(s, " ")]
        seeds = [(vals[i], vals[i] + vals[i + 1] - 1) for i ∈ 1:2:length(vals)]
    else
        mapping = split(s, " ")
        mapping = map(x -> parse(Int, x), mapping)
        push!(maps[c], (mapping[1], mapping[2], mapping[3]))
    end
end

m = Inf32
for mappings ∈ maps
    global seeds
    for (i, (l, u)) ∈ enumerate(seeds)
        for (d_s, s_s, len) ∈ mappings
            s_in = s_s > l && s_s < u
            d_in = s_s + len - 1 > l && s_s + len - 1 < u
            if s_in && d_in 
                int_1 = (l, s_s - 1)
                int_3 = (s_s + len, u)
                l, u = d_s, d_s + len - 1
                seeds[i] = (l, u)
                push!(seeds, int_1)
                push!(seeds, int_3)
                break
            elseif s_in
                int_1 = (l, s_s - 1)
                l, u = d_s, d_s + (u - s_s)
                seeds[i] = (l, u)
                push!(seeds, int_1)
                break
            elseif d_in
                int_2 = (s_s + len, u)
                l, u = d_s + (l - s_s), d_s + len - 1
                seeds[i] = (l, u)
                push!(seeds, int_2)
                break
            elseif l >= s_s && u <= s_s + len - 1
                l, u = d_s + (l - s_s), d_s + (u - s_s)
                seeds[i] = (l, u)
                break
            end
        end
    end
end

println(minimum([l for (l, _) ∈ seeds]))

