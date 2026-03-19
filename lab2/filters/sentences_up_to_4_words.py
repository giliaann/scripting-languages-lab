import sys
from lab2.utils.get_sentence import get_sentence
from lab2.utils.split_first_word import split_first_word

def has_up_to_4_words(sentence: str) -> bool:
    word_limit = 4

    word, remainder = split_first_word(sentence)
    word_count = 1 if word else 0

    while word and word_count < word_limit:
        word, remainder = split_first_word(remainder)
        word_count += 1

    word, remainder = split_first_word(remainder)
    
    return not word


def f_sentences_up_to_4_words() -> None:
    sentence, eof = get_sentence()

    while sentence:

        if has_up_to_4_words(sentence):
            print(sentence)

        if eof:
            break
        sentence, eof = get_sentence()


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    f_sentences_up_to_4_words()
