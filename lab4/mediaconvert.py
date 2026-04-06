import typer
from utils import LogEntry
import utils
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from datetime import datetime
from pathlib import Path
from typing import Annotated


app = typer.Typer(help="Media converter CLI using ffmpeg / ImageMagick")


def process_file(file_path: Path, output_dir: Path, target_format: str) -> LogEntry | None:
    media_type = utils.get_media_type(file_path)
    if not media_type:
        return None

    program = utils.get_handle(media_type)
    if not program:
        return None

    timestampt = str(datetime.now().timestamp())
    dest_path = (output_dir / f"{timestampt}-{file_path.stem}.{target_format}").resolve()

    cmd = program(file_path, dest_path)
    tool = cmd[0]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return LogEntry(str(datetime.now().isoformat()), target_format, str(file_path), str(dest_path), tool, "SUCCESS")
    except subprocess.CalledProcessError as e:
        return LogEntry(
            str(datetime.now().isoformat()),
            target_format,
            str(file_path),
            str(dest_path),
            tool,
            "FAILED",
            e.stderr.strip(),
        )


@app.command()
def mediaconvert(
    directory: Annotated[
        Path,
        typer.Argument(..., exists=True, file_okay=False, readable=True, help="Directory containing files to convert"),
    ],
    target_format: Annotated[str, typer.Argument(..., help="Target format extension, e.g. mp3, mp4, jpg")],
    fast: Annotated[bool, typer.Option("--fast", help="Use all CPU cores")] = False,
) -> None:
    # chcek if source directory path exists
    if not directory.exists() or not directory.is_dir():
        typer.secho(f"Path {directory} does not exists or is not a directory", fg=typer.colors.RED)
        raise typer.Exit(1)

    files_to_process = utils.get_media_files(directory)

    if not files_to_process:
        typer.secho(f"Directory {directory} is empty, nothing to convert", fg=typer.colors.GREEN)
        raise typer.Exit(0)

    output_dir = utils.get_output_dir("CONVERTED_DIR", "converted")
    if not output_dir.exists():
        typer.secho(f"Creating directory: {output_dir}", fg=typer.colors.YELLOW)
        utils.ensure_directory_exists(output_dir)
    typer.secho(f"Converted files will be stored in: {output_dir}", fg=typer.colors.YELLOW)

    if fast:
        actual_workers = os.cpu_count() or 4
        typer.secho(f"Mode fast activated, using up to {actual_workers} processes", fg=typer.colors.YELLOW)
    else:
        actual_workers = 1

    logs = []

    with ProcessPoolExecutor(max_workers=actual_workers) as executor:
        futures = {
            executor.submit(process_file, file_path, output_dir, target_format): file_path
            for file_path in files_to_process
        }

        with typer.progressbar(as_completed(futures), length=len(futures), label="Converting") as progress:
            for future in progress:
                result_log = future.result()
                if result_log:
                    logs.append(result_log)

    log_path = output_dir / "logs.json"
    utils.log_json(log_path, logs)

    success_count = sum(1 for log in logs if log.status == "SUCCESS")
    count = len(logs)

    typer.secho(
        f"Converted {success_count}/{count} files",
        fg=typer.colors.GREEN if success_count == count else typer.colors.MAGENTA,
    )

    if success_count != count:
        typer.secho(f"Check logs for errors: {log_path}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
