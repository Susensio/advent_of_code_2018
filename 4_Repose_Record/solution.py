from datetime import datetime
import pandas as pd
from collections import Counter

# PART 1
INPUT_FILENAME = 'input.txt'

test_input = [
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up',
]


def iter_file():
    with open(INPUT_FILENAME) as file:
        for line in file:
            yield line


class Shift:
    """
    >>> s = Shift(1)
    >>> s.falls_sleep(5)
    >>> s.wakes_up(10)
    >>> s.falls_sleep(40)
    >>> s.wakes_up(50)
    >>> s.minutes_asleep
    15
    >>> s.is_asleep(5)
    True
    >>> s.is_asleep(10)
    False
    >>> list(s.asleep_minutes_iterator)
    [5, 6, 7, 8, 9, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    """

    def __init__(self, guard):
        self.guard = guard
        self.fall_sleep_times = []
        self.wake_up_times = []

    def falls_sleep(self, minute):
        self.fall_sleep_times.append(minute)

    def wakes_up(self, minute):
        self.wake_up_times.append(minute)

    @property
    def minutes_asleep(self):
        return sum(wake - fall for fall, wake in self.intervals)

    @property
    def intervals(self):
        return zip(self.fall_sleep_times, self.wake_up_times)

    @property
    def asleep_minutes_iterator(self):
        return (minute for minute in range(0, 60) if self.is_asleep(minute))

    def is_asleep(self, minute):
        for fall, wake in self.intervals:
            if fall <= minute < wake:
                return True
        return False


def parse_records(records):
    """
    >>> parsed = parse_records(test_input)
    >>> len(parsed)
    5
    >>> parsed[0].guard
    '10'
    >>> parsed[-1].guard
    '99'
    >>> parsed[0].minutes_asleep
    45
    """
    empty = [False for _ in range(60)]
    parsed = []
    fall_sleep_minute = 0
    for record in sorted(records):
        if 'Guard' in record:    # New shift
            guard_id = record.split()[3][1:]
            shift = Shift(guard_id)
            parsed.append(shift)
        else:
            minute = int(record[15:17])
            # print(minute)
            if 'falls' in record:
                shift.falls_sleep(minute)
            else:
                shift.wakes_up(minute)
    return parsed


def group_by_guard(parsed):
    """
    >>> parsed = parse_records(test_input)
    >>> grouped = group_by_guard(parsed)
    >>> len(grouped['10'])
    2
    >>> len(grouped['99'])
    3
    """
    grouped = {}
    for shift in parsed:
        try:
            grouped[shift.guard].append(shift)
        except KeyError:
            grouped[shift.guard] = [shift]
    return grouped


def most_time_asleep_guard(grouped):
    """
    >>> parsed = parse_records(test_input)
    >>> grouped = group_by_guard(parsed)
    >>> most_time_asleep_guard(grouped)
    '10'
    """
    return max(grouped.values(), key=lambda shifts: sum(shift.minutes_asleep for shift in shifts))[0].guard


def most_common_sleep_minute(shifts):
    """
    >>> parsed = parse_records(test_input)
    >>> grouped = group_by_guard(parsed)
    >>> minute, count = most_common_sleep_minute(grouped['10'])
    >>> minute
    24
    >>> count
    2
    >>> most_common_sleep_minute(grouped['99'])
    (45, 3)
    """
    # print(list(shifts.asleep_minutes_iterator))
    counter = Counter(minute for shift in shifts for minute in shift.asleep_minutes_iterator)
    # print(counter)
    try:
        return counter.most_common(1)[0]
    except IndexError:
        return (0, 0)


def most_frequently_asleep_guard(grouped):
    """
    >>> parsed = parse_records(test_input)
    >>> grouped = group_by_guard(parsed)
    >>> most_frequently_asleep_guard(grouped)
    '99'
    """
    return max(grouped.values(), key=lambda shifts: most_common_sleep_minute(shifts)[1])[0].guard


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    parsed = parse_records(iter_file())
    grouped = group_by_guard(parsed)
    lazy_guard = most_time_asleep_guard(grouped)
    shifts = grouped[lazy_guard]
    minute, count = most_common_sleep_minute(shifts)

    print(f"Part 1:\n\tguard id = {lazy_guard}\n\tminute = {minute}\n\tproduct = {int(lazy_guard) * minute}")

    predictable_guard = most_frequently_asleep_guard(grouped)
    shifts = grouped[predictable_guard]
    minute, count = most_common_sleep_minute(shifts)

    print(f"\nPart 2:\n\tguard id = {predictable_guard}\n\tminute = {minute}\n\tproduct = {int(predictable_guard) * minute}")
