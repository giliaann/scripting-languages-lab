import sys

sys.path.append("../utils")

from get_sentence import get_sentence
from split_first_word import split_first_word


def f_sentences_up_to_4_words():

    word_limit = 4

    sentence, eof = get_sentence()

    while sentence:
        word, remainder = split_first_word(sentence)
        word_count = 1 if word else 0

        while word and word_count < word_limit:
            word, remainder = split_first_word(remainder)
            word_count += 1
        
        word, remainder = split_first_word(remainder)
        # if there is no more words
        if not word:
            print(sentence)
        if eof:
            break
        sentence, eof = get_sentence()


if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    f_sentences_up_to_4_words()
