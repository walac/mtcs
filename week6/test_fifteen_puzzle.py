import itertools
import pytest
import is_even
from fifteen_puzzle import *


def assert_circle_nodes_visited(circle):
    """Sanity check of the circle list.

    Make sure all relevant nodes are visited and that
    we don't interact with any None position.
    """
    visited = [0] * len(circle)
    none_count = 0

    for _, x in enumerate(circle):
        if x is None:
            none_count += 1
        else:
            assert x < PERMUTATION_LENGTH
            assert circle[x] is not None
            assert visited[x] == 0
            visited[x] = 1

    assert sum(visited) == PERMUTATION_LENGTH - none_count


def test_sanity():
    assert len(CIRCLE1) == PERMUTATION_LENGTH
    assert len(CIRCLE2A) == PERMUTATION_LENGTH
    assert len(CIRCLE2B) == PERMUTATION_LENGTH
    assert len(CIRCLE3) == PERMUTATION_LENGTH

    assert CIRCLE2A[0] is None
    assert CIRCLE2A[CIRCLE2A_PIVOT] is None
    assert CIRCLE2B[0] is None
    assert CIRCLE2B[CIRCLE2B_PIVOT] is None
    assert CIRCLE3[0] is None
    assert CIRCLE3[1] is None

    assert_circle_nodes_visited(CIRCLE1)
    assert_circle_nodes_visited(CIRCLE2A)
    assert_circle_nodes_visited(CIRCLE2B)
    assert_circle_nodes_visited(CIRCLE3)


def test_to_2d():
    expected_values = (
        # Line 0
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),

        # Line 1,
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),

        # Line 2,
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),

        # Line 3,
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
    )

    for i, expected in zip(range(PERMUTATION_LENGTH), expected_values):
        assert to_2d(i) == expected


def test_transpose_to_pos():
    p = list(GOAL)
    goal_set = set(GOAL)

    for i in range(16):
        t = transpose_to_pos(ZERO_POS, i)
        apply_transpositions(p, ZERO_POS, t)
        assert p[i] == 0
        assert set(p) == goal_set
        apply_transpositions(p, i, invert_transpositions(ZERO_POS, t))
        assert p == GOAL


def shift_to_pos_test_helper(p, srcs, dest):
    for i in srcs:
        val = p[i]
        t, zero = shift_to_pos(list(p), i, dest)
        apply_transpositions(p, ZERO_POS, t)
        assert p[dest] == val
        apply_transpositions(p, zero, invert_transpositions(ZERO_POS, t))
        assert p == GOAL


def test_shift_to_pos():
    with pytest.raises(ValueError):
        shift_to_pos([], 6, 7)

    srcs = list(GOAL)
    srcs.remove(A)
    srcs.remove(B)
    srcs.remove(C)
    p = list(GOAL)

    shift_to_pos_test_helper(p, srcs, A)
    shift_to_pos_test_helper(p, srcs, B)
    shift_to_pos_test_helper(p, srcs, C)


def test_gen_permutations():
    assert gen_permutations_to_solve(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == []
    assert gen_permutations_to_solve(
        [2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == [(0, 1)]
    assert gen_permutations_to_solve(
        [3, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == [(0, 2)]
    assert gen_permutations_to_solve(
        [4, 3, 2, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == [(0, 3),
                                                                    (1, 2)]
    assert gen_permutations_to_solve(
        [2, 1, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]) == [(0, 1),
                                                                    (2, 3)]


def test_solve():
    i = 0
    for p in itertools.permutations(GOAL[:-1]):
        if i > 1000:
            break

        p = list(p) + [0]
        if is_even.is_even_permutation(p):
            i += 1
            t = solution(p)
            apply_transpositions(p, p.index(0), t)
            assert p == GOAL, f'p={p}, t={t}'
        else:
            with pytest.raises(ValueError):
                solution(p)


if __name__ == '__main__':
    test_solve()
