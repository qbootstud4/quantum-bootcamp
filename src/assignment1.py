import os
import math
import numpy as np
from numpy.typing import ArrayLike, NDArray
from typing import Tuple, Optional
import matplotlib.pyplot as plt


def print_chart(canvas: NDArray) -> None:
    """
    Print a multidimensional array to the standard output
    :param canvas:
    :return:
    """
    canvas_inter = [''.join(row) for row in canvas]
    print('\n'.join(canvas_inter))


def initialize_canvas(
    width: int,
    height: int,
    grid: bool = False,
) -> NDArray:
    """
    Initialize a 2D array based on given dimensions
    :param width:
    :param height:
    :param grid:
    :return:

    >>> initialize_canvas(2, 2).tolist()
    [['+', '+'], ['+', '+']]
    >>> initialize_canvas(5, 3, True).tolist()
    [['+', '-', '-', '-', '+'], ['|', '·', '·', '·', '|'], ['+', '-', '-', '-', '+']]
    """
    # initialize corr 2D array with space char
    canvas = np.empty((height, width), dtype="str")
    if grid:
        canvas[:] = '·'
    else:
        canvas[:] = ' '

    # fill corners
    canvas[[0, 0, -1, -1], [0, -1, 0, -1]] = '+'

    # fill edges, horizontal and then vertical
    canvas[0, 1:-1] = canvas[-1, 1:-1] = '-'
    canvas[1:-1, 0] = canvas[1:-1, -1] = '|'
    return canvas


def preprocess_data(
    x: ArrayLike,
    y: ArrayLike,
    canvas: NDArray,
) -> Tuple:
    """
    Min-max normalize each axis and scale it to width and height of the canvas
    :param x:
    :param y:
    :param canvas:
    :return:

    >>> width, height = 5, 5
    >>> canvas = initialize_canvas(width, height)
    >>> x = [0, 1, 2, 3]
    >>> y = [2, 4, 6, 8]
    >>> preprocess_data(x, y, canvas)[0][-1]
    4
    >>> preprocess_data(x, y, canvas)[1][1]
    1
    """
    assert len(x) == len(y)

    def _min_max_normalize(arr: NDArray) -> NDArray:
        return (arr - np.amin(arr)) / (np.amax(arr) - np.amin(arr))
    def _rescale(arr: NDArray, scale_factor: int) -> NDArray:
        return np.floor(arr * (scale_factor - 1))

    height, width = canvas.shape
    x, y = np.asarray(x), np.asarray(y)
    x_pre = _rescale(_min_max_normalize(x), width).astype(int)
    y_pre = _rescale(_min_max_normalize(y), height).astype(int)
    return x_pre, y_pre


def draw_points(
    x: ArrayLike,
    y: ArrayLike,
    canvas: NDArray,
    grid: bool,
) -> NDArray:
    """
    Draw the data points on a canvas.
    :param x:
    :param y:
    :param canvas:
    :param grid:
    :return:
    """
    assert len(x) == len(y)
    x_pre, y_pre = preprocess_data(x, y, canvas)
    if grid:
        canvas[y_pre, x_pre] = '*'
    else:
        canvas[y_pre, x_pre] = '·'
    return np.flip(canvas, axis=0)


