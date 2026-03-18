import sys
from utils.get_sentence import get_sentence


class SentenceNotFound(Exception):
    pass


def find_first_complex_sentence() -> str:
    sentence, eof = get_sentence()

    while sentence:
        comma_count = 0
        has_letters_in_segment = False

        for char in sentence:
            if char.isalpha():
                has_letters_in_segment = True
                if comma_count >= 2:
                    return sentence.strip()

            elif char == "," and has_letters_in_segment:
                comma_count += 1
                has_letters_in_segment = False

        if eof:
            break

        sentence, eof = get_sentence()

    raise SentenceNotFound("W tekscie nie ma ani jednego zdania zlozonego")


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(find_first_complex_sentence())
