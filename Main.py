def solve(game: list[list[int]]) -> list[list[int]]:
    get_toggle_matrix(2, 2)

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
    for r in mat:
        print(r)

def row_major_index(size: int, i: int, j: int) -> int:
    return size * i + j

if __name__ == "__main__":
    solve([])