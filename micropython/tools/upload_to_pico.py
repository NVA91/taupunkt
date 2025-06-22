"""Upload the micropython package to a connected Pico using mpremote."""

import subprocess
import pathlib
import sys
import shutil


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else ":/"
    root = pathlib.Path(__file__).resolve().parents[1]

    if shutil.which("mpremote") is None:
        print("mpremote not found. Install it via 'pip install mpremote'.")
        return

    subprocess.run(
        ["mpremote", "cp", "-r", str(root), dest],
        check=True,
    )


if __name__ == "__main__":
    main()
