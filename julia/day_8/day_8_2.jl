f = open("input.txt", "r")
pattern = readline(f)
pattern = [c for c ∈ pattern]
_ = readline(f)

starting = Vector{String}()
children = Dict{String, Tuple{String, String}}()
while !eof(f)  
    s = readline(f)
    parent, child = split(s, "=")
    parent = parent[1:end-1]
    if parent[end] == 'A'
        push!(starting, parent)
    end
    left_child, right_child = split(child, ",")
    left_child = left_child[3:end]
    right_child = right_child[2:end-1]
    children[parent] = (left_child, right_child)
end
close(f)

values = zeros(Int, length(starting))
for (i, s) ∈ enumerate(starting)
    local j = 1
    local current = s
    while true
        left, right = children[current]
        move = pattern[(j - 1) % length(pattern) + 1]
        current = move == 'L' ? left : right
        if current[end] == 'Z'
            break
        end
        j += 1
    end
    values[i] = j
end

sol = 1
for v ∈ values
    global sol
    sol = lcm(sol, v)
end
println(sol)
