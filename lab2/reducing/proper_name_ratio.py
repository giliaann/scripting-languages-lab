from utils.split_first_word import split_first_word
from utils.get_sentence import get_sentence
import sys


def has_proper_name(sentence: str) -> bool:
    _, sentence = split_first_word(sentence)
    first_word, sentence = split_first_word(sentence)

    while first_word:
        if first_word[0].isupper():
            return True
        first_word, sentence = split_first_word(sentence)
    return False


def proper_name_ratio() -> float:
    sentence_counter = 0
    proper_name_sentence_counter = 0

    sentence, eof = get_sentence()

    while sentence:
        sentence_counter += 1
        if has_proper_name(sentence):
            proper_name_sentence_counter += 1
            print(sentence)

        if eof:
            break
        sentence, eof = get_sentence()

    return (
        proper_name_sentence_counter / sentence_counter
        if sentence_counter != 0
        else 0.0
    )


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(proper_name_ratio())
