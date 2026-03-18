
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


def split_first_word(sentence):
    word = ""
    remainder = ""
    i = 0
    while i < len(sentence):
        c = sentence[i]
        if c.isalpha():
            word += c
        #ommit first whitespaces
        elif len(word) != 0:
            break
        i += 1
    
    remainder = sentence[i:]

    return word, remainder


def has_two_words_with_same_initial(sentence: str) -> bool:
    """
    Checks if the string contains two consecutive words starting with the same letter.
    """
    last_first_letter = ''

    word, rest = split_first_word(sentence)
    while word:
        if word[0] == last_first_letter:
            return True
        last_first_letter = word[0]
        word, rest = split_first_word(rest)
    return False


def longest_non_repeating_initials_sentence():
    longest_sentence = ''

    sentence, eof = get_sentence()

    while sentence:
        if not has_two_words_with_same_initial(sentence):
            if len(sentence) > len(longest_sentence):
                longest_sentence = sentence

        if eof:
            break
        sentence, eof = get_sentence()

    return longest_sentence


if __name__ == '__main__':
    print(longest_non_repeating_initials_sentence())
