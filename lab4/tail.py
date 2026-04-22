import sys
import time
import typer
from pathlib import Path
from collections import deque
from collections.abc import Iterable
from file_read_backwards import FileReadBackwards
from itertools import islice


app = typer.Typer()


def read_last_lines(lines_iter: Iterable[str], n: int) -> Iterable[str]:
    return deque(lines_iter, maxlen=n)


def read_last_lines_file(filepath: Path, n: int) -> Iterable[str]:
    with FileReadBackwards(filepath, encoding="utf-8") as f:
        lines = tuple(islice(f, n))
    return reversed(lines)


def follow_file(filepath: Path) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        f.seek(0, 2)
        while True:
            new_content = f.read()
            if new_content:
                sys.stdout.write(new_content)
                sys.stdout.flush()
            else:
                time.sleep(0.2)
                # checking if file has been moved or removed
                try:
                    # checking if file has been truncated
                    current_size = filepath.stat().st_size
                    if f.tell() > current_size:
                        f.seek(0)
                except FileNotFoundError:
                    typer.echo(f"Error: file ceased to exist at this path: {filepath}", err=True)
                    raise typer.Exit(1)


@app.command()
def tail(
    file: Path | None = typer.Argument(None),
    lines: int = typer.Option(10, "--lines", "-n", min=0),
    follow: bool = typer.Option(False, "--follow", "-f"),
):
    if file:
        if not file.exists():
            typer.echo(f"Error: File does not exist: {file}", err=True)
            raise typer.Exit(1)
        if not file.is_file():
            typer.echo(f"Error: {file} is not a file", err=True)
            raise typer.Exit(1)
        last_lines = read_last_lines_file(file, lines)
    else:
        if follow:
            typer.echo("Error: option --follow requires filepath", err=True)
            raise typer.Exit(1)

        if sys.stdin.isatty():
            typer.echo("Error: no data on input and not filepath given", err=True)
            raise typer.Exit(1)

        last_lines = read_last_lines(sys.stdin, lines)

    for line in last_lines:
        sys.stdout.write(line if line.endswith("\n") else line + "\n")
    sys.stdout.flush()

    if file and follow:
        try:
            follow_file(file)
        except KeyboardInterrupt:
            raise typer.Exit(0)


if __name__ == "__main__":
    app()
