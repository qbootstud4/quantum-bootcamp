def multiplier(x: int, y: int) -> int:
    """
    :param x:
    :param y:
    :return:

    >>> multiplier(2, 2)
    4
    >>> multiplier(5, 2)
    10
    """
    return x * y


def main():
    """
    >>> main()
    hello
    """
    print('hello')


if __name__ == '__main__':
    import doctest
    doctest.testmod()