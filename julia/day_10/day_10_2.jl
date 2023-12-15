mat = Vector{Vector{Char}}()
f = open("input.txt", "r")
c = 1
while !eof(f)  
    global c
    s = readline(f)
    s = collect(s)
    if 'S' ∈ s
        global i_s = c
        global j_s = findfirst(s .== 'S')
    end
    c += 1
    push!(mat, s)
end
close(f)

m, n = length(mat), length(mat[1])
inrange(i::Int, j::Int) = i >= 1 && i <= m && j >= 1 && j <= n
function find_nei(i::Int, j::Int)
    local to_check = []
    if mat[i][j] == 'S'
        to_check = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    elseif mat[i][j] == '|'
        to_check = [(i - 1, j), (i + 1, j)]
    elseif mat[i][j] == '-'
        to_check = [(i, j - 1), (i, j + 1)]
    elseif mat[i][j] == 'L'
        to_check = [(i - 1, j), (i, j + 1)]
    elseif mat[i][j] == 'J'
        to_check = [(i - 1, j), (i, j - 1)]
    elseif mat[i][j] == '7'
        to_check = [(i + 1, j), (i, j - 1)]
    elseif mat[i][j] == 'F'
        to_check = [(i + 1, j), (i, j + 1)]
    end
    local nei = []
    for tc ∈ to_check
        if !inrange(tc...)
            continue
        end
        if tc == (i - 1, j) && mat[i - 1][j] ∈ ['F', '|', '7']
            push!(nei, tc)
        end
        if tc == (i + 1, j) && mat[i + 1][j] ∈ ['L', '|', 'J']
            push!(nei, tc)
        end
        if tc == (i, j - 1) && mat[i][j - 1] ∈ ['F', '-', 'L']
            push!(nei, tc)
        end
        if tc == (i, j + 1) && mat[i][j + 1] ∈ ['7', '-', 'J']
            push!(nei, tc)
        end
    end
    return nei
end

using DataStructures
dist = Inf * ones(Int, (m, n))
Q = PriorityQueue()
for i ∈ 1:m
    for j ∈ 1:n
        d = (i == i_s && j == j_s) ? 0 : Inf
        push!(Q, (i, j) => d)
        dist[i, j] = d
    end
end
while !isempty(Q)
    local ((i, j), d) = first(Q)
    delete!(Q, (i, j))
    nei = find_nei(i, j)
    for (k, l) ∈ nei
        if !haskey(Q, (k, l))
            continue
        end
        alt = d + 1
        if alt < dist[k, l]
            Q[(k, l)] = alt 
            dist[k, l] = alt
        end
    end
end

function find_next(i::Int, j::Int)
    for (k, l) ∈ [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        if inrange(k, l) && dist[k, l] ∈ [dist[i, j] - 1, dist[i, j] + 1] && (k, l) ∉ p
            return (k, l)
        end
    end
    return -1
end
p = [(i_s, j_s)]
next = find_next(i_s, j_s)
while next != -1
    global next, p
    push!(p, next)
    next = find_next(next...)
end
push!(p, (i_s, j_s))

# Compute area with shoelace formula
A = 0
for idx ∈ 1:(length(p[1:end]) - 1)
    global A
    (x1, y1) = p[idx]
    (x2, y2) = p[idx + 1]
    det = x1 * y2 - y1 * x2
    A += det
end
A = abs(A ÷ 2)

# Compute sol with Pick's theorem
sol = A + 1 - ((length(p) - 1) / 2)
println(sol)
