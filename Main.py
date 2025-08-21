# Toggle matrix generation
def get_toggle_matrix(rows: int, cols: int) -> list[list[int]]:
    s = rows * cols
    mat = list([0] * s for _ in range(s))
    for i in range(rows):
        for j in range(cols):
            c = row_major_index(cols, i, j)
            mat[c][c] = 1
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if (di == 0) == (dj == 0): # Check if both are 0 or abs(1)
                        continue
                    elif -1 < i + di < rows and -1 < j + dj < cols:
                        mat[c][row_major_index(cols, i + di, j + dj)] = 1
    return mat

def row_major_index(size: int, i: int, j: int) -> int:
    return size * i + j

# Gaussian elimination
def linearize(matrix: list[list[int]]) -> list[int]:
    res = []
    for r in matrix:
        res += r
    # end loop
    return res

def find_pivot(matrix: list[list[int]], start_row: int, pivot_col) -> int:
    for row in range(start_row, len(matrix)):
        if matrix[row][pivot_col]:
            return row
    # end loop
    return -1

def perform_gaussian_elimination(toggle_matrix, game_vector) -> None:
    next_free_row = 0
    for col in range(len(game_vector)):
        pivot_row = find_pivot(toggle_matrix, next_free_row, col)
        if pivot_row == -1:
            continue
        toggle_matrix[pivot_row], toggle_matrix[next_free_row] = toggle_matrix[next_free_row], toggle_matrix[pivot_row]
        game_vector[pivot_row], game_vector[next_free_row] = game_vector[next_free_row], game_vector[pivot_row]
        for row in range(next_free_row + 1, len(game_vector)):
            if toggle_matrix[row][col]:
                toggle_matrix[row] = list(a ^ b for a, b in zip(toggle_matrix[row], toggle_matrix[next_free_row]))
                game_vector[row] ^= game_vector[next_free_row]
        # end loop
        next_free_row += 1
    # end loop

def back_substitute(toggle_matrix: list[list[int]], game_vector: list[int]) -> list[int]:
    result: list[int] = [0] * len(toggle_matrix)
    for row in range(len(game_vector) - 1, -1, -1):
        pivot = None
        for col in range(len(game_vector)):
            if toggle_matrix[row][col]:
                pivot = col
                break
        if pivot is None:
            if game_vector[row]:
                print("There's no solution.")
                return []
        else:
            result[row] = game_vector[row]
            for col in range(pivot + 1, len(game_vector)):
                result[row] = result[row] ^ (toggle_matrix[row][col] & result[col])

    return result

# Decode the column vector
def decode_to_pairs(solution: list[int], n: int) -> list[list[int]]:
    result = []
    for i in range(len(solution)):
        if solution[i]:
            result.insert(0, [i // n, i % n])
    return result

# Solve
def solve(game_matrix: list[list[int]]) -> list[list[int]]:
    toggle = get_toggle_matrix(len(game_matrix), len(game_matrix[0]))
    vector = linearize(game_matrix)
    perform_gaussian_elimination(toggle, vector)
    solution = back_substitute(toggle, vector)
    return decode_to_pairs(solution, len(game_matrix))

# Tests
def test1():
    print(back_substitute([
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 1]
    ],
    [1, 1, 0]))
    # result should be [0, 1, 0]

def test2():
    mat = [
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1]
    ]
    vec = [1, 0, 1]
    perform_gaussian_elimination(mat, vec)
    print(mat, vec)

def test3():
    puzzle = [
        [1, 0],
        [0, 1]
    ]
    print(solve(puzzle))

def test4():
    puzzle = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]
    print(solve(puzzle))

# Execute
if __name__ == "__main__":
    test4()