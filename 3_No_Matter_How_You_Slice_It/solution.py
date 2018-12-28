import re

# PART 1
INPUT_FILENAME = 'input.txt'
PARSE_LINE = re.compile(r'''[#]
                            (?P<id>\d*)
                            \s@\s
                            (?P<left>\d*)
                            ,
                            (?P<top>\d*)
                            :\s
                            (?P<width>\d*)
                            x
                            (?P<height>\d*)
                            ''', flags=re.X)


def iter_file():
    with open(INPUT_FILENAME) as file:
        for line in file:
            yield line


def parse_claim(claim):
    """
    >>> test_input = '#1 @ 1,3: 4x4'
    >>> parse_claim(test_input)
    {'id': 1, 'left': 1, 'top': 3, 'width': 4, 'height': 4}
    """
    parsed = PARSE_LINE.match(claim).groupdict()
    return {k: int(v) for k, v in parsed.items()}


def parse_claims(raw):
    for claim in raw:
        yield parse_claim(claim)


def process_claims(claims):
    """
    fabric is a sparse map that uses a dict structure:
    fabric[(x,y)] = claim['id'] or 'X' if overlapping
    """
    fabric = {}
    for claim in claims:
        for x in range(claim['left'], claim['left'] + claim['width']):
            for y in range(claim['top'], claim['top'] + claim['height']):
                if fabric.get((x, y), None):
                    fabric[(x, y)] = 'X'
                else:
                    fabric[(x, y)] = claim['id']
    return fabric


def count_overlaps(fabric):
    """
    >>> test_input = [
    ... '#1 @ 1,3: 4x4',
    ... '#2 @ 3,1: 4x4',
    ... '#3 @ 5,5: 2x2',
    ... ]
    >>> fabric = process_claims(parse_claims(test_input))
    >>> count_overlaps(fabric)
    4
    """
    return len([v for v in fabric.values() if v == 'X'])


# PART 2
def find_non_overlapping(fabric, claims):
    for claim in claims:
        if not claim_overlaps(claim, fabric):
            return claim['id']


def claim_overlaps(claim, fabric):
    return not all(claim['id'] == fabric[(x, y)]
                   for x in range(claim['left'], claim['left'] + claim['width'])
                   for y in range(claim['top'], claim['top'] + claim['height']))

    # def print_fabric(fabric):
    #     width = max(x for x, y in fabric.keys())
    #     height = max(y for x, y in fabric.keys())
    #     for x in range(width + 1):
    #         print(''.join(fabric.get((x, y), '.') for y in range(height + 1)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    fabric = process_claims(parse_claims(iter_file()))
    print(f"Part 1: {count_overlaps(fabric)}")

    claims = parse_claims(iter_file())
    print(f"Part 2: {find_non_overlapping(fabric, claims)}")