def label_axis(
    canvas: NDArray,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    legend: Optional[str] = None,
) -> NDArray:
    """
    Adds x- and y-axis.
    :param canvas:
    :param x_min:
    :param x_max:
    :param y_min:
    :param y_max:
    :param legend:
    :return:
    """
    # create x-axis
    x_label = np.empty(canvas.shape[1], dtype='str')
    x_label[:] = ' '

    x_min = math.floor(x_min)
    x_max = math.ceil(x_max)
    x_label[0:len(str(x_min))] = list(str(x_min))
    x_label[-len(str(x_max)):] = list(str(x_max))

    # add legend to x-axis
    if legend is not None:
        legend_start = math.floor((len(x_label) - len(legend)) / 2)
        legend_end = -math.ceil((len(x_label) - len(legend)) / 2)
        x_label[legend_start:legend_end] = list(legend)

    # add both x-axis and legend to the canvas
    canvas = np.vstack((canvas, x_label))

    # create and add y-axis to the canvas
    y_label = np.empty((canvas.shape[0], 3), dtype="str")
    y_label[:] = ' '

    y_min = math.floor(y_min)
    y_max = math.ceil(y_max)
    y_label[-2, -len(str(y_min)):] = list(str(y_min))
    y_label[0, -len(str(y_max)):] = list(str(y_max))
    y_label = y_label.reshape(y_label.shape[0], -1)
    canvas = np.hstack((y_label, canvas))

    return canvas


def add_title(canvas: NDArray, title: str) -> NDArray:
    """
    Add title to the canvas.
    :param canvas:
    :param title:
    :return:
    """
    width = canvas.shape[1]
    title_arr = np.empty(width, dtype="str")
    title_arr[:] = ' '

    title_start = math.floor((width - len(title)) / 2)
    title_end = -math.ceil((width - len(title)) / 2)
    title_arr[title_start:title_end] = list(title)

    return np.vstack((title_arr, canvas))


def plot(
    x: ArrayLike,
    y: ArrayLike,
    display_grid: bool = False,
    height: int = 15,
    width: int = 100,
    title: str = '',
    legend: str = '',
):
    """
    A single function for plotting.
    :param x:
    :param y:
    :param display_grid:
    :param height:
    :param width:
    :param title:
    :param legend:
    :return:
    """
    canvas = initialize_canvas(width, height, display_grid)
    canvas = draw_points(x, y, canvas, display_grid)
    canvas = label_axis(
        canvas,
        np.amin(x),
        np.amax(x),
        np.amin(y),
        np.amax(y),
        legend,
    )
    canvas = add_title(canvas, title)
    print_chart(canvas)


def plot_matplotlib(
    x: ArrayLike,
    y: ArrayLike,
    display_grid: bool = False,
    height: int = 15,
    width: int = 100,
    title: str = '',
    legend: str = '',
):
    plt.figure(figsize=(width, height))
    plt.plot(x, y)
    plt.suptitle(title)
    plt.xlabel(legend)
    save_at = '_'.join(title.split(' ')).lower() + '.png'
    if display_grid:
        plt.grid()
    plt.savefig(os.path.join('data', save_at))



def main():
    # Example 1
    scale = 0.1
    n = int(8 * math.pi / scale)
    x = [scale * i for i in range(n)]
    y = [math.sin(scale * i) for i in range(n)]
    plot(
        x, y,
        display_grid=True,
        height=15,
        title="The sine function",
        legend="f(x) = sin(x), where 0 <= x <= 8π"
    )
    plot_matplotlib(
        x, y,
        display_grid=True,
        height=5,
        width=12,
        title="The sine function",
        legend="f(x) = sin(x), where 0 <= x <= 8π"
    )

    # Example 2
    scale = 0.1
    n = int(2 * math.pi / scale)
    x = [scale * i for i in range(n)]
    y = [math.cos(scale * i) for i in range(n)]
    plot(
        x, y,
        width=50,
        title="The cosine function",
        legend="f(x) = cos(x), where 0 <= x <= 2π"
    )
    plot_matplotlib(
        x, y,
        height=5,
        width=12,
        title="The cosine function",
        legend="f(x) = cos(x), where 0 <= x <= 2π"
    )

    # Example 3
    y = [ord(c) for c in 'ASCII Plotter example']
    n = len(y)
    x = [i for i in range(n)]
    plot(
        x, y,
        title="Plotting Random Data",
        legend="f(x) = random data"
    )
    plot_matplotlib(
        x, y,
        height=5,
        width=12,
        title="Plotting Random Data",
        legend="f(x) = random data"
    )


if __name__ == '__main__':
    main()