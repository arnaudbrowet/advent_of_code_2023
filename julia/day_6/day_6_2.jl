my_parse(line) = parse(Int64, join(map(x -> line[x] == " " ? "" : line[x], 1:length(line))))
f = open("input.txt", "r")
t = my_parse(split(split(readline(f), ":")[2], " "))
d = my_parse(split(split(readline(f), ":")[2], " "))
c = 0
for i = 1:t
    global c
    c += (t-i) * i > d ? 1 : 0
end
println(c)
close(f)

