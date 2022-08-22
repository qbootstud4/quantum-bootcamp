#!/usr/bin/env python
"""Assignment 2 Part 2"""
from random import randint, uniform
from dataclasses import dataclass
from collections import namedtuple
from typing import NamedTuple


@dataclass
class ArtConfig:
    """art configuration"""
    SHA: int = tuple((0, 2))
    RAD: tuple = tuple((0, 100))
    X: tuple = tuple()
    Y: tuple = tuple()
    RX: tuple = tuple((10, 30))
    RY: tuple = tuple((10, 30))
    W: tuple = tuple((10, 100))
    H: tuple = tuple((10, 100))
    R: tuple = tuple((0, 255))
    G: tuple = tuple((0, 255))
    B: tuple = tuple((0, 255))
    OP: tuple = tuple((0., 1.))

    def get_attr(self, name: str):
        return getattr(self, name)

    def set_attr(self, name: str, value: tuple):
        setattr(self, name, value)


class GenRandom:
    """a random number generator"""

    @classmethod
    def gen_int_in_range(cls, a: int, b: int) -> int:
        """
        generate a random integer in range (a, b)
        :param a:
        :param b:
        :return:
        """
        return randint(a, b)

    @classmethod
    def gen_float_in_range(cls, a: float, b: float) -> float:
        """
        generate a random float in range (a, b)
        :param a:
        :param b:
        :return:
        """
        return round(uniform(a, b), 1)


Canvas: NamedTuple = namedtuple('Canvas', 'w h')


class SvgTable:
    """a svg table"""
    COLS: list = [
        'SHA', 'X', 'Y', 'RAD', 'RX', 'RY',
        'W', 'H', 'R', 'G', 'B', 'OP',
    ]
    def __init__(self, canvas: Canvas, num_rows: int):
        """
        initialize an svg table
        :param canvas:
        :param num_rows:
        """
        self.canvas = canvas
        self.num_rows = num_rows

        self.art_config = ArtConfig()
        self.art_config.set_attr('X', tuple((0, self.canvas.w)))
        self.art_config.set_attr('Y', tuple((0, self.canvas.h)))

    def create_table(self) -> str:
        """
        create a table
        :return:
        """
        def _create_row(row: list) -> str:
            """
            create a row
            :param row:
            :return:
            """
            str_row = [f"{str(val):>6}" for val in row]
            return f"".join(str_row)

        header = _create_row(['CNT'] + self.COLS)
        table = [header]
        for row_idx in range(self.num_rows):
            row = [row_idx]
            for col in self.COLS:
                start, end = self.art_config.get_attr(col)
                if end <= 1:
                    row.append(GenRandom.gen_float_in_range(start, end))
                else:
                    row.append(GenRandom.gen_int_in_range(start, end))
            table.append(_create_row(row))
        return '\n'.join(table)


def main():
    table = SvgTable(
        canvas=Canvas(500, 300),
        num_rows=10,
    ).create_table()

    with open('a22.txt', 'w') as f:
        f.write(table)


if __name__ == '__main__':
    print(__doc__)
    main()