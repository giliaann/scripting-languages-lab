import sys
import json
import re
from pathlib import Path
from collections import Counter


def read_path() -> Path | None:
    line = sys.stdin.readline().strip()
    return Path(line) if line else None


def analyze(file_path: Path) -> str:

    results = {"lines": 0, "path": str(file_path)}

    chars_counter = Counter()
    words_counter = Counter()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            results["lines"] += 1

            lowercase_line = line.lower()
            chars_counter.update((c for c in lowercase_line if not c.isspace()))
            words_counter.update(re.findall(r"\w+", lowercase_line))

    results["words"] = words_counter.total()
    results["chars"] = chars_counter.total()
    results["most_common_word"] = words_counter.most_common(1)[0][0] if words_counter else None
    results["most_common_char"] = chars_counter.most_common(1)[0][0] if chars_counter else None

    return json.dumps(results, indent=3)


def txt_analyzer() -> None:

    file_path = read_path()

    if not file_path:
        sys.stderr.write("Failed to read any path" + "\n")
        return

    if not file_path.is_file():
        sys.stderr.write(f"{file_path} is not a valid file path" + "\n")
        return

    if not (file_path.suffix.lower() == ".txt"):
        sys.stderr.write(f"File {file_path} is not a .txt file" + "\n")
        return

    result = analyze(file_path)

    sys.stdout.write(result + "\n")


if __name__ == "__main__":
    txt_analyzer()
