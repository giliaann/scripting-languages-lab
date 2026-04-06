import sys
import os


def show_env_vars() -> None:
    lower_args = {arg.lower() for arg in sys.argv[1:]}
    env_vars = os.environ

    if lower_args:
        filtered_env_vars = ((k, v) for k, v in env_vars.items() if any(arg in k.lower() for arg in lower_args))
    else:
        filtered_env_vars = env_vars.items()

    for var, path in sorted(filtered_env_vars):
        print(f"{var}={path}")


if __name__ == "__main__":
    show_env_vars()
