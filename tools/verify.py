"""Repeat fixed local checks into a fresh directory inside this project.

Usage: python tools/verify.py --output NEW_DIRECTORY. Installed Bandit is required.
Temporarily mutates only own model.py and restores exact original bytes in finally.
No input-derived commands, shell, network, package installation or publication.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
# Only fixed reviewed interpreter checks, never shell or synthetic case commands.
import subprocess  # nosec B404
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(arguments, output, name, expected=0):
    environment = os.environ.copy()
    # Fresh, nonexistent cache location plus disabled writes prevents stale same-size
    # mutant imports. Tests' fixed children inherit this setting, not older pyc files.
    environment["PYTHONPYCACHEPREFIX"] = str(output / (name + "-no-bytecode"))
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    if name == "compile":
        # Explicit compileall writes to the ordinary own-source cache; the relocated
        # cache path duplicated this long Windows workspace path and failed creation.
        environment.pop("PYTHONPYCACHEPREFIX", None)
    result = subprocess.run([sys.executable] + arguments, cwd=ROOT, env=environment,
                            capture_output=True, timeout=60, check=False)  # nosec B603
    (output / (name + ".stdout.txt")).write_bytes(result.stdout)
    (output / (name + ".stderr.txt")).write_bytes(result.stderr)
    passed = result.returncode == expected
    if expected == 1:
        log = result.stderr.decode("utf-8", "replace")
        passed = passed and bool(re.search(r"FAILED \(failures=[1-9][0-9]*\)", log)) and "FAIL: test_frozen_labels" in log
    return {"name":name, "arguments":arguments, "exit_code":result.returncode,
            "expected_exit":expected, "passed":passed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        parser.error("evidence output must be a new directory inside this project")
    output.mkdir(parents=True, exist_ok=False)
    checks = []
    checks.append(run(["-m", "unittest", "discover", "-s", "tests", "-v"], output, "tests-normal"))
    checks.append(run(["-O", "-m", "unittest", "discover", "-s", "tests", "-v"], output, "tests-optimized"))
    checks.append(run(["-m", "compileall", "-q", "redirectlab", "tests", "tools"], output, "compile"))
    checks.append(run(["-m", "bandit", "-r", "redirectlab", "tests", "tools", "-f", "json"], output, "bandit"))
    model = ROOT / "redirectlab/model.py"
    original = model.read_bytes()
    mutations = [
        ("rewrite-preserving-codes", b'if status == 303:', b'if status in (303, 307, 308):'),
        ("lose-post-preserve-choice", b'rule = "POST_PRESERVED"', b'proposed, rule = "GET", "POST_TO_GET"'),
        ("idempotent-means-safe", b'UNSAFE = ("POST", "PUT", "DELETE", "PATCH")', b'UNSAFE = ("POST", "PATCH")'),
        ("skip-unavailable-body", b'if case["body"] == "nonreplayable":', b'if False:'),
        ("known-stop-loses-unknown", b'row["unknowns"] = sorted(set(row["unknowns"]))', b'row["unknowns"] = [] if row["blockers"] else sorted(set(row["unknowns"]))'),
    ]
    try:
        for name, before, after in mutations:
            if original.count(before) != 1:
                raise RuntimeError("mutation target changed")
            model.write_bytes(original.replace(before, after))
            checks.append(run(["-B", "-m", "unittest", "discover", "-s", "tests", "-v"], output, name, 1))
            model.write_bytes(original)
    finally:
        model.write_bytes(original)
    restored = model.read_bytes() == original
    checks.append(run(["-B", "-m", "unittest", "discover", "-s", "tests", "-v"], output, "tests-restored"))
    for format_name in ("json", "markdown"):
        target = output / ("demo." + ("json" if format_name == "json" else "md"))
        checks.append(run(["-m", "redirectlab", "fixtures/cases.json", "--format", format_name,
                           "--output", str(target)], output, "demo-" + format_name, 2))
    boundaries, stress = [], []
    for name in ("tests-normal", "tests-optimized"):
        for line in (output / (name + ".stdout.txt")).read_text(encoding="utf-8").splitlines():
            if line.startswith("BOUNDARY_RECORDS "):
                boundaries.extend(json.loads(line.removeprefix("BOUNDARY_RECORDS ")))
            elif line.startswith("STRESS_RECORD "):
                stress.append(json.loads(line.removeprefix("STRESS_RECORD ")))
    (output / "cli-boundary.json").write_text(json.dumps(boundaries, indent=2) + "\n", encoding="utf-8")
    (output / "stress.json").write_text(json.dumps(stress, indent=2) + "\n", encoding="utf-8")
    files = [*ROOT.joinpath("redirectlab").glob("*.py"), ROOT / "tests/test_lab.py", ROOT / "tools/verify.py",
             ROOT / "fixtures/cases.json", ROOT / "fixtures/expected.json", ROOT / "fixtures/errors.json", ROOT / "CONTRACT.md"]
    receipt = {"runtime":sys.version, "checks":checks, "model_restored":restored,
               "hashes":{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
               "passed":restored and all(item["passed"] for item in checks)}
    (output / "results.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed":receipt["passed"], "checks":len(checks), "restored":restored}))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
