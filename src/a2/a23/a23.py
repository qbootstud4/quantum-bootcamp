#!/usr/bin/env python
"""Assignment 2 Part 3"""

from typing import IO
from collections import namedtuple
from random import randint, uniform
from dataclasses import dataclass


class HtmlDoc:
    """an html document"""
    TAB: str = "   "  # HTML indentation tab (default: three spaces)

    def __init__(self, file_name: str, window_title: str) -> None:
        self.__fnam: str = file_name
        self.__wintitle: str = window_title
        self.fd: IO[str] = self.open_html_file()

    def generate_html_file(self) -> None:
        """write an empty html document"""
        self.write_html_head()
        self.write_html_tail()

    def open_html_file(self) -> IO[str]:
        """open the html document"""
        return open(self.__fnam, "w")

    def close_html_file(self) -> None:
        """close the html document"""
        self.fd.close()

    def __write_html_comment(self, t: int, com: str) -> None:
        """
        write a comment in the html document
        :param t:
        :param com:
        :return:
        """
        ts: str = HtmlDoc.TAB * t
        self.fd.write(f"{ts}<!--{com}-->\n")

    def write_html_line(self, t: int, line: str) -> None:
        """
        write a line in the html document
        :param t:
        :param line:
        :return:
        """
        ts: str = HtmlDoc.TAB * t
        self.fd.write(f"{ts}{line}\n")

    def write_html_head(self) -> None:
        """write the html header"""
        self.write_html_line(0, "<html>")
        self.write_html_line(0, "<head>")
        self.write_html_line(1, f"<title>{self.__wintitle}</title>")
        self.write_html_line(0, "</head>")
        self.write_html_line(0, "<body>")

    def write_html_tail(self) -> None:
        """write the html footer"""
        self.write_html_line(0, "</body>")
        self.write_html_line(0, "</html>")


class SvgCanvas:
    """an svg canvas"""
    def __init__(self, tlx: int, tly: int, w: int, h: int) -> None:
        self.__tlx: int = tlx
        self.__tly: int = tly
        self.__w: int = w
        self.__h: int = h

    def gen_art(self, hd: HtmlDoc, figures: list, t: int):
        """
        generate an art on the svg canvas
        :param hd:
        :param figures:
        :param t:
        :return:
        """
        hd.write_html_line(t, f'<svg height="{self.__h}" width="{self.__w}">')
        for figure in figures:
            figure.draw_shape_line(hd, t * 2)
        hd.write_html_line(t, f'</svg>')


# shorten shape parameters using namedtuples
Point = namedtuple('Point', 'x y')
Color = namedtuple('Color', 'red green blue')


class Shape:
    """a shape"""
    def __init__(
        self,
        point: Point,
        color: Color,
        op: float,
    ) -> None:
        """
        initialize a shape
        :param point:
        :param color:
        :param op:
        """
        self.x: int = point.x
        self.y: int = point.y
        self.red: int = color.red
        self.green: int = color.green
        self.blue: int = color.blue
        self.op: float = op


class Circle(Shape):
    """a circle"""
    def __init__(self, rad: int, point: Point, color: Color, op: float) -> None:
        """
        initialize a circle
        :param rad:
        :param point:
        :param color:
        :param op:
        """
        super().__init__(point, color, op)
        self.__rad: int = rad

    def draw_shape_line(self, hd: HtmlDoc, t: int) -> None:
        """
        draw a circle
        :param hd:
        :param t:
        :return:
        """
        line1: str = f'<circle cx="{self.x}" cy="{self.y}" r="{self.__rad}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        hd.write_html_line(t, line1 + line2)


class Rectangle(Shape):
    """a rectangle"""
    def __init__(self, point: Point, width: int, height: int, color: Color, op: float) -> None:
        """
        initialize a rectangle
        :param point:
        :param width:
        :param height:
        :param color:
        :param op:
        """
        super().__init__(point, color, op)
        self.__width: int = width
        self.__height: int = height

    def draw_shape_line(self, hd: HtmlDoc, t: int) -> None:
        """
        draw a rectangle
        :param hd:
        :param t:
        :return:
        """
        line1: str = f'<rect x="{self.x}" y="{self.y}" width="{self.__width}" height="{self.__height}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        hd.write_html_line(t, line1 + line2)


