from lab2.utils.get_sentence import get_sentence
import sys

def is_exclamation_or_question(sentence: str) -> bool:
    last_char = sentence[-1]
    return last_char == "!" or last_char == "?"


def f_sentences_exclamations_questions() -> None:
    sentence, eof = get_sentence()

    while sentence:

        if is_exclamation_or_question(sentence):
            print(sentence)

        if eof:
            break
        sentence, eof = get_sentence()


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    f_sentences_exclamations_questions()
