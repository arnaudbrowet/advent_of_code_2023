f = open("input.txt", "r")
sum_sum = 0
while !eof(f)  
    global sum_sum
    s = readline(f)
    line = [parse(Int, a) for a ∈ split(s, " ")]
    diff = copy(line)
    len = length(line) - 1
    first = [line[1]]
    while !all(diff[1:len] .== 0)
        for i = 1:len
            diff[i] = diff[i + 1] - diff[i]
        end
        len -= 1
        pushfirst!(first, diff[1])
    end
    local delta = 0
    for f ∈ first[2:end]
        delta = f - delta
    end
    sum_sum += delta
end
println(sum_sum)
close(f)
