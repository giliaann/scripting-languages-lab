from lab2.utils.get_sentence import get_sentence
from lab2.utils.split_first_word import split_first_word
from lab2.utils.extract_content import process_preamble, process_content


def proper_nouns():
    sentence, eof = get_sentence()

    while sentence:
        _, sentence = split_first_word(sentence)
        first_word, sentence = split_first_word(sentence)

        while first_word:
            if first_word[0].isupper():
                print(first_word)
            first_word, sentence = split_first_word(sentence)
        
        if eof:
            break

        sentence, eof = get_sentence()


if __name__ == '__main__':
    proper_nouns()

