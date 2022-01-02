import sys

# Possible diagonals
R =  1 # right diagonal
L = -1 # left diagonal
E =  0 # empty spot

DEBUG = 0

STR_TABLE = '\*/'

def str_entry(e):
    return STR_TABLE[e+1]

def print_diagonals(m):
    for l in m:
        for e in l:
            print(str_entry(e), end=' ')
        print()

def check(m, i, j):
    if DEBUG:
        print('---------------------')
        print_diagonals(m)
        print(i, j)

    try:
        e = m[i][j]
        n = len(m)
        # +-----+
        # | | | |
        # +-----+
        # |/|\|/|
        # +-----+
        # | | | |
        # +-----+
        if j > 0 and e == -1*m[i][j-1]:
            return False

        if j+1 < n and e == -1*m[i][j+1]:
            return False

        # +-----+
        # | |/| |
        # +-----+
        # | |\| |
        # +-----+
        # | |/| |
        # +-----+
        if i > 0 and e == -1*m[i-1][j]:
            return False

        if i+1 < n and e == -1*m[i+1][j]:
            return False

        # +-----+
        # |\| | |
        # +-----+
        # | |\| |
        # +-----+
        # | | |\|
        # +-----+
        if i > 0 and j > 0 and e ==  m[i-1][j-1] == L:
            return False

        if i+1 < n and j+1 < n and e ==  m[i+1][j+1] == L:
            return False

        # +-----+
        # | | |/|
        # +-----+
        # | |/| |
        # +-----+
        # |/| | |
        # +-----+
        if i > 0 and j+1 < n and e == m[i-1][j+1] == R:
            return False

        if j > 0 and i+1 < n and e == m[i+1][j-1] == R:
            return False

    finally:
        if DEBUG:
            print_diagonals(m)
            print('---------------------')
            print()

    return True

def solve_helper(m, i, j, n):
    if n == 0:
        return True

    # calculate if there is room for the remaining diagonals
    room = len(m)*(len(m) - (i+1)) + len(m) - j + 1
    if room < n:
        return False

    for x in range(i, len(m)):
        for y in range(j, len(m)):
            if m[x][y] == E:
                for s in [R, L]:
                    m[x][y] = s
                    if check(m, x, y) and solve_helper(m, x, y, n-1):
                        return True

                m[x][y] = E
        j = 0

    return False

def solve(m, n):
    return solve_helper(m, 0, 0, n)

def main():
    N = int(sys.argv[1])
    M = int(sys.argv[2])
    m = list([E]*N for i in range(N))
    if solve(m, M):
        print_diagonals(m)

if __name__ == '__main__':
    main()
