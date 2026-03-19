from lab2.utils.get_sentence import get_sentence
from lab2.utils.split_first_word import split_first_word
import sys


def is_target_word(word: str) -> bool:
    return word == "i" or word == "oraz" or word == "ale" or word == "że" or word == "lub"

def sentence_conjecture() -> None:
    sentence, eof = get_sentence()

    while sentence:
        word, rest = split_first_word(sentence)
        special_word_count = 0

        while word:
            if is_target_word(word):
                special_word_count += 1

            if special_word_count >= 2:
                print(sentence)
                break

            word, rest = split_first_word(rest)

        if eof:
            break

        sentence, eof = get_sentence()


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    sentence_conjecture()
