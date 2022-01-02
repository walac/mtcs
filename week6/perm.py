def convert(transposition):
    i, j = transposition
    assert i != j
    i, j = min(i, j), max(i, j)
    return [(s, s + 1) for s in range(i, j)] + \
            [(s, s + 1) for s in
                    reversed(range(i, j - 1))]

def transform(first, second):
	assert len(first) == len(second)
	n = len(first)
	assert set(first) == set(range(n))
	assert set(second) == set(range(n))
	transpositions = []
	current = list(first)
	for i in range(n):
		if current[i] != second[i]:
			idx = current.index(second[i])
			assert idx != i
			transpositions.extend((convert((i, idx))))
			current[i], current[idx] = current[idx], current[i]
		assert current[i] == second[i]
	return transpositions

print(transform([0, 1, 2, 3, 4, 5], [1, 3, 2, 0, 5, 4]))

