f = open("input.txt", "r")
caps = []
while !eof(f)  
    local numbers, winning
    global caps
    c = readline(f)
    _, c = split(c, ":")
    c = c[2:end]
    numbers, winning = split(c, "|")
    numbers = [parse(Int64, n) for n ∈ split(numbers, " ") if n != ""]
    winning = [parse(Int64, n) for n ∈ split(winning, " ") if n != ""]
    push!(caps, numbers ∩ winning)
end
copies = ones(Int64, length(caps))
for (id, n) ∈ enumerate(copies)
    global copies
    for _ = 1:n
        for j = 1:length(caps[id])
            copies[id + j] += 1
        end
    end
end
println(Base.sum(copies))
close(f)
