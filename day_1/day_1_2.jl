DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGITS_DIC = Dict(zip(DIGITS, collect(1:9)))

sum = 0
f = open("day_1_input.txt", "r")
while !eof(f)  
    global sum
    d = []
    s = readline(f)
    for i ∈ 1:length(s)
        for j ∈ i:length(s)
            if i == j && isdigit(s[i])
                push!(d, "$(s[i])")
            elseif s[i:j] ∈ DIGITS
                push!(d, "$(s[i:j])")
            end
        end
    end
    d1 = isdigit(d[1][1]) ? parse(Int64, d[1]) : DIGITS_DIC[d[1]]
    dend = isdigit(d[end][1]) ? parse(Int64, d[end]) : DIGITS_DIC[d[end]]
    sum += 10 * d1 + dend
end
close(f)
println(sum)
