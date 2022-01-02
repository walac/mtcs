PERMUTATION_LENGTH = 16
LINE_LENGTH = 4
CIRCLE1 = (1, 2, 3, 7, 0, 9, 5, 6, 4, 10, 11, 15, 8, 12, 13, 14)
CIRCLE2A = (None, 2, 3, 7, 5, 1, 10, 6, 4, None, 11, 15, 8, 12, 13, 14)
CIRCLE2B = (None, 2, 6, None, 5, 1, 7, 11, 4, 13, 9, 15, 8, 12, 10, 14)
CIRCLE3 = (None, None, 3, 7, 5, 6, 2, 11, 4, 13, 9, 15, 8, 12, 10, 14)
CIRCLE2A_PIVOT = 9
CIRCLE2B_PIVOT = 3
ZERO_POS = 15
GOAL = list(range(1, 16))
GOAL.append(0)

# for 3-cycle transposition
A = 0  # (A, _, _)
B = 1  # (_, B, _)
C = 4  # (_, _, C)
D = 5

THREE_CYCLE_TRANSP = [1, 0, 4, 5]


def print_p(p):
    for i in range(4):
        print(
            f'{p[i * 4]:2}, {p[i * 4 + 1]:2}, {p[i * 4 + 2]:2}, {p[i * 4 + 3]:2}'
        )
    print()


def to_2d(pos):
    """Convert an 1d position to a pair of 2d indexes."""
    return (pos // LINE_LENGTH, pos % LINE_LENGTH)


def swap(p, i, j):
    """Swap to elements in a list."""
    p[i], p[j] = p[j], p[i]


def apply_transpositions(p, initial, trans):
    """Apply transpositions to the list p.

    The list of transpositions is indicated by the list trans,
    and it starts in the position initial.
    """
    for t in trans:
        swap(p, initial, t)
        initial = t


def invert_transpositions(final, trans):
    """Given a list of transpositions, return the inverse path."""
    return list(reversed(trans[:-1])) + [final]


def transpose_to_pos(src, dest):
    """Move an item from position src to position dest using 2-cycle transpositions.

    We generate a list of transpositions that moves the element
    from position src to the position dest.
    """
    if src == dest:
        return []

    ls, cs = to_2d(src)  # line souce, column source
    ld, cd = to_2d(dest)  # line dest, column dest
    line_dist = ld - ls
    col_dist = cd - cs
    line_dir = line_dist // abs(line_dist) if line_dist else 0
    col_dir = col_dist // abs(col_dist) if col_dist else 0

    def gen_lines(src):
        return [src + 4 * i * line_dir for i in range(1, abs(line_dist) + 1)]

    def gen_cols(src):
        return [src + i * col_dir for i in range(1, abs(col_dist) + 1)]

    ret = gen_lines(src)
    if ret:
        src = ret[-1]
    ret.extend(gen_cols(src))
    return ret


def shift_to_pos(p, src, dest, zero=ZERO_POS):
    """Move an item to the destination position using grid shift.

    Only positions A, B and C are valid destinations.
    Return the transpositions and the new position of the zero
    position.
    """
    if dest == A:
        circle = CIRCLE1
    elif dest == B:
        if src == CIRCLE2A_PIVOT or p[CIRCLE2A_PIVOT] == 0:
            circle = CIRCLE2B
        else:
            circle = CIRCLE2A
    elif dest == C:
        circle = CIRCLE3
    else:
        raise ValueError(f'Destination {dest} is invalid')

    trans = []
    x = p[src]
    i = src

    while p[dest] != x:
        i = circle[zero]
        assert i is not None
        trans.append(i)
        swap(p, zero, i)
        zero = i

    return trans, zero


def gen_permutations_to_solve(p):
    """Generate the list of permutations to sort p."""
    assert p[ZERO_POS] == 0
    ret = []
    p = list(p)
    for i in range(len(p)):
        while p[i] != GOAL[i]:
            j = p[i] - 1
            x, y = min(i, j), max(i, j)
            ret.append((x, y))
            swap(p, i, j)
    return ret


def to_3_cycle(p):
    """Convert a 2-cycle list of permutations to 3-cycle.

    From group theory:
        (a, b)(a, c) = (a, b, c)
        (a, b)(c, d) = (a, b, c)(a, d, c)
        (a, b) == (b, a)
    """
    assert len(p) % 2 == 0
    ret = []
    for i in range(0, len(p), 2):
        a, b = p[i]
        c, d = p[i + 1]
        if a == c:
            ret.append((a, b, d))
        else:
            ret.extend(((a, b, c), (a, d, c)))
    return ret


def move_zero_to_correct_pos(p):
    """Move the zero a known position."""
    cur_zero_pos = p.index(0)
    transpositions = transpose_to_pos(cur_zero_pos, ZERO_POS)
    apply_transpositions(p, cur_zero_pos, transpositions)
    assert p[ZERO_POS] == 0
    return transpositions


def solution(positions):
    """Solve the fifteen puzzle.

    It returns the list of permutations with the space that
    we must apply to solve the puzzle.
    """
    ret = []
    positions = list(positions)

    assert set(positions) == set(GOAL)

    if positions[ZERO_POS] != 0:
        ret = move_zero_to_correct_pos(positions)

    perms = gen_permutations_to_solve(positions)

    if len(perms) % 2 != 0:
        raise ValueError(f'{positions} is an odd permutation, perms={perms}')

    for a, b, c in to_3_cycle(perms):
        a_val = positions[a]
        b_val = positions[b]
        c_val = positions[c]
        inversions = []
        z = ZERO_POS

        for val, dest in zip((a_val, b_val, c_val), (A, B, C)):
            i = positions.index(val)
            t, new_z = shift_to_pos(positions, i, dest, z)
            ret.extend(t)
            inversions.append((new_z, invert_transpositions(z, t)))
            z = new_z

        t = transpose_to_pos(z, D)
        ret.extend(t)
        apply_transpositions(positions, z, t)
        t = invert_transpositions(z, t)
        inversions.append((D, t))

        ret.extend(THREE_CYCLE_TRANSP)
        apply_transpositions(positions, D, THREE_CYCLE_TRANSP)

        for i, t in reversed(inversions):
            apply_transpositions(positions, i, t)
            ret.extend(t)

    return ret
