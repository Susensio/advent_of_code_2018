from collections import Counter

# PART 1
INPUT_FILENAME = 'input.txt'


def iter_file():
    with open(INPUT_FILENAME) as file:
        for line in file:
            yield line


def calculate_checksum(items):
    """
    >>> test_input = [
    ...     'abcdef',
    ...     'bababc',
    ...     'abbcde',
    ...     'abcccd',
    ...     'aabcdd',
    ...     'abcdee',
    ...     'ababab',
    ... ]
    >>> calculate_checksum(test_input)
    12
    """
    checksum_counter = Counter()
    for item in items:
        letter_count = Counter(item.strip())
        counts = set(letter_count.values())   # Set because only counts as one
        checksum_counter += Counter(counts)
    checksum = checksum_counter[3] * checksum_counter[2]
    return checksum


# PART 2
def differ_by_one_char(s1, s2):
    """
    >>> differ_by_one_char('fghij', 'fguij')
    True
    >>> differ_by_one_char('abcde', 'axcye')
    False
    """
    eq = [c1 == c2 for c1, c2 in zip(s1, s2)]
    count = Counter(eq)
    return count[False] == 1


from itertools import combinations


def find_similar(items):
    """
    >>> test_input = [
    ...     'abcde',
    ...     'fghij',
    ...     'klmno',
    ...     'pqrst',
    ...     'fguij',
    ...     'axcye',
    ...     'wvxyz',
    ... ]
    >>> find_similar(test_input)
    ('fghij', 'fguij')
    """
    for pair in combinations(items, 2):
        if differ_by_one_char(*pair):
            return pair


def common_chars(word1, word2):
    """
    >>> common_chars('fghij', 'fguij')
    'fgij'
    """
    return ''.join(c1 for c1, c2 in zip(word1, word2) if c1 == c2)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f"Part 1: {calculate_checksum(iter_file())}")

    print(f"Part 2: {common_chars(*find_similar(iter_file()))}")
