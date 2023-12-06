function my_parse(line)
    line = [v for v ∈ line if tryparse(Int64, v) !== nothing]
    line = [parse(Int64, v) for v ∈ line]
    return line
end
f = open("input.txt", "r")
t_list = my_parse(split(split(readline(f), ":")[2], " "))
d_list = my_parse(split(split(readline(f), ":")[2], " "))
prod = 1
for (t, d) ∈ zip(t_list, d_list)
    global prod
    local c = 0
    for i ∈ 1:t
        c += (t-i) * i > d ? 1 : 0
    end
    prod *= c
end
println(prod)
close(f)

