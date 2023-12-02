f = open("input.txt", "r")
id = 1
sum = 0

while !eof(f)  
    global id, sum
    s = readline(f)
    _, s = split(s, ":")
    s = s[2:end]
    ok = true
    for sub ∈ split(s, "; ")
        draws = split(sub, ", ")
        for draw ∈ draws
            if !ok 
                break 
            end
            n, color = split(draw, " ")
            n = parse(Int64, n)
            if (color == "red" && n > 12) || (color == "green" && n > 13) || (color == "blue" && n > 14)
                ok = false
                break
            end
        end
    end
    sum += ok ? id : 0
    id += 1
end
println(sum)
close(f)
