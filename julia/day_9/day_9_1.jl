f = open("input.txt", "r")
sum_sum = 0
while !eof(f)  
    global sum_sum
    s = readline(f)
    line = [parse(Int, a) for a ∈ split(s, " ")]
    diff = copy(line)
    len = length(line) - 1
    local sum = line[end]
    while !all(diff[1:len] .== 0)
        for i = 1:len
            diff[i] = diff[i + 1] - diff[i]
        end
        sum += diff[len]
        len -= 1
    end
    sum_sum += sum
end
println(sum_sum)
close(f)
