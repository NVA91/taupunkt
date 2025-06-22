"""Upload the micropython package to a connected Pico using mpremote."""

import subprocess
import pathlib
import sys


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else ":/"
    root = pathlib.Path(__file__).resolve().parents[1]
    subprocess.run([
        "mpremote",
        "cp",
        str(root),
        dest,
    ], check=True)


if __name__ == "__main__":
    main()
