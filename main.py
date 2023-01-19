"""Валидация карты"""


import sys


TEST_MODE = False


class HexMap:
    non_region_chars = "._"

    def __init__(self, n: int, m: int):
        self.lines = n
        self.cols = m
        self.map = []
        self._create_map()
        self.regions = self._get_regions()
        self.current_region = ""

    def _create_map(self):
        """Создать карту"""
        self.map.append(["_"] * (self.cols + 4))
        for _ in range(self.lines):
            line = input()
            self.map.append(["_"] * 2 + [*line] + ["_"] * 2)
        self.map.append(["_"] * (self.cols + 4))

    def _get_regions(self):
        """Получить перечень регионов"""
        regions = set(sum(self.map, []))
        for c in self.non_region_chars:
            regions.discard(c)
        return tuple(sorted(regions))

    def _scout_region(self, i, j):
        """Разведать регион"""
        if self.map[i][j] != self.current_region:
            return False
        self.map[i][j] = self.current_region.lower()
        # left-top
        self._scout_region(i - 1, j - 1)
        # right-top
        self._scout_region(i - 1, j + 1)
        # left
        self._scout_region(i, j - 2)
        # right
        self._scout_region(i, j + 2)
        # left-bottom
        self._scout_region(i + 1, j - 1)
        # right-bottom
        self._scout_region(i + 1, j + 1)

    def _get_1d_map(self):
        """Получить одномерную карту"""
        return sum(self.map, [])

    def validate_map(self) -> bool:
        """Валидировать карту"""
        for r in self.regions:
            self.current_region = r
            map_1d = self._get_1d_map()
            indx = map_1d.index(self.current_region)
            i, j = divmod(indx, self.cols + 4)
            self._scout_region(i, j)
            map_1d = self._get_1d_map()
            if self.current_region in map_1d:
                return False

        return True


def main():
    if TEST_MODE:
        input_file = open("input_data")
        tmp_in = sys.stdin
        sys.stdin = input_file

    t = int(input())
    for _ in range(t):
        # новая карта
        n, m = map(int, input().split())
        new_map = HexMap(n, m)
        print(("NO", "YES")[new_map.validate_map()])

    if TEST_MODE:
        sys.stdin = tmp_in
        input_file.close()


if __name__ == '__main__':
    main()
