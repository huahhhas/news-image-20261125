#!/usr/bin/env python3
"""news-image-20261125: write the day's news image to the output dir.

Pure stdlib, no network. Copies the image shipped beside this file
(entry.png, drawn for Wednesday 25 November 2026) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
Deterministic: the same bytes every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    # MAKEFUN_OUTPUT_DIR may name a directory or the file itself.
    if out_dir.endswith(".png"):
        dst = out_dir
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    else:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
