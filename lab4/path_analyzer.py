import os
import sys
from pathlib import Path


def is_executable(filepath: Path) -> bool:
    if not filepath.is_file():
        return False
    
    if sys.platform == 'win32':
        pathext = os.environ.get('PATHEXT', '.COM;.EXE;.BAT;.CMD').lower()
        valid_extensions = tuple(pathext.split(os.pathsep))
        return filepath.suffix.lower() in valid_extensions
    return os.access(filepath, os.X_OK)


def get_PATHS() -> list[Path]:
    path_env = os.environ.get('PATH', '')
    paths = [Path(path) for path in path_env.split(os.pathsep) if path]
    return paths



def list_executables(directory: Path) -> list[Path]:
    return [path for path in directory.iterdir() if is_executable(path)]


def path_analyzer() -> None:
    args = sys.argv[1:]

    show_executables = '--exe' in args

    paths = get_PATHS()

    for path in paths:
        print(path.resolve())
        if show_executables:
            execs = list_executables(path)
            for exec in execs:
                print(f'\t{exec.name}')



if __name__=='__main__':
    path_analyzer()


