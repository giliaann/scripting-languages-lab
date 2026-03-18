import sys

sys.path.append("../utils")

from get_paragraph import get_paragraph

def r_paragraphs_count():
    paragraph, eof = get_paragraph()

    counter = 0

    while paragraph:
        counter += 1
        
        if eof:
            break
        
        paragraph,eof = get_paragraph()
    
    print(counter)

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    r_paragraphs_count()