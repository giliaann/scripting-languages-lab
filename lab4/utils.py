import os
from pathlib import Path
from typing import Callable
import mimetypes
import shutil
import json
from dataclasses import dataclass, asdict


@dataclass
class LogEntry:
    timestamp: str
    target_format: str
    source_path: str
    destination_path: str
    tool_used: str
    status: str
    error_msg: str = ""


def get_output_dir(env_var_name: str, default_dir_name: str, base_path: Path | None = None) -> Path:
    env_dir = os.environ.get(env_var_name)

    if env_dir:
        return Path(env_dir).resolve()

    base = base_path if base_path else Path.cwd()
    return (base / default_dir_name).resolve()


def ensure_directory_exists(directory_path: Path) -> Path:
    directory_path.mkdir(parents=True, exist_ok=True)
    return directory_path


def get_media_files(dir_path: Path) -> list[Path]:
    return [path for path in dir_path.iterdir() if path.is_file()]


type media_conv = Callable[[Path, Path], list[str]]
media_convert_registy: dict[str, media_conv] = {}


def register_media_converter(media_type: str):
    def decorator(func: media_conv):
        media_convert_registy[media_type] = func
        return func

    return decorator


@register_media_converter("audio")
@register_media_converter("video")
def ffmpeg(in_path: Path, out_path: Path) -> list[str]:
    return ["ffmpeg", "-i", str(in_path), str(out_path)]


@register_media_converter("image")
def magick(in_path: Path, out_path: Path) -> list[str]:
    return ["magick" if shutil.which("magick") else "convert", str(in_path), str(out_path)]


def get_handle(media_type: str) -> media_conv | None:
    return media_convert_registy.get(media_type)


def get_media_type(file_path: Path) -> str | None:
    mime, _ = mimetypes.guess_type(file_path)
    if not mime:
        return None

    prefix = mime.split("/")[0]
    return prefix


def log_json(log_path: Path, logs: list[LogEntry]) -> None:
    with open(log_path, mode="a", encoding="utf-8") as f:
        for entry in logs:
            f.write(json.dumps(asdict(entry)) + "\n")
