sum = 0
f = open("input.txt", "r")
count(array) = isempty(array) ? 0 : 2^(length(array) - 1)
while !eof(f)  
    local numbers, winning
    global sum
    c = readline(f)
    _, c = split(c, ":")
    c = c[2:end]
    numbers, winning = split(c, "|")
    numbers = [parse(Int64, n) for n ∈ split(numbers, " ") if n != ""]
    winning = [parse(Int64, n) for n ∈ split(winning, " ") if n != ""]
    sum += count(numbers ∩ winning)
end
close(f)
println(sum)
