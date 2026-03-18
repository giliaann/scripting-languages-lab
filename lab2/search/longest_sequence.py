import sys
from utils.get_sentence import get_sentence


def search_longest_sequence():
    longest_sequence = ""

    sequence, eof = get_sentence()
    while sequence:
        if len(sequence) > len(longest_sequence):
            longest_sequence = sequence

        if eof:
            break
        sequence, eof = get_sentence()

    return longest_sequence


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(search_longest_sequence())
