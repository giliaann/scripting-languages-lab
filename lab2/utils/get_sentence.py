import sys

# command to run script:
# $OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# before first usage of this function type this in code:
# sys.stdin.reconfigure(encoding="utf-8-sig")
# sys.stdout.reconfigure(encoding="utf-8")


def get_sentence():

    c = sys.stdin.read(1)

    # end of sentence chars: '?', '!', '.', '\n' ...whistepsaces.. '\n'

    while c and c.isspace():
        c = sys.stdin.read(1)

    eof_occured = False
    previous_new_line = False
    divisor_series = 0
    max_divisors = 5

    sentence = ""

    #any char starts a sentence, '.' is a snetence 

    while c and c != "?" and c != "!" and c != ".":
        # checking eof chars
        if c == "-":
            divisor_series += 1
            # eof sequence found
            if divisor_series >= max_divisors:
                eof_occured = True
                break
        else:
            sentence += "-" * divisor_series
            divisor_series = 0

            if c == "\n":
                # double new line means end of sentence
                if previous_new_line:
                    break
                else:
                    previous_new_line = True
            elif not c.isspace():
                # potential double new line interrupted
                previous_new_line = False

            sentence += c

        c = sys.stdin.read(1)

    if c and not c.isspace() and c != "-":
        sentence += c

    if not eof_occured:
        sentence += "-" * divisor_series

    # return value and strip whitespaces at the end
    return sentence.strip(), eof_occured
