f = open("input.txt", "r")
pattern = readline(f)
pattern = [c for c ∈ pattern]
_ = readline(f)

children = Dict{String, Tuple{String, String}}()
while !eof(f)  
    s = readline(f)
    parent, child = split(s, "=")
    parent = parent[1:end-1]
    left_child, right_child = split(child, ",")
    left_child = left_child[3:end]
    right_child = right_child[2:end-1]
    children[parent] = (left_child, right_child)
end
close(f)

i = 1
current = "AAA"
while true
    global i, current
    left, right = children[current]
    move = pattern[(i - 1) % length(pattern) + 1]
    current = move == 'L' ? left : right
    if current == "ZZZ"
        break 
    end
    i += 1
end
println(i)