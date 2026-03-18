import sys

# command to run script:
# $OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# before first usage of this function type this in code:
# sys.stdin.reconfigure(encoding="utf-8-sig")
# sys.stdout.reconfigure(encoding="utf-8")


def get_sentence():

    c = sys.stdin.read(1)

    divisor_series = 0
    max_divisors = 5
    eof_occured = False

    sentence = ""

    #sentence starts with a letter
    while c and not c.isalpha():
        if c == "-":
            divisor_series += 1
            # eof sequence found
            if divisor_series >= max_divisors:
                eof_occured = True
                return sentence, eof_occured
        else:
            divisor_series = 0
        c = sys.stdin.read(1)

    divisor_series = 0
    previous_new_line = False

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

class SentenceNotFound(Exception):
    pass


def find_first_complex_sentence():
    sentence, eof = get_sentence()
    
    while sentence:
        comma_count = 0
        has_letters_in_segment = False

        for char in sentence:
            if char.isalpha():
                has_letters_in_segment = True
                if comma_count >= 2:
                    return sentence.strip()
                
            elif char == ',' and has_letters_in_segment:
                comma_count += 1
                has_letters_in_segment = False
                
        if eof:
            break
        sentence, eof = get_sentence()
    
    raise SentenceNotFound('W tekscie nie ma ani jednego zdania zlozonego')


if __name__ == '__main__':
    print(find_first_complex_sentence())
    