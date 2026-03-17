import sys

# command to run script:
# $OutputEncoding = [System.Text.Encoding]::UTF8
# cat -Encoding UTF8 ../data/dickens-opowiesc-wigilijna.txt | python extract_content.py

def process_preamble():

    whitespaces_buffer = ""
    preamble_buffer = ""

    end_of_preamble_white_lines = 2
    max_preamble_lines = 10
    max_divisors = 5

    line_count = 0
    new_line_series = 0
    divisor_series = 0

    leading_new_line = True
    eof_occured = False

    c = sys.stdin.read(1)

    while (
        c
        and new_line_series < end_of_preamble_white_lines + 1
        and line_count < max_preamble_lines
    ):
        if c == "-":
            divisor_series += 1
            # eof mark found
            if divisor_series >= max_divisors:
                eof_occured = True
                break
        else:
            # few divisors are content
            preamble_buffer += "-" * divisor_series
            divisor_series = 0

            if c.isspace():
                if c == "\n":
                    preamble_buffer += c
                    #'\n' terminating a sequence - end of line, all whitespaces have to be ommited
                    leading_new_line = True
                    whitespaces_buffer = ""
                    new_line_series += 1
                    line_count += 1

                elif not leading_new_line:
                    #'\n' - leads a sequence - start of line, all whitespaces have to be ommited

                    # ommit spaces that are not necessary
                    if c == " ":
                        if not whitespaces_buffer:
                            whitespaces_buffer = c
                    else:
                        whitespaces_buffer += c

            else:
                # not a whitespace breaks new line series
                new_line_series = 0
                leading_new_line = False
                # if there are whitespaces, they are between sentences
                if whitespaces_buffer:
                    preamble_buffer += whitespaces_buffer
                    whitespaces_buffer = ""
                preamble_buffer += c

        c = sys.stdin.read(1)

        # if this condition is met after max_preamble_lines, there is no preamble
        has_preamble = (
            not eof_occured and not new_line_series < end_of_preamble_white_lines + 1
        )

    if not eof_occured:
        preamble_buffer += "-" * divisor_series

    return preamble_buffer, has_preamble, eof_occured, c


def process_content(c):

    max_divisors = 5
    divisor_series = 0
    whitespaces_buffer = ""

    # if a sequence of whitespaces has leading '\n', without any letter, all whitespces should be ommited
    leading_new_line = True

    eof_occured = False

    while c:
        if c == "-":
            divisor_series += 1
            # eof mark found
            if divisor_series >= max_divisors:
                eof_occured = True
                break
        else:
            # few divisors are content
            print("-" * divisor_series, end="")
            divisor_series = 0

            if c.isspace():
                if c == "\n":
                    print(c, end="")
                    #'\n' terminating a sequence - end of line, all whitespaces have to be ommited
                    leading_new_line = True
                    whitespaces_buffer = ""

                elif not leading_new_line:
                    # ommit spaces that are not necessary
                    if c == " ":
                        if not whitespaces_buffer:
                            whitespaces_buffer = c
                    else:
                        whitespaces_buffer += c

            else:
                # if there are whitespaces, they are between sentences
                if whitespaces_buffer:
                    print(whitespaces_buffer, end="")
                    whitespaces_buffer = ""
                leading_new_line = False
                print(c, end="")

        c = sys.stdin.read(1)

    # adding last divisors if they were not eof
    if not eof_occured:
        print("-" * divisor_series, end="")


def main():

    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    preamble_buffer, has_preamble, eof_occured, c = process_preamble()

    if not has_preamble:
        print(preamble_buffer, end="")

    if eof_occured:
        return

    process_content(c if c else sys.stdin.read(1))


if __name__ == "__main__":
    main()
