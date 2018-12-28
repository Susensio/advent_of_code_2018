INPUT_FILENAME = 'input.txt'

# PART 1


def iterate_file():
    with open(INPUT_FILENAME) as file:
        for line in file:
            sign = line[0]
            number = int(line[1:].strip())
            if sign == '-':
                number = - number
            yield number


def sum_all_freqs():
    freq = 0
    for change in iterate_file():
        freq += change
    return freq


print(sum_all_freqs())


# PART 2
def find_first_twice_seen_freq():
    freq = 0
    freqs_seen = set()
    while True:
        for change in iterate_file():
            freq += change
            if freq in freqs_seen:
                return freq
            else:
                freqs_seen.add(freq)


print(find_first_twice_seen_freq())
