import sys
from utils.split_first_word import split_first_word
from utils.get_sentence import get_sentence


def has_two_words_with_same_initial(sentence: str) -> bool:
    last_first_letter = ""

    word, rest = split_first_word(sentence)
    while word:
        if word[0] == last_first_letter:
            return True
        last_first_letter = word[0]
        word, rest = split_first_word(rest)
    return False


def longest_non_repeating_initials_sentence() -> str:
    longest_sentence = ""

    sentence, eof = get_sentence()

    while sentence:
        if not has_two_words_with_same_initial(sentence):
            if len(sentence) > len(longest_sentence):
                longest_sentence = sentence

        if eof:
            break
        sentence, eof = get_sentence()

    return longest_sentence


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(longest_non_repeating_initials_sentence())
