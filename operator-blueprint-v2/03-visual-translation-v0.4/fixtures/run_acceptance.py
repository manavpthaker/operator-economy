#!/usr/bin/env python3
"""Run the preserved v0.3 controls plus the additive v0.4 controls."""

import pathlib
import re
import subprocess
import sys


HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = REPO / "operator-blueprint-v2/03-visual-translation/fixtures"
BASE_VALIDATOR = BASE / "validate.py"
V04_VALIDATOR = HERE / "validate.py"
PRODUCTION_CASE_GUARD = HERE / "check_production_case_rejected.py"


def numeric_case(path):
    match = re.match(r"a(\d+)-", path.name)
    return int(match.group(1)) if match else 10_000


controls = [
    ("v0.3/p01-clean-legacy", [sys.executable, str(BASE_VALIDATOR), "--legacy", str(BASE / "positive/clean-baseline")]),
    ("v0.3/p02-boundary-ledger", [sys.executable, str(BASE_VALIDATOR), str(BASE / "positive/boundary-ledger-derived")]),
    ("v0.3/p03-markdown-provenance", [sys.executable, str(BASE_VALIDATOR), str(BASE / "positive/markdown-provenance")]),
    ("v0.3/p04-establishment", [sys.executable, str(BASE_VALIDATOR), str(BASE / "positive/establishment-class")]),
]

for case in sorted((BASE / "adversarial").glob("a*-*"), key=numeric_case):
    number = numeric_case(case)
    command = [sys.executable, str(BASE_VALIDATOR)]
    if number <= 9:
        command.append("--legacy")
    command.append(str(case))
    controls.append((f"v0.3/{case.name}", command))

controls.append(("v0.4/p01-film-layer", [sys.executable, str(V04_VALIDATOR), str(HERE / "positive/film-layer")]))
controls.append(("v0.4/p02-full-input-lock", [sys.executable, str(V04_VALIDATOR), "--through", "V1", str(HERE / "positive/full-input-lock")]))
controls.append(("v0.4/p03-production-case-guard", [sys.executable, str(PRODUCTION_CASE_GUARD)]))
for case in sorted((HERE / "adversarial").glob("a*-*"), key=numeric_case):
    command = [sys.executable, str(V04_VALIDATOR)]
    if numeric_case(case) >= 62:
        command.extend(["--through", "V1"])
    command.append(str(case))
    controls.append((f"v0.4/{case.name}", command))

failed = []
for label, command in controls:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode == 0:
        print(f"PASS {label}")
    else:
        failed.append(label)
        print(f"FAIL {label}")
        print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())

print(f"RESULT {len(controls) - len(failed)}/{len(controls)} controls passed")
if failed:
    print("FAILED " + ", ".join(failed))
raise SystemExit(1 if failed else 0)
