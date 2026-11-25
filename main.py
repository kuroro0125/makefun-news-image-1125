#!/usr/bin/env python3
"""Entry point for the 25 November 2026 news-image entry.

The front page is rendered by render.py into entry.png (1024x1024, well
under 1 MiB, deterministic). This program only places that file where the
grader expects it: <output dir>/entry.png. The output dir comes from
MAKEFUN_OUTPUT_DIR, defaulting to /output in the grading container.
Standard library only; no network, no randomness.
"""
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
LIMIT_BYTES = 1_048_576
MAX_SIDE = 1024


def png_size(path: Path) -> tuple:
    """Read width/height straight from the PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    size = target.stat().st_size
    if size > LIMIT_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    width, height = png_size(target)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png is {width}x{height}, over the 1024px limit",
              file=sys.stderr)
        return 1
    print(f"wrote {target} ({width}x{height}, {size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
