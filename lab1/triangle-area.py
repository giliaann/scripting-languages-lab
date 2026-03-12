import sys


def count_area(base, height):
    return base * height / 2


def get_user_input():
    print("Enter triangle data.")
    base = input("Base: ")
    height = input("Height: ")
    return base, height


def parse_positive_integer(n):
    n = int(n)
    if n <= 0:
        raise ValueError("Invalid argument - value must be positive")
    return n


def main():

    base, height = get_user_input()

    valid_data = True

    try:
        base = parse_positive_integer(base)
    except ValueError as e:
        print(f"Invalid base - {e}", file=sys.stderr)
        valid_data = False

    try:
        height = parse_positive_integer(height)
    except ValueError as e:
        print(f"Invalid height - {e}", file=sys.stderr)
        valid_data = False

    if not valid_data:
        return

    print(f"Area of given triangle: {count_area(base, height)}")


if __name__ == "__main__":
    main()
