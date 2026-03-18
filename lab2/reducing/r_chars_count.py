import sys

def r_chars_count():

    counter = 0

    divisor_series = 0
    max_divisors = 5

    c = sys.stdin.read(1)

    while c:
        if c == "-":
            divisor_series += 1
            # eof sequence found
            if divisor_series >= max_divisors:
                print(counter)
                return
        else:
            counter += divisor_series
            divisor_series = 0

            if not c.isspace():
                counter += 1

        c = sys.stdin.read(1)

    print(counter)

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    r_chars_count()