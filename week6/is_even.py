def is_even_permutation(p):
    visited = [False] * (len(p) - 1)
    parity = True
    for (i, x) in enumerate(p[:-1]):
        if visited[i]:
            continue
        visited[i] = True
        j = x - 1
        while j != i:
            parity = not parity
            visited[j] = True
            j = p[j] - 1
    return parity


if __name__ == '__main__':
    assert is_even_permutation([1, 2, 3, 0]) is True
    assert is_even_permutation([2, 1, 3, 0]) is False
