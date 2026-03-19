import sys


def r_chars_count() -> int:
    counter = 0

    divisor_series = 0
    max_divisors = 5

    c = sys.stdin.read(1)

    while c:
        if c == "-":
            divisor_series += 1
            # eof sequence found
            if divisor_series >= max_divisors:
                return counter
        else:
            counter += divisor_series
            divisor_series = 0

            if not c.isspace():
                counter += 1

        c = sys.stdin.read(1)

    return counter


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(r_chars_count())
