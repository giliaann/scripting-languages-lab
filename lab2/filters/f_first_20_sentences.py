from utils.get_sentence import get_sentence
import sys


def f_first_20_sentences() -> None:
    sentence, eof = get_sentence()

    counter = 0

    while sentence and counter < 20:
        print(sentence)
        counter += 1
        if eof:
            break
        sentence, eof = get_sentence()

    if counter != 20:
        raise ValueError("The file does not contain 20 sentences")


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    f_first_20_sentences()