class Ellipse(Shape):
    """an ellipse"""
    def __init__(self, point: Point, rx: int, ry: int, color: Color, op: float) -> None:
        """
        initialize an ellipse
        :param point:
        :param rx:
        :param ry:
        :param color:
        :param op:
        """
        super().__init__(point, color, op)
        self.__rx: int = rx
        self.__ry: int = ry

    def draw_shape_line(self, hd: HtmlDoc, t: int) -> None:
        """
        draw an ellipse
        :param hd:
        :param t:
        :return:
        """
        line1: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.__rx}" ry="{self.__ry}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        hd.write_html_line(t, line1 + line2)


class ShapeFactory:
    """map specs to a shape instance"""

    @classmethod
    def from_specs(cls, specs):
        """get shape from specs"""
        point = Point(specs.x, specs.y)
        color = Color(specs.red, specs.green, specs.blue)
        if specs.shape == 0:
            return Circle(
                rad=specs.rad,
                point=point,
                color=color,
                op=specs.op,
            )
        elif specs.shape == 1:
            return Rectangle(
                point=point,
                width=specs.width,
                height=specs.height,
                color=color,
                op=specs.op,
            )
        else:
            return Ellipse(
                point=point,
                rx=specs.rx,
                ry=specs.ry,
                color=color,
                op=specs.op,
            )


@dataclass
class ArtConfig:
    """art configuration"""
    SHAPE: int = tuple((0, 2))
    RAD: tuple = tuple((0, 100))
    X: tuple = tuple()
    Y: tuple = tuple()
    RX: tuple = tuple((10, 30))
    RY: tuple = tuple((10, 30))
    WIDTH: tuple = tuple((10, 100))
    HEIGHT: tuple = tuple((10, 100))
    RED: tuple = tuple((0, 255))
    GREEN: tuple = tuple((0, 255))
    BLUE: tuple = tuple((0, 255))
    OP: tuple = tuple((0., 1.))

    def get_attr(self, name: str):
        return getattr(self, name.upper())

    def set_attr(self, name: str, value: tuple):
        setattr(self, name.upper(), value)


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


Canvas: namedtuple = namedtuple('Canvas', 'w h')
Specs: namedtuple = namedtuple('Props', 'shape x y rad rx ry width height red green blue op')


class Batch:
    """create a batch of shapes"""
    def __init__(self, canvas: Canvas, num_shapes: int):
        """
        initialize a batch of shapes
        :param canvas:
        :param num_shapes:
        """
        self.canvas = canvas
        self.num_shapes = num_shapes

        self.art_config = ArtConfig()
        self.art_config.set_attr('x', tuple((0, self.canvas.w)))
        self.art_config.set_attr('y', tuple((0, self.canvas.h)))

    def create_batch(self):
        """
        create batch
        :return:
        """
        props: list = [
            'shape', 'x', 'y', 'rad', 'rx', 'ry',
            'width', 'height', 'red', 'green', 'blue', 'op',
        ]
        shapes = []
        for shape_idx in range(self.num_shapes):
            shape = []
            for prop in props:
                start, end = self.art_config.get_attr(prop)
                if end <= 1:
                    value = GenRandom.gen_float_in_range(start, end)
                else:
                    value = GenRandom.gen_int_in_range(start, end)
                shape.append(value)
            shapes.append(Specs(*shape))
        return shapes


def main() -> None:
    canvas: namedtuple = Canvas(800, 500)
    for i in range(1, 4):
        hd: HtmlDoc = HtmlDoc(f"a2-3{i}.html", f"MyPart{i}")
        hd.open_html_file()
        hd.write_html_head()

        batch: Batch = Batch(canvas, 2000)
        shape_specs: list = batch.create_batch()
        shapes: list = []
        for specs in shape_specs:
            shapes.append(ShapeFactory().from_specs(specs))
        cn: SvgCanvas = SvgCanvas(tlx=0, tly=0, w=canvas.w, h=canvas.h)
        cn.gen_art(hd, shapes, 1)

        hd.write_html_tail()
        hd.close_html_file()

if __name__ == "__main__":
    print(__doc__)
    main()
