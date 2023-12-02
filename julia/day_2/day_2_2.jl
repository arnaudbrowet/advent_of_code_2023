f = open("input.txt", "r")
id = 1
sum = 0

while !eof(f)  
    global id, sum
    s = readline(f)
    _, s = split(s, ":")
    s = s[2:end]
    m = Dict([("red", 0), ("green", 0), ("blue", 0)])
    for sub ∈ split(s, "; ") 
        draws = split(sub, ", ")
        for draw ∈ draws
            n, color = split(draw, " ")
            n = parse(Int64, n)
            m[color] = max(m[color], n)
        end
    end
    p = 1
    for (_ , v) ∈ m
        p *= v
    end
    sum += p
    id += 1
end
println(sum)
close(f)
