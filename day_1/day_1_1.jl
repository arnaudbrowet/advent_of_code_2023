sum = 0
f = open("day_1_input.txt", "r")
while !eof(f)  
    global sum
    s = readline(f)
    s = [c for c = s if isdigit(c)]
    sum += parse(Int64, "$(s[1])$(s[end])")
end
close(f)
println(sum)
