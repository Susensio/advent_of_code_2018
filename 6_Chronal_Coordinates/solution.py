from copy import deepcopy
from collections import Counter

# PART 1
INPUT_FILENAME = 'input.txt'

test_coordinates = [
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9),
]


def iter_file():
    with open(INPUT_FILENAME) as file:
        for line in file:
            x, y = line.split(', ')
            yield int(x), int(y)


# def largest_area(coordinates):
#     """ Size of the largest area that isn't infinte.
#     >>> largest_area(test_coordinates)
#     17
#     """
#     pass


class Grid:
    """
    >>> g = Grid(test_coordinates)
    >>> g.bounding_box
    ((1, 1), (8, 9))
    >>> g[1, 1]
    0
    >>> g[8, 9]
    5
    >>> g[10, 10]
    Traceback (most recent call last):
    ...
    IndexError: Coordinates out of bounding box
    >>> g[0, 0]
    Traceback (most recent call last):
    ...
    IndexError: Coordinates out of bounding box

    >>> list(g.nearest_cells((1,1)))
    [None, None]
    >>> list(g.nearest_cells((2,1)))
    [None, 0, None]

    >>> g.filled
    False

    >>> g.boundary_points
    (0, 1, 2, 5)

    >>> g.largest_area
    17

    >>> g.distances((1,1))
    [0, 5, 9, 5, 8, 15]

    >>> g.nearest_point((1,1))
    0
    >>> g.nearest_point((4,2))
    3
    >>> g.nearest_point((5,1))
    '.'

    >>> g.len_total_distance_less_than(32)
    16
    """

    def __init__(self, targets):
        self.targets = tuple(targets)
        self.bounding_box = tuple(zip(*tuple(((min(c), max(c))
                                              for c in zip(*self.targets)))))
        # Initialize empty map
        self.map = self.empty_map()

        for num, coord in enumerate(self.targets):
            self[coord] = num

        ((x_min, y_min), (x_max, y_max)) = self.bounding_box
        self.boundary_points = tuple(i for i, (x, y) in enumerate(self.targets) if x in {x_min, x_max} or y in {y_min, y_max})

    def empty_map(self):
        return [[None for _ in self.y_range] for _ in self.x_range]

    @property
    def x_range(self):
        ((x_min, _), (x_max, _)) = self.bounding_box
        return range(x_min, x_max + 1)

    @property
    def y_range(self):
        ((_, y_min), (_, y_max)) = self.bounding_box
        return range(y_min, y_max + 1)

    def corrected_coordinates(self, coordinates):
        ((x_min, y_min), (x_max, y_max)) = self.bounding_box
        x, y = coordinates
        if not(x_min <= x <= x_max and y_min <= y <= y_max):
            # print(x, y, self.bounding_box)
            raise IndexError("Coordinates out of bounding box")

        return x - x_min, y - y_min

    def __getitem__(self, coordinates):
        x, y = self.corrected_coordinates(coordinates)
        return self.map[x][y]

    def __setitem__(self, coordinates, value):
        x, y = self.corrected_coordinates(coordinates)
        self.map[x][y] = value

# OLD ###################
    def nearest_cells(self, coordinates):
        x, y = coordinates

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            try:
                yield self[x + dx, y + dy]
            except IndexError:
                pass

    def nearest_cell(self, coordinates):
        cells = {c for c in self.nearest_cells(coordinates) if c is not None}
        if len(cells) == 1:
            return cells.pop()
        elif len(cells) > 1:
            return '.'
        else:
            return None

    def grow(self):
        while not self.filled:
            new_grid = deepcopy(self)

            for x in self.x_range:
                for y in self.y_range:
                    if self[x, y] == None:
                        new_grid[x, y] = self.nearest_cell((x, y))

            self = new_grid
        return self
###################

    @property
    def filled(self):
        return all(self[x, y] is not None for x in self.x_range for y in self.y_range)

    def __str__(self):
        header = '\t' + '\t'.join(map(str, self.x_range))

        y_range = list(self.y_range)
        body = '\n'.join(str(y_range[i]) + '\t' + '\t'.join(str(cell) if cell is not None else ' ' for cell in row) for i, row in enumerate(map(list, zip(*self.map))))

        return header + '\n' + body + '\n'

    @property
    def largest_area(self):
        # self = self.grow()
        self.fill()
        cell_candidates = (self[x, y] for x in self.x_range for y in self.y_range if self[x, y] not in self.boundary_points)
        count = Counter(cell_candidates)
        largest, size = count.most_common()[0]
        return size

    def distances(self, coordinates):
        x, y = coordinates
        return [abs(x - target[0]) + abs(y - target[1])
                for target in self.targets]

    def nearest_point(self, coordinates):
        distances = self.distances(coordinates)
        indexes = [i for i, x in enumerate(distances) if x == min(distances)]
        if len(indexes) == 1:
            return indexes[0]
        else:
            return '.'

    def fill(self):
        freeze = deepcopy(self)

        for x in self.x_range:
            for y in self.y_range:
                self[x, y] = freeze.nearest_point((x, y))

### PART 2 ###
    def len_total_distance_less_than(self, total_distance):
        return len([_ for x in self.x_range for y in self.y_range if sum(self.distances((x, y))) < total_distance])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # g = Grid(test_coordinates)
    # g.fill()
    # # print(g.distances((1, 1)))

    g = Grid(iter_file())
    print(f"Part 1:\n\t largest area = {g.largest_area}")

    print(f"Part 2:\n\t region rize = {g.len_total_distance_less_than(10000)}")
    # print(f"Part 2:\n\t number of units = {len(reaction)}")
