#!/usr/bin/env python3
"""Copy EP009 world-kit definitions into a HyperFrames composition.

  python3 kit_defs.py list
  python3 kit_defs.py defs kit-guest kit-desk            # print <g> defs plus dependencies
  python3 kit_defs.py inject path/to/index.html [ids...] # replace <!-- KIT:DEFS:BEGIN -->...<!-- KIT:DEFS:END -->
  python3 kit_defs.py inline kit-ceiling-slip-filled --prefix s10-slip
      # print the object's children with ids renamed (kit-ceiling-slip-filled__box1 -> s10-slip__box1)
      # so single parts can be animated. Dependencies (href="#kit-...") still need defs.

Inline markup is copied from kit.svg byte for byte apart from the xmlns attribute and renamed ids.
"""
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent / "kit.svg"
BEGIN, END = "<!-- KIT:DEFS:BEGIN -->", "<!-- KIT:DEFS:END -->"


def blocks():
    text = KIT.read_text()
    out = {}
    for m in re.finditer(r'<g id="(kit-[a-z0-9-]+)" data-kit-desc="([^"]*)">\n(.*?)\n</g>(?=\n<g id="kit-|\n</defs>)', text, re.S):
        out[m.group(1)] = (m.group(0), m.group(2), m.group(3))
    return out


def closure(ids, B):
    seen, stack = [], list(ids)
    while stack:
        i = stack.pop(0)
        if i in seen:
            continue
        if i not in B:
            sys.exit(f"unknown kit id: {i}")
        seen.append(i)
        stack += re.findall(r'href="#(kit-[a-z0-9-]+)"', B[i][0])
    return seen


def main():
    B = blocks()
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        for k, v in B.items():
            print(f"{k}\t{v[1]}")
        return
    cmd = sys.argv[1]
    if cmd == "defs":
        print("\n".join(B[i][0] for i in closure(sys.argv[2:] or list(B), B)))
    elif cmd == "inject":
        target = Path(sys.argv[2])
        ids = closure(sys.argv[3:] or list(B), B)
        html = target.read_text()
        if BEGIN not in html or END not in html:
            sys.exit(f"markers {BEGIN} / {END} not found in {target}")
        # one line per object keeps compositions under the HyperFrames file-length lint
        defs = "\n".join(B[i][0].replace("\n", "") for i in ids)
        pre, rest = html.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        target.write_text(pre + BEGIN + "\n" + defs + "\n" + END + post)
        print(f"injected {len(ids)} kit objects into {target}")
    elif cmd == "inline":
        oid = sys.argv[2]
        prefix = sys.argv[sys.argv.index("--prefix") + 1] if "--prefix" in sys.argv else oid
        body = B[oid][2].replace(f'id="{oid}__', f'id="{prefix}__')
        print(body)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
