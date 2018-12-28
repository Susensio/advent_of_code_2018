from datetime import datetime
import pandas as pd
from collections import Counter
from string import ascii_lowercase

# PART 1
INPUT_FILENAME = 'input.txt'

test_input = 'dabAcCaCBAcCcaDA'


def read_file():
    with open(INPUT_FILENAME) as file:
        return next(file).strip()


def trigger_polymer(polymer):
    """
    >>> trigger_polymer(test_input)
    'dabCBAcaDA'
    >>> trigger_polymer('abcdefgGFEDCBA')
    ''
    >>> trigger_polymer('dabAaBAaDA')
    'daDA'
    >>> trigger_polymer('abAcCaCBAcCc')
    'abCBAc'
    """
    # print(polymer)
    reacted = list(polymer)
    for i in range(len(reacted) - 1, 0, -1):
        # print(reacted)
        try:
            if units_are_reactive(reacted[i], reacted[i - 1]):
                # print(''.join(reacted))
                reacted.pop(i)
                reacted.pop(i - 1)
        except IndexError:
            pass
            # print(e.with_traceback())
            # print(i, reacted)
    return ''.join(reacted)


def units_are_reactive(u1, u2):
    """
    >>> units_are_reactive('u', 'U')
    True
    >>> units_are_reactive('O', 'o')
    True
    >>> units_are_reactive('a', 'a')
    False
    >>> units_are_reactive('m', 'N')
    False
    >>> units_are_reactive('c', 'a')
    False
    """
    return u1.swapcase() == u2
    # return (u1.isupper() ^ u2.isupper()) & (u1.lower() == u2.lower())


# PART 2
def remove_unit_instances(polymer, unit):
    """
    >>> remove_unit_instances(test_input, 'a')
    'dbcCCBcCcD'
    >>> remove_unit_instances(test_input, 'b')
    'daAcCaCAcCcaDA'
    >>> remove_unit_instances(test_input, 'c')
    'dabAaBAaDA'
    >>> remove_unit_instances(test_input, 'd')
    'abAcCaCBAcCcaA'
    """
    return polymer.replace(unit.lower(), '').replace(unit.upper(), '')


def improve_and_react_polymer(polymer):
    """
    Return shortest polymer than can be produced by removing all units of exactly one type and fully reacting the result.

    >>> improve_and_react_polymer(test_input)
    'daDA'
    """
    letters = set(polymer.lower())
    return min((trigger_polymer(remove_unit_instances(polymer, unit)) for unit in letters), key=len)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    reaction = trigger_polymer(read_file())
    print(f"Part 1:\n\t number of units = {len(reaction)}")

    reaction = improve_and_react_polymer(read_file())
    print(f"Part 2:\n\t number of units = {len(reaction)}")
