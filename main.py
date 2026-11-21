# Entry program for make.fun's the-poster-for-a-place-that-i-2-20261121-0539 contest.
#
# The repository ships one finished travel poster, entry.png (a vintage
# poster for VELMORA, a fictional island where the aurora pools in a
# still lagoon, generated as an image and resized/quantized to the
# 1 MiB, 1024x1024 gate). The grader runs this file twice, offline,
# and both runs must leave identical bytes in the output folder — so
# the program does the simplest possible thing: copy the picture next
# to it into the output directory and report its size.
# MAKEFUN_OUTPUT_DIR stands in for /output when the program runs
# outside the grader.

import os
import shutil
import struct
import sys

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# Gate limits from the competition rules: a whole PNG or JPEG of at most
# 1 MiB and at most 1024 by 1024 pixels. Validate the shipped picture
# before copying so a bad file fails loudly instead of entering invalid.
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_png(path):
    """Check path is a PNG within the gate; raise SystemExit otherwise."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the {MAX_BYTES} limit")
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG file")
    if len(head) < 29 or head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit(f"entry.png is {width}x{height}, over {MAX_DIMENSION}x{MAX_DIMENSION}")
    return size


validate_png(SRC)

os.makedirs(OUT_DIR, exist_ok=True)
target = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(SRC, target)

size = os.path.getsize(target)
print(f"entry.png -> {target} ({size} bytes)")
sys.exit(0 if size <= 1_048_576 else 1)
