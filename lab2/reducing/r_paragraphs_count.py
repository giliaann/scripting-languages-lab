import sys
from lab2.utils.get_paragraph import get_paragraph


def r_paragraphs_count():
    paragraph, eof = get_paragraph()

    counter = 0

    while paragraph:
        counter += 1

        if eof:
            break

        paragraph, eof = get_paragraph()

    return counter


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdin.reconfigure(encoding="utf-8-sig")
        sys.stdout.reconfigure(encoding="utf-8")
    print(r_paragraphs_count())
