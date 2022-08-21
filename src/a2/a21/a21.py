#!/usr/bin/env python
"""Assignment 2 Part 1"""

from typing import IO
from collections import namedtuple


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
            if isinstance(figure, Circle):
                figure.draw_circle_line(hd, t * 2)
            elif isinstance(figure, Rectangle):
                figure.draw_rectangle_line(hd, t * 2)
            elif isinstance(figure, Ellipse):
                figure.draw_ellipse_line(hd, t * 2)
        hd.write_html_line(t, f'</svg>')


# shorten shape parameters using namedtuples
Point = namedtuple('Point', 'x y')
Color = namedtuple('Color', 'red green blue')


class Shape:
    """a shape"""
    def __init__(self, point: Point, color: Color, op: float) -> None:
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
        print(self.x)

    def draw_circle_line(self, hd: HtmlDoc, t: int) -> None:
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

    def draw_rectangle_line(self, hd: HtmlDoc, t: int) -> None:
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

    def draw_ellipse_line(self, hd: HtmlDoc, t: int) -> None:
        """
        draw an ellipse
        :param hd:
        :param t:
        :return:
        """
        line1: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.__rx}" ry="{self.__ry}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        hd.write_html_line(t, line1 + line2)


def main() -> None:
    hd: HtmlDoc = HtmlDoc("part1.html", "MyPart1")
    hd.open_html_file()
    hd.write_html_head()

    figures = [
        Circle(rad=20, point=Point(10, 20), color=Color(100, 200, 255), op=0.5),
        Circle(rad=55, point=Point(50, 120), color=Color(100, 100, 255), op=0.3),
        Rectangle(point=Point(10, 10), width=50, height=60, color=Color(255, 100, 200), op=0.8),
        Ellipse(point=Point(40, 45), rx=10, ry=40, color=Color(200, 100, 200), op=0.6),
    ]
    cn: SvgCanvas = SvgCanvas(tlx=0, tly=0, w=500, h=150)
    cn.gen_art(hd, figures, 1)

    hd.write_html_tail()
    hd.close_html_file()


if __name__ == "__main__":
    print(__doc__)
    main()