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

is_symbol(c::Char) = !isdigit(c) && c != '.'
row_in_range(i::Int) = i >= 1 && i <= n
col_in_range(j::Int) = j >= 1 && j <= m

RE = r"(\d+)"
for (i, l) ∈ enumerate(lines)
    global sum
    res = [match.match for match in eachmatch(RE, l)]
    l_cp = deepcopy(l)
    for r ∈ res
        indices = findfirst(r, l_cp)
        l_cp = collect(l_cp)
        l_cp[indices] .= '.'
        l_cp = join(l_cp)
        for j ∈ (indices[1] - 1):(indices[end] + 1)
            if col_in_range(j) && row_in_range(i - 1) && is_symbol(mat[i - 1, j])
                sum += parse(Int, r) 
                break
            end
            if col_in_range(j) && row_in_range(i + 1) && is_symbol(mat[i + 1, j])
                sum += parse(Int, r)  
                break
            end
        end
        sum += col_in_range(indices[1] - 1) && is_symbol(mat[i, indices[1] - 1]) ? parse(Int, r)  : 0
        sum += col_in_range(indices[end] + 1) && is_symbol(mat[i, indices[end] + 1]) ? parse(Int, r)  : 0
    end
end

close(f)
println(sum)
