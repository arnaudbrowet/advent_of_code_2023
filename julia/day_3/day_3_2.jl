sum = 0
f = open("input.txt", "r")
lines = readlines(f)
m = length(lines)
n = length(lines[1])
mat = Matrix{Char}(undef, m, n)

for (i, l) ∈ enumerate(lines)
    for (j, c) ∈ enumerate(l)
        mat[i, j] = c
    end 
end

numbers = []
RE = r"(\d+)"
for (i, l) ∈ enumerate(lines)
    global sum
    res = [match.match for match in eachmatch(RE, l)]
    l_cp = deepcopy(l)
    for r ∈ res
        indices = findfirst(r, l_cp)
        push!(numbers, (r, i, indices))

        l_cp = collect(l_cp)
        l_cp[indices] .= '.'
        l_cp = join(l_cp)
    end
end

row_in_range(i::Int) = i >= 1 && i <= n
col_in_range(j::Int) = j >= 1 && j <= m
function adjacent(i::Int, j::Int)
    for (n, row, col_range) ∈ numbers
        if row == i && j ∈ col_range
            return n
        end
    end
    return -1
end

for (i, l) ∈ enumerate(lines)
    for (j, c) ∈ enumerate(l)
        global sum
        if mat[i, j] == '*'
            p = 1
            c = 0
            test = [(i, j-1), (i-1, j-1), (i-1, j), (i-1, j+1), (i, j+1), (i+1, j+1), (i+1, j), (i+1, j-1)]
            save = []
            for (i_t, j_t) ∈ test
                if row_in_range(i_t) && col_in_range(j_t) 
                    local a = adjacent(i_t, j_t)
                    if a != -1 && a ∉ save
                        push!(save, a)
                        c += 1
                        p *= parse(Int, a)
                    end
                end
            end
            if c == 2
                sum += p
            end
        end
    end 
end

close(f)
println(sum)
