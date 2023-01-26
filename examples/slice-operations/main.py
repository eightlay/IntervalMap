from ijim import IntervalMap


def main():
    im = IntervalMap[int, int](
        0,
        [],
        []
    )
    print(im)

    im.slice_add(2, 4, 1)
    print(im)

    im.slice_sub(2, 4, 1)
    print(im)


if __name__ == "__main__":
    main()
